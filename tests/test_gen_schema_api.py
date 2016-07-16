# -*- coding: utf-8 -*-
"""
Test the GenSchema API.

Created on Sun Jul 10 14:32:01 2016

@author: Aaron Beckett
"""


import pytest

from ctip.utils import GenSchema


def test_construction():
    """Test GenSchema constructor."""
    
    gen = GenSchema()
    assert gen.name is None
    assert gen.schema == {}
    
    gen = GenSchema("schema_name")
    assert gen.name == "schema_name"
    assert gen.schema == {}
    
def test_add_invalid_values():
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

def test_add_values():
    """Test ability to add values to a variable's list of valid values."""
    
    gen = GenSchema()
    
    # Inital variable creation
    gen.add_values("var1", 1, 2)
    assert "var1" in gen.schema
    assert gen.schema["var1"] == [(1,None), (2,None)]
    
    # Add another value to an already created variable
    gen.add_values("var1", 3)
    assert gen.schema["var1"] == [(1,None), (2,None), (3,None)]
    
    # Add multiple new values to an aready created variable
    gen.add_values("var1", 4, 5, 6)
    assert gen.schema["var1"] == [(1,None), (2,None), (3,None), (4,None), (5,None), (6,None)]
    
    # Add a duplicate value to an already created variable
    gen.add_values("var1", 2)
    assert gen.schema["var1"] == [(1,None), (2,None), (3,None), (4,None), (5,None), (6,None), (2,None)]
    
    # Add a new variable
    gen.add_values("var2", 2, 3, 1, 1)
    assert len(gen.schema) == 2
    assert len(gen.schema["var1"]) == 7
    assert len(gen.schema["var2"]) == 4
    
def test_add_dependency_to_non_existent_variable():
    """Ensure dependencies can't be added to variables that don't exist."""
    
    gen = GenSchema()
    with pytest.raises(KeyError):
        gen.add_dependencies("var1", "val1", GenSchema())
        
def test_add_dependency_to_non_existent_value():
    """Ensure dependencies can't be added to values that don't exist."""
    
    gen = GenSchema()
    gen.add_values("var1", "val1")
    with pytest.raises(ValueError):
        gen.add_dependencies("var1", "val2", GenSchema())
    
def test_add_invalid_dependencies():
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
    
def test_add_dependencies():
    """Test ability to tie a dependency to a specific value."""
    
    gen = GenSchema()
    
    # Add dependency to existing value of existing variable
    gen.add_values("var1", "val1")
    gen.add_dependencies("var1", "val1", GenSchema())
    assert len(gen.schema["var1"]) == 1
    binding = gen.schema["var1"][0]
    assert binding[0] == "val1"
    assert isinstance(binding[1], GenSchema)
    
    # Add dependency to integer value
    gen.add_values("var1", 1, 2)
    dep1 = GenSchema()
    dep1.add_values("one", 'a', 'b')
    dep1.add_values("num", 11.1, 34.2)
    with pytest.raises(ValueError):
        gen.add_dependencies("var1", "2", dep1)
    gen.add_dependencies("var1", 2, dep1)
    assert isinstance(gen.schema["var1"][2][1], GenSchema)
    assert len(gen.schema["var1"][2][1].schema) == 2
    
    # Add another dependency to the same arg
    dep2 = GenSchema()
    dep2.add_values("two", 100, 200)
    gen.add_dependencies("var1", 2, dep2)
    assert isinstance(gen.schema["var1"][2][1], GenSchema)
    assert len(gen.schema["var1"][2][1].schema) == 3
    
    # Add multiple dependencies to same value
    gen.add_values("var2", 1, 3, 2)
    gen.add_dependencies("var2", 3, dep1, dep2)
    assert len(gen.schema["var2"]) == 3
    binding = gen.schema["var2"][1]
    assert binding[0] == 3
    assert isinstance(binding[1], GenSchema)
    assert len(binding[1].schema) == 3

