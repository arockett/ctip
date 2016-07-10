# -*- coding: utf-8 -*-
"""
Test the GenSchema API.

Created on Sun Jul 10 14:32:01 2016

@author: Aaron Beckett
"""


import pytest

from ctip.utils import GenSchema


class TestGenSchemaCreation(object):
    """Tests for GenSchema API."""
    
    def test_construction(self):
        """Test GenSchema constructor."""
        
        gen = GenSchema()
        assert gen.schema == {}
        
    def test_add_invalid_values(self):
        """Test error detection when adding variables and values to a schema."""
        
        gen = GenSchema()
        with pytest.raises(TypeError): gen.add_values([], 1)
        with pytest.raises(TypeError): gen.add_values({}, 1)
        with pytest.raises(TypeError): gen.add_values(set(), 1)
        with pytest.raises(TypeError): gen.add_values((), 1)
        with pytest.raises(TypeError): gen.add_values(1, [])
        with pytest.raises(TypeError): gen.add_values(1, {})
        with pytest.raises(TypeError): gen.add_values(1, set())
        with pytest.raises(TypeError): gen.add_values(1, ())
        with pytest.raises(TypeError): gen.add_values(1)
    
    def test_add_values(self):
        """Test ability to add values to a variable's list of valid values."""
        
        gen = GenSchema()
        
        # Inital variable creation
        gen.add_values("var1", 1, 2)
        assert "var1" in gen.schema
        assert gen.schema["var1"] == [(1,[]), (2,[])]
        
        # Add another value to an already created variable
        gen.add_values("var1", 3)
        assert gen.schema["var1"] == [(1,[]), (2,[]), (3,[])]
        
        # Add multiple new values to an aready created variable
        gen.add_values("var1", 4, 5, 6)
        assert gen.schema["var1"] == [(1,[]), (2,[]), (3,[]), (4,[]), (5,[]), (6,[])]
        
        # Add a duplicate value to an already created variable
        gen.add_values("var1", 2)
        assert gen.schema["var1"] == [(1,[]), (2,[]), (3,[]), (4,[]), (5,[]), (6,[]), (2,[])]
        
        # Add a new variable
        gen.add_values("var2", 2, 3, 1, 1)
        assert len(gen.schema) == 2
        assert len(gen.schema["var1"]) == 7
        assert len(gen.schema["var2"]) == 4
        
    def test_add_dependency_to_non_existent_variable(self):
        """Ensure dependencies can't be added to variables that don't exist."""
        
        gen = GenSchema()
        with pytest.raises(KeyError):
            gen.add_dependencies("var1", "val1", GenSchema())
            
    def test_add_dependency_to_non_existent_value(self):
        """Ensure dependencies can't be added to values that don't exist."""
        
        gen = GenSchema()
        gen.add_values("var1", "val1")
        with pytest.raises(ValueError):
            gen.add_dependencies("var1", "val2", GenSchema())
        
    def test_add_invalid_dependencies(self):
        """Test TypeError detection when adding dependencies to a schema."""
        
        gen = GenSchema()
        gen.add_values("var1", 1)
        with pytest.raises(TypeError): gen.add_dependencies("var1", 1, 1)
        with pytest.raises(TypeError): gen.add_dependencies("var1", 1, "bad")
        with pytest.raises(TypeError): gen.add_dependencies("var1", 1, [])        
        with pytest.raises(TypeError): gen.add_dependencies("var1", 1, {})        
        with pytest.raises(TypeError): gen.add_dependencies("var1", 1, ())        
        with pytest.raises(TypeError): gen.add_dependencies("var1", 1, set())
        with pytest.raises(TypeError): gen.add_dependencies("var1", 1)        
        
    def test_add_dependencies(self):
        """Test ability to tie a dependency to a specific value."""
        
        gen = GenSchema()
        
        # Add dependency to existing value of existing variable
        gen.add_values("var1", "val1")
        gen.add_dependencies("var1", "val1", GenSchema())
        assert len(gen.schema["var1"]) == 1
        binding = gen.schema["var1"][0]
        assert binding[0] == "val1"
        assert isinstance(binding[1][0], GenSchema)
        
        # Add dependency to integer value
        gen.add_values("var1", 1, 2)
        with pytest.raises(ValueError):
            gen.add_dependencies("var1", "2", GenSchema())
        gen.add_dependencies("var1", 2, GenSchema())
        assert len(gen.schema["var1"][2][1]) == 1
        
        # Add multiple dependencies to same value
        gen.add_values("var2", 1, 3, 2)
        gen.add_dependencies("var2", 3, GenSchema(), GenSchema())
        assert len(gen.schema["var2"]) == 3
        binding = gen.schema["var2"][1]
        assert binding[0] == 3
        assert len(binding[1]) == 2
        assert isinstance(binding[1][0], GenSchema)
        assert isinstance(binding[1][1], GenSchema)

