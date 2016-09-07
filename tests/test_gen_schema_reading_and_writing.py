# -*- coding: utf-8 -*-
"""
Test parsing genfiles and writing GenSchema to genfiles.

Created on Sun Jul 10 19:54:47 2016

@author: Aaron Beckett
"""


import pytest
import json
import os

from ctip import GenSchema


def gather_test_files():
    """Search the tests/resources directory for pairs of gen and config files."""
    return [
        ("tests/resources/genfile1_single_var_single_arg.gen", "tests/resources/configs1.json"),
        ("tests/resources/genfile2_single_var_multiple_args.gen", "tests/resources/configs2.json"),
        ("tests/resources/genfile3_multiple_vars.gen", "tests/resources/configs3.json"),
        ("tests/resources/genfile4_simple_nested_preconstructed_args.gen", "tests/resources/configs4.json"),
        ("tests/resources/genfile5_simple_nested.gen", "tests/resources/configs5.json"),
        ("tests/resources/genfile6_multiple_vars_in_nest.gen", "tests/resources/configs6.json"),
        ("tests/resources/genfile7_incomplete_nested.gen", "tests/resources/configs7.json"),
        ("tests/resources/genfile8_multiple_nests.gen", "tests/resources/configs8.json"),
        ("tests/resources/genfile9_multi_nested.gen", "tests/resources/configs9.json"),
        ("tests/resources/genfile10_multiple_vars_own_nest.gen", "tests/resources/configs10.json"),
        ("tests/resources/genfile11_commented.gen", "tests/resources/configs11.json")
    ]


@pytest.mark.parametrize("genfile,config_file", gather_test_files())
def test_gen_schema_read(genfile, config_file):
    """Test the Genfile read method with all examples in test/resources."""
    schema = GenSchema.read(genfile)
    configs = json.load(open(config_file))

    pytest.helpers.compare_configs(configs, schema)


@pytest.mark.parametrize("genfile,config_file", gather_test_files())
def test_gen_schema_write(genfile, config_file, tmpdir):
    """Test the Genfile write method with all examples in test/resources."""
    tmp_genfile = str(tmpdir.join(os.path.basename(genfile)))
    configs = json.load(open(config_file))

    schema = GenSchema.read(genfile)
    schema.write(tmp_genfile)
    schema = GenSchema.read(tmp_genfile)

    pytest.helpers.compare_configs(configs, schema)


