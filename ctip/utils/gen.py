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
                'val2.1',
                [
                    'val2.2',
                    {
                        'dependent1': ['dval1.1', 'dval1.2'],
                        'dependent2': ['dval2.1']
                    }
                ],
                'val2.3'
            ]
        }
        
    Notice how the dependents tied to 'val2.2' really just define a nested
    gen schema which is linked to 'val2.2'.
    """
    
    def __init__(self):
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
    
    def __iter__(self):
        return self
        
    def __next__(self):
        pass
    
    def __str__(self):
        pass
        
    def write_to_file(self, filename):
        """Create a new genfile from a GenSchema."""
        pass
    
    @classmethod
    def build_from_file(cls, filename):
        """Factory method for creating a GenSchema from the contents of a file."""
        pass
