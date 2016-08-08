# -*- coding: utf-8 -*-
"""
Define objects for handling genfile reading, writing, and iteration.

Created on Sun Jul 10 14:48:26 2016

@author: Aaron Beckett
"""


class GenSchema(object):
    """Object representation of a gen schema.
    
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
            'variable1': ['val1.1', 'val1.2'],
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
        self.name = name
        self.schema = {}
    
    def add_values(self, variable, *values):
        """Add values to a variable's list of valid values.

        If the variable doesn't exist, it is created. Variables and values can
        be any immutable datatype besides a tuple.
        """
        
        def valid_type(v):
            return type(v) == str or type(v) == int or type(v) == float
            
        if not values:
            raise TypeError("Must provide at least one value to add_values()")
            
        if not valid_type(variable) or not all([valid_type(v) for v in values]):
            raise TypeError("Gen schema variables and values must strings, ints, or floats")
            
        values = [(v,None) for v in values]
        if variable not in self.schema:
            self.schema[variable] = values
        else:
            self.schema[variable].extend(values)
    
    def add_dependencies(self, variable, value, *dependencies):
        """Bind dependent gen schemas to a particular value of a variable.

        The variable and value must already exist and dependencies must be
        a GenSchema.        
        """
        
        if not dependencies:
            raise TypeError("Must provide at least one dependency to add_dependencies()")
            
        if not all([isinstance(d, GenSchema) for d in dependencies]):
            raise TypeError("Dependencies must be of type GenSchema")
            
        try:
            args = self.schema[variable]
        except KeyError as e:
            raise KeyError("{} does not exist in the gen schema".format(variable)) from e
        
        indices = [i for i,arg in enumerate(args) if arg[0] == value]
        if not indices:
            raise ValueError("{} is not a valid argument for {}".format(value,variable))
            
        for i in indices:
            if args[i][1] is None:
                args[i] = (args[i][0], GenSchema())
            for dep in dependencies:
                args[i][1].schema.update(dep.schema)
    
    def configs(self):
        """Generate configurations represented by the schema."""
        
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
                idx: Index of the variable in the order.
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
    
    def __str__(self):
        """Return a string representation of this schema."""
        pass
        
    def write_to_file(self, filename):
        """Create a new genfile from a GenSchema."""
        pass
    
    @classmethod
    def build_from_file(cls, filename):
        """Factory method for creating a GenSchema from the contents of a file."""
        pass
