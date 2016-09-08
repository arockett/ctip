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

    resource_dir = "tests" + os.path.sep + "resources" + os.path.sep

    genfile_config_pairs = []
    for (dirpath, dirnames, filenames) in os.walk(resource_dir):
        for name in filenames:
            if name.startswith("genfile"):
                cfg_name = name.split("_")[0].replace("genfile", "configs") + ".json"
                pair = (resource_dir + name, resource_dir + cfg_name)
                genfile_config_pairs.append(pair)
        break
    return genfile_config_pairs


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


