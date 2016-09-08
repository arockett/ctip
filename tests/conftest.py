# -*- coding: utf-8 -*-
"""
Configuration file for the main ctip test suite.

Created on Sat Jul  9 23:48:43 2016

@author: Aaron Beckett
"""

import sys, os
import pytest

sys.path.append(os.path.join(os.getcwd(), '.'))
sys.path.append(os.path.join(os.getcwd(), '..'))


pytest_plugins = ['helpers_namespace']


########### Fixtures ################


########### Helper funcs ##############

@pytest.helpers.register
def compare_configs(configs, schema):
    """Compare configs generated by a schema with a list of configs."""

    # Define error messages
    incorrect_length = "Incorrect number of configs generated: {} != {}"
    incorrect_values = "Incorrect config values"

    generated = schema.configs()

    i = 0
    try:
        while True:
            config = next(generated)
            i += 1

            if not configs:
                pytest.fail(incorrect_length.format(i, i - 1))

            for i in range(len(configs)):
                if configs[i] == config:
                    del configs[i]
                    break
            else:
                pytest.fail(incorrect_values)

    except StopIteration:
        if configs:
            pytest.fail(incorrect_length.format(i, i + len(configs)))