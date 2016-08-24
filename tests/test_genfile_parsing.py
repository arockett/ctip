# -*- coding: utf-8 -*-
"""
Created on Sun Aug 21 22:11:38 2016

@author: amino
"""


import pytest

from ctip import GenParser


def test_single_var_single_val():
    result = GenParser.parseFile("tests/resources/genfile1_single_var_single_arg.gen")
    assert result["name"] == "bows"
    assert len(result["schema"]) == 1
    domain = result["schema"][0]
    assert domain["var"] == "type"
    assert len(domain["values"]) == 1
    assert domain["values"][0] == "long"
    assert "deps" not in domain

def test_no_name():
    result = GenParser.parseString("type = long")
    assert "name" not in result
    assert "schema" in result

def test_single_var_multiple_vals():
    result = GenParser.parseFile("tests/resources/genfile2_single_var_multiple_args.gen")
    assert result["name"] == "bows"
    assert len(result["schema"]) == 1
    domain = result["schema"][0]
    assert domain["var"] == "type"
    assert len(domain["values"]) == 2
    assert domain["values"][0] == "long"
    assert domain["values"][1] == "recurve"
    assert "deps" not in domain
    
def test_special_chars():
    result = GenParser.parseString("name7_with.special-chars = val1, val2")
    assert result["schema"][0]["var"] == "name7_with.special-chars"
    
def test_quoted_values():
    result = GenParser.parseString("variable = 'val1', \"#alwaystraining\", 'comma,string' # comment")
    domain = result["schema"][0]
    assert len(domain["values"]) == 3
    assert domain["values"].asList() == ["val1", "#alwaystraining", "comma,string"]
    
    result = GenParser.parseString("var = '{}',\"{}\"".format("\'", '\"'))
    assert result["schema"][0]["values"].asList() == ["'", '"']

def test_multiple_vars():
    result = GenParser.parseFile("tests/resources/genfile3_multiple_vars.gen")
    assert result["name"] == "bows"
    assert len(result["schema"]) == 2
    
    domain = result["schema"][0]
    assert domain["var"] == "type"
    assert len(domain["values"]) == 2
    assert domain["values"][0] == "long"
    assert domain["values"][1] == "recurve"
    assert "deps" not in domain
    
    domain = result["schema"][1]
    assert domain["var"] == "wood"
    assert len(domain["values"]) == 4
    assert domain["values"].asList() == ["osage orange", "yew", "oak", "hickory"]
    assert "deps" not in domain
    
def test_simple_nested_preconstructed_args():
    result = GenParser.parseFile("tests/resources/genfile4_simple_nested_preconstructed_args.gen")
    assert result["name"] == "bows"
    assert len(result["schema"]) == 3
    
    domain = result["schema"][0]
    assert domain["var"] == "type"
    assert len(domain["values"]) == 2
    assert domain["values"][0] == "long"
    assert domain["values"][1] == "recurve"
    assert "deps" not in domain
    
    domain = result["schema"][1]
    assert domain["var"] == "type"
    assert len(domain["values"]) == 1
    assert domain["values"][0] == "long"
    assert len(domain["deps"]) == 1
    dep = domain["deps"][0]
    assert dep["var"] == "length"
    assert dep["values"].asList() == ['66', '72']
    assert "deps" not in dep
    
    domain = result["schema"][2]
    assert domain["var"] == "type"
    assert len(domain["values"]) == 1
    assert domain["values"][0] == "recurve"
    assert len(domain["deps"]) == 1
    dep = domain["deps"][0]
    assert dep["var"] == "length"
    assert dep["values"].asList() == ['42', '46']
    assert "deps" not in dep
    
def test_multiple_vars_in_nest():
    result = GenParser.parseFile("tests/resources/genfile6_multiple_vars_in_nest.gen")
    assert result["name"] == "bows"
    assert len(result["schema"]) == 2
    
    domain = result["schema"][0]
    assert domain["var"] == "type"
    assert domain["values"].asList() == ["long"]
    deps = domain["deps"]
    assert len(deps) == 2
    
    assert deps[0]["var"] == "length"
    assert deps[0]["values"].asList() == ['42','46']
    assert "deps" not in deps[0]
    assert deps[1]["var"] == "wood"
    assert deps[1]["values"].asList() == ['osage orange','yew']
    assert "deps" not in deps[1] 
    
    domain = result["schema"][1]
    assert domain["var"] == "type"
    assert domain["values"].asList() == ["recurve"]
    deps = domain["deps"]
    assert len(deps) == 2
    
    assert deps[0]["var"] == "length"
    assert deps[0]["values"].asList() == ['66','72']
    assert "deps" not in deps[0]
    assert deps[1]["var"] == "wood"
    assert deps[1]["values"].asList() == ['hickory']
    assert "deps" not in deps[1] 
    
def test_multi_nested():
    result = GenParser.parseFile("tests/resources/genfile9_multi_nested.gen")
    assert result["name"] == "p3"
    assert len(result["schema"]) == 1
    
    domain = result["schema"][0]
    assert domain["var"] == "decoder"
    assert domain["values"].asList() == ["Hypercube"]
    deps = domain["deps"]
    assert len(deps) == 2
    
    assert deps[0]["var"] == "gates"
    assert deps[0]["values"].asList() == ['12']
    deps2 = deps[0]["deps"]
    assert len(deps2) == 2
    
    assert deps2[0]["var"] == "complexity"
    assert deps2[0]["values"].asList() == ['2']
    deps3 = deps2[0]["deps"]
    assert len(deps3) == 1
    
    assert deps3[0]["var"] == "length"
    assert deps3[0]["values"].asList() == ['80']
    assert "deps" not in deps3[0]
    
    assert deps2[1]["var"] == "complexity"
    assert deps2[1]["values"].asList() == ['3']
    deps3 = deps2[1]["deps"]
    assert len(deps3) == 1
    
    assert deps3[0]["var"] == "length"
    assert deps3[0]["values"].asList() == ['110']
    assert "deps" not in deps3[0]
    
    assert deps[1]["var"] == "gates"
    assert deps[1]["values"].asList() == ['15']
    deps2 = deps[1]["deps"]
    assert len(deps2) == 2
    
    assert deps2[0]["var"] == "complexity"
    assert deps2[0]["values"].asList() == ['2']
    deps3 = deps2[0]["deps"]
    assert len(deps3) == 1
    
    assert deps3[0]["var"] == "length"
    assert deps3[0]["values"].asList() == ['116']
    assert "deps" not in deps3[0]
    
    assert deps2[1]["var"] == "complexity"
    assert deps2[1]["values"].asList() == ['3']
    deps3 = deps2[1]["deps"]
    assert len(deps3) == 1
    
    assert deps3[0]["var"] == "length"
    assert deps3[0]["values"].asList() == ['140', '158']
    assert "deps" not in deps3[0]
    
def test_multiple_vars_own_nest():
    result = GenParser.parseFile("tests/resources/genfile10_multiple_vars_own_nest.gen")
    assert result["name"] == "locations"
    assert len(result["schema"]) == 1
    
    domain = result["schema"][0]
    assert domain["var"] == "city"
    assert domain["values"].asList() == ["East Lansing", "Lansing", "Okemos"]
    deps = domain["deps"]
    assert len(deps) == 3
    
    assert deps[0]["var"] == "county"
    assert deps[0]["values"].asList() == ["Ingham"]
    assert "deps" not in deps[0]
    assert deps[1]["var"] == "state"
    assert deps[1]["values"].asList() == ["Michigan"]
    assert "deps" not in deps[1]
    assert deps[2]["var"] == "country"
    assert deps[2]["values"].asList() == ["United States"]
    assert "deps" not in deps[2]
    
@pytest.mark.skip
def test_commented():
    result = GenParser.parseFile("tests/resources/genfile11_commented.gen")
    assert result["name"] == "p3"
    assert len(result["schema"]) == 3
    
    domain = result["schema"][0]
    assert domain["var"] == "decoder"
    assert domain["values"].asList() == ["Hypercube", "Unstructured", "FixedLogic", "FixedInputs"]
    assert "deps" not in domain
    
    domain = result["schema"][1]
    assert domain["var"] == "decoder"
    assert domain["values"].asList() == ["Hypercube"]
    deps = domain["deps"]
    assert len(deps) == 2
    
    assert deps[0]["var"] == "complexity"
    assert deps[0]["values"].asList() == ['2']
    deps2 = deps[0]["deps"]
    assert len(deps2) == 1
    
    assert deps2[0]["var"] == "gates"
    assert deps2[0]["values"].asList() == ['12', '15']
    assert "deps" not in deps2[0]
    
    assert deps[1]["var"] == "complexity"
    assert deps[1]["values"].asList() == ['3']
    deps2 = deps[1]["deps"]
    assert len(deps2) == 1
    
    assert deps2[0]["var"] == "gates"
    assert deps2[0]["values"].asList() == ['8', '11']
    assert "deps" not in deps2[0]
    
    domain = result["schema"][2]
    assert domain["var"] == "decoder"
    assert domain["values"].asList() == ["Unstructured"]
    deps = domain["deps"]
    assert len(deps) == 1
    
    assert deps[0]["var"] == "complexity"
    assert deps[0]["values"].asList() == ['2', '3']
    assert "deps" not in deps[0]
    