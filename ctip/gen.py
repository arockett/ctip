# -*- coding: utf-8 -*-
"""
Define objects for handling genfile reading, writing, and iteration.

Created on Sun Jul 10 14:48:26 2016

@author: Aaron Beckett
"""

import pyparsing as p

from .utils import frange

TAB = ' ' * 4


class GenSchema(object):
    """
    Object representation of a gen schema.
    
    The GenSchema class is used  for reading and writing genfiles as well as
    iterating over the configurations defined by a gen schema.
    
    
    The primary functions used for reading and writing a genfile are:
        
        build_from_file(filename)
        write_to_file(schema, filename)
    
    The gen schema API is defined by the functions:
    
        add_values(variable, *values)
        add_dependencies(variable, value, *dependencies)
        
        
    The structure of a gen schema's variables and dependencies can be
    summarized by the following json object:
    
        {
            'variable1': [
                ['val1.1', null],
                ['val1.2', null]
            ],
            'variable2': [
                ['val2.1', null],
                [
                    'val2.2',
                    {
                        'dependent1': ['dval1.1', 'dval1.2'],
                        'dependent2': ['dval2.1']
                    }
                ],
                ['val2.3', null]
            ]
        }
        
    Notice how the dependents tied to 'val2.2' really just define a nested
    gen schema which is linked to 'val2.2'.
    """
    
    def __init__(self, name = None):
        """
        Initialize a GenSchema object.
        
        Args:
            name: (str) Optional name for the schema.
        """
        self.name = name
        self.schema = {}
    
    def add_values(self, variable, *values):
        """
        Add values to a variable's list of valid values.

        If the variable doesn't exist, it is created.
        If the value already exists in the variable's domain it is not added again.
        If a value is passed in twice it is only added to the variable's domain once (provided it does not aready
        exist in the domain).
        Variables and values can be any immutable datatype besides a tuple.
        
        Args:
            variable: Name of the variable to add values to.
            *values: One or more values to add to the variable.
        Raises:
            TypeError if no values are provided or the variable/values are not strings, ints, or floats
        """
        
        def valid_type(v):
            return type(v) == str or type(v) == int or type(v) == float
            
        unique = set()
        current_domain = {v[0] for v in self.schema[variable]} if variable in self.schema else None
        def check_uniqueness(v):
            """
            Check if v is already in the variable domain or duplicated in the values.

            Args:
                v: value to check
            Returns:
                True if v is not already in the variable's domain AND has not already been flagged as unique.
            """
            # test v against set of already checked values and
            # current domain of the variable
            if v in unique or (current_domain and v in current_domain):
                return False
            # v is not duplicated, add it to the set of checked values
            unique.add(v)
            return True
            
        if not values:
            raise TypeError("Must provide at least one value to add_values()")
            
        if not valid_type(variable) or not all([valid_type(v) for v in values]):
            raise TypeError("Gen schema variables and values must be strings, ints, or floats")
            
        values = [(v,None) for v in values if check_uniqueness(v)]
        
        if variable not in self.schema:
            self.schema[variable] = values
        else:
            self.schema[variable].extend(values)
    
    def add_dependencies(self, variable, value, *dependencies):
        """
        Bind dependent gen schemas to a particular value of a variable.

        The variable and value must already exist and dependencies must be
        a GenSchema.
        
        Args:
            variable: Variable containing the value aquiring dependencies.
            value: Value aquiring dependencies.
            *dependencies: One or more GenSchema to add as dependent schemas.
        Raises:
            TypeError if no dependencies are provided or a dependency is not of type GenSchema
            KeyError if the variable does not exist in the GenSchema
            ValueError if the value is not in the variable's domain
        """
        
        if not dependencies:
            raise TypeError("Must provide at least one dependency to add_dependencies()")
            
        if not all([isinstance(d, GenSchema) for d in dependencies]):
            raise TypeError("Dependencies must be of type GenSchema")
            
        try:
            values = self.schema[variable]
            idx = [v[0] for v in values].index(value)
        except KeyError as e:
            raise KeyError("{} does not exist in the gen schema".format(variable)) from e
        except ValueError as e:
            raise ValueError("{} is not a valid value for {}".format(value,variable)) from e
            
        if values[idx][1] is None:
            values[idx] = (values[idx][0], GenSchema())
        for dep in dependencies:
            values[idx][1].schema.update(dep.schema)
    
    def configs(self):
        """Generate all configurations represented by the schema."""
        
        # Make sure there's a schema with which to generate configs
        if not self.schema:
            raise StopIteration
        
        # List of the variable names to maintain an order
        variables = list(self.schema.keys())
        N = len(variables)
        # Indices tracking which value is next for each variable
        cursors = [-1] * N
        # References to any generator used to get a value's sub-variables
        gens = [None] * N
        # List holding pieces of the curent config associated with each variable.
        # Config pieces are dictionaries of variables and their values. The piece
        # associated with a varialbe at this level will have more than just that
        # variable only if there are sub-variables associated with its current value.
        config_pieces = [{}] * N
            
        def increment(variable, idx):
            """
            Update the config piece associated with this variable.
            
            Args:
                variable: Name of the variable to increment.
                idx: (int) Index of the variable in the order.
            """
            # Store whether or not the values for this variable rolled-over
            cycled = False
            # The new piece of the config associated with this variable
            piece = {}
            
            # If there's a generator for this variable, the current value we're
            # on has sub-variables. This means we should get the next round of
            # sub-variables and only increment the cursor if there are no more
            # sub-variables to be generated.
            if gens[idx]:
                val = self.schema[variable][cursors[idx]][0]
                try:
                    piece = next(gens[idx])
                except StopIteration:
                    # No more sub-variables to generate, un-store generator
                    # so we fall in to the cursor incrementing if statement
                    gens[idx] = None
                    
            # If there is no generator, either there never were sub-variables or
            # the sub-variables ran out. Either way, we need to increment the
            # cursor and move on to the next value. 
            if not gens[idx]:
                # Increment the cursor tracking which value we're on for this
                # variable. Detect if we've cycled so we can return that flag.
                pos = cursors[idx] + 1
                if pos == len(self.schema[variable]):
                    cycled = True
                    pos = 0
                cursors[idx] = pos
                # Get the new value and any sub-value generator associated with it
                val, gen = self.schema[variable][pos]
                # If there are sub-variables, store their generator and get the
                # first set of sub-variables.
                if gen:
                    gens[idx] = gen.configs()
                    piece = next(gens[idx])

            # At this point, val will have the correct value, regardless of whether
            # it was incremented or stayed the same because of sub-variables or
            # cycled. piece will either have sub-variables or be empty.
            piece[variable] = val
            # Swap out the old piece associated with this variable with the new piece
            config_pieces[idx] = piece
            
            return cycled
        
        # Fill config_pieces with initial pieces for each variable
        for i, var in enumerate(variables):
            increment(var, i)
        
        # If we've rolled over on the last element, we're done generating configs
        cycled_last_variable = False
        while not cycled_last_variable:
            # Create and yield the current config made from the config pieces
            yield {k:v for d in config_pieces for k,v in d.items()}
            
            # Gather new pieces of the config based on incrementing the cursors
            for i, var in enumerate(variables):
                cycled_last_variable = increment(var, i)
                if not cycled_last_variable:
                    break
    
    def __str__(self, indent=''):
        """
        Return a string representation of this schema.

        Args:
            indent: Optional string appended before all lines added by this schema.
        """
        
        # Use sorted list to enforce an order (useful for testing and readability)
        variables = sorted(self.schema.keys())

        # The plan here is to build up a list of lines in the string representation
        # then join them all with newlines in the end
        s = []
        
        # Add name of schema if it exists
        if self.name:
            s.append(str(self.name))
        
        # Add lines for each variable and its values
        for variable in variables:            
            # Add a line itemizing values without dependencies
            values = [str(pair[0]) for pair in self.schema[variable] if not pair[1]]
            if values:
                line = "{}{} = {}".format(indent, variable, ','.join(values))
                s.append(line)
            
            # Add values with dependencies
            values_with_deps = [pair for pair in self.schema[variable] if pair[1]]
            for value, dep in values_with_deps:
                line = "{}{} = {}".format(indent, variable, value)
                s.append(line)
                s.append(dep.__str__(indent + TAB))
            
        return '\n'.join(s)
        
    def write(self, filename):
        """
        Create a new genfile from a GenSchema.

        Args:
            filename: (str) Filename of the new genfile.
        """
        with open(filename, 'w') as f:
            f.write(str(self))
    
    @classmethod
    def read(cls, filename):
        """
        Factory method for creating a GenSchema from the contents of a file.
        
        Args:
            cls: Python class this method was called on, should always be GenSchema.
            filename: (str) Genfile to parse.
        """

        def create_schema(domains):
            """
            Create GenSchema filled with the given domains.

            See the GenParser for more specific information about what the domains parameter
            looks like.

            Args:
                domains: ParseResult containing domain definitions.
            Returns:
                New GenSchema object whose schema is filled with the domains.
            """
            schema = GenSchema()
            for domain in domains:
                ranges = []
                values = [v for v in domain['values'] if not isinstance(v, tuple) or ranges.append(v)]
                for range in ranges:
                    range_vals = [round(v, 5) for v in frange(*range)]
                    values.extend(range_vals)
                schema.add_values(domain['var'], *values)
                if 'deps' in domain:
                    deps = create_schema(domain['deps'])
                    for val in domain['values']:
                        schema.add_dependencies(domain['var'], val, deps)
            return schema

        # Parse the genfile using the GenParser
        parsed_schema = GenParser.parseFile(filename)

        # Create a GenSchema from the ParseResult object
        schema = create_schema(parsed_schema['schema'])

        # Set the name of the GenSchema if one is given
        if 'name' in parsed_schema:
            schema.name = parsed_schema['name']

        return schema
    
    
###############################################################################    
    
    
class GenParser(object):
    """Wrapper for a pyparsing parser object used to parse genfile syntax."""

    @staticmethod
    def parseString(s):
        """
        Parse a string describing a gen schema.

        Returns:
            ParseResults object that can be consumed in the GenSchema read function.
        """
        return GenParser._get_parser().parseString(s)

    @staticmethod
    def parseFile(f):
        """
        Parse a genfile.
        
        Returns:
            ParseResults object that can be consumed in the GenSchema read function.
        """
        return GenParser._get_parser().parseFile(f)

    @staticmethod
    def _get_parser():
        """
        Create parser for genfile using pyparsing library.
        
        Returns:
            Parser capable of turning a genfile into a consumable ParseResults object.
        """
        
        def strip_quotes(orig, loc, toks):
            """Strip quotation marks from the end of a string if present."""
            s = toks[0]
            if len(s) > 1:
                if (s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'"):
                    s = s[1:-1]
            return s
            
        ########## Define important literals ############
            
        pound = p.Literal("#")
        point = p.Literal(".")
        comma = p.Literal(",")
        e     = p.CaselessLiteral("E")
        colon = p.Literal(":").suppress()
        white = p.White(" \t\r")
        endl  = p.LineEnd().suppress()
        plus  = p.Literal("+")
        minus = p.Literal("-")
        nums  = p.Word(p.nums)
            
        ######### Define important constructs ###########
        
        # Define comment structure    
        comment = pound + p.restOfLine
            
        # non-quoted string
        non_quoted_token = p.Word(p.printables, excludeChars="#,")
        non_quoted_token += p.Optional(~endl + white + ~p.FollowedBy(comma|pound|endl))
        non_quoted = p.Combine(p.OneOrMore(non_quoted_token))
        
        # quoted string                        
        quote = (p.QuotedString('"', escChar="\\") | p.QuotedString("'", escChar="\\"))
        quote.addParseAction(strip_quotes)
        
        # integer
        integer = p.Word("+-"+p.nums, p.nums)
        integer.setParseAction( lambda s,l,t: int(t[0]) )
        
        # floating point number
        fpoint = p.Combine( p.Optional(plus|minus) + p.Optional(nums) +
                                point + nums + p.Optional( e + integer ) )
        fpoint.setParseAction( lambda s,l,t: float(t[0]) )
        
        # Any number
        number = (fpoint | integer)
        
        # range specification
        range_spec = number + colon + number + p.Optional(colon + number)
        range_spec.addParseAction( lambda s,l,t: [tuple(t)] )
        
        ######### Define grammar #########################
         
        # Indent stack needed for the pyparsing indentBlock function
        indent_stack = [1]
        # Statement used for recursive definition of genfile grammar
        stmt = p.Forward()
    
        # Variable names must start with a letter and can include
        # numbers, dashes, underscores, and periods.
        variable = p.Word(p.alphas, p.alphanums + "-_.")
        
        # Comma separated list of values
        value = (range_spec | number | quote | non_quoted)
        values = p.delimitedList(value)
    
        # Variable domain/scope:
        #       variable = val1, val2, val3 ...
        scope = variable("var") + p.Suppress("=") + p.Group(values)("values")
        
        # Dependencies are variable domains nested beneath another scope
        deps = p.indentedBlock(stmt, indent_stack)
        
        # A suite is a variable scope along with all of its dependencies
        suite = scope + p.Optional(deps("deps"))
        stmt << suite
        
        # A gen schema is one or more suites of variables
        genschema = p.OneOrMore(p.Group(suite))
        
        # A genfile starts with an optional schema name then defines a gen schema
        genfile = p.Optional(variable("name") + p.FollowedBy(p.lineEnd)) + genschema("schema")
        # Ignore comments in genfile
        genfile.ignore(comment)
        
        return genfile


