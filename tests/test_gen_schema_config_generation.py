# -*- coding: utf-8 -*-
"""
Tests for generation of all valid configs defined by a genfile schema.

Created on Sun Jul 10 19:59:26 2016

@author: Aaron Beckett
"""


import pytest
import json

from ctip import GenSchema
    

def test_single_var_single_arg():
    """Test gen schema containing one variable with one argument."""
    
    configs = json.load(open("tests/resources/configs1.json"))
    
    schema = GenSchema()
    schema.add_values("type", "long")
    
    pytest.helpers.compare_configs(configs, schema)

def test_single_var_multiple_args():
    """Test gen schema containing one variable with multiple arguments."""
    
    configs = json.load(open("tests/resources/configs2.json"))
    
    schema = GenSchema()
    schema.add_values("type", "long", "recurve")

    pytest.helpers.compare_configs(configs, schema)

def test_multiple_vars():
    """Test gen schema containing multiple variables."""
    
    configs = json.load(open("tests/resources/configs3.json"))
    
    schema = GenSchema()
    schema.add_values("type", "long", "recurve")
    schema.add_values("wood", "osage orange", "yew", "oak", "hickory")

    pytest.helpers.compare_configs(configs, schema)
   
def test_simple_nested_gen():
    """Test gen schema containing nested arguments on preconstructed variables."""
    
    configs = json.load(open("tests/resources/configs4.json"))
    
    schema = GenSchema()
    schema.add_values("type", "long", "recurve")
    long_dep = GenSchema()
    long_dep.add_values("length", 66, 72)
    schema.add_dependencies("type", "long", long_dep)
    recurve_dep = GenSchema()
    recurve_dep.add_values("length", 42, 46)
    schema.add_dependencies("type", "recurve", recurve_dep)

    pytest.helpers.compare_configs(configs, schema)
    
def test_multiple_vars_in_nested_gen():
    """Test gen schema containing multiple variables in a nested schema."""
    
    configs = json.load(open("tests/resources/configs6.json"))
    
    schema = GenSchema()
    schema.add_values("type", "long", "recurve")
    long_dep = GenSchema()
    long_dep.add_values("length", 42, 46)
    long_dep.add_values("wood", "osage orange", "yew")
    schema.add_dependencies("type", "long", long_dep)
    recurve_dep = GenSchema()
    recurve_dep.add_values("length", 66, 72)
    recurve_dep.add_values("wood", "hickory")
    schema.add_dependencies("type", "recurve", recurve_dep)

    pytest.helpers.compare_configs(configs, schema)
    
def test_incomplete_nested_gen():
    """Test gen schema with nested schema on only one arg of a multi-arg variable."""
    
    configs = json.load(open("tests/resources/configs7.json"))
    
    schema = GenSchema()
    schema.add_values("type", "long", "recurve")
    long_dep = GenSchema()
    long_dep.add_values("primitive", "yes", "no")
    schema.add_dependencies("type", "long", long_dep)

    pytest.helpers.compare_configs(configs, schema)
    
def test_multiple_nests():
    """Test gen schema with nested schemas under multiple variables."""
    
    configs = json.load(open("tests/resources/configs8.json"))
    
    schema = GenSchema()
    schema.add_values("type", "long", "recurve")
    schema.add_values("pokemon_type", "water", "fire")
    
    long_dep = GenSchema()
    long_dep.add_values("length", 66, 70)
    schema.add_dependencies("type", "long", long_dep)
    
    recurve_dep = GenSchema()
    recurve_dep.add_values("length", 44, 45)
    schema.add_dependencies("type", "recurve", recurve_dep)
    
    water_dep = GenSchema()
    water_dep.add_values("name", "Squirtle", "Lapras")
    schema.add_dependencies("pokemon_type", "water", water_dep)
    
    fire_dep = GenSchema()
    fire_dep.add_values("name", "Charmander", "Vulpix")
    schema.add_dependencies("pokemon_type", "fire", fire_dep)

    pytest.helpers.compare_configs(configs, schema)
    
def test_multi_nested():
    """Test gen schema with multiple levels of nexting under one argument."""
    
    configs = json.load(open("tests/resources/configs9.json"))
    
    schema = GenSchema()
    schema.add_values("decoder", "Hypercube")
    
    gates = GenSchema()
    gates.add_values("gates", 12, 15)
    
    c1 = GenSchema()
    c1.add_values("complexity", 2, 3)
    
    l1 = GenSchema()
    l1.add_values("length", 80)
    c1.add_dependencies("complexity", 2, l1)
    
    l2 = GenSchema()
    l2.add_values("length", 110)
    c1.add_dependencies("complexity", 3, l2)
    
    c2 = GenSchema()
    c2.add_values("complexity", 2, 3)
    
    l3 = GenSchema()
    l3.add_values("length", 116)
    c2.add_dependencies("complexity", 2, l3)
    
    l4 = GenSchema()
    l4.add_values("length", 140, 158)
    c2.add_dependencies("complexity", 3, l4)
    
    gates.add_dependencies("gates", 12, c1)
    gates.add_dependencies("gates", 15, c2)
    
    schema.add_dependencies("decoder", "Hypercube", gates)

    pytest.helpers.compare_configs(configs, schema)

    