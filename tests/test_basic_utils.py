# -*- coding: utf-8 -*-
"""
Test the simple utility functions found in ctip/utils/basic_utils.py

Created on Sun Jul 10 01:41:17 2016

@author: Aaron Beckett
"""

import pytest
import sys
import math

def my_isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
    """
    Test if a and b are close enough to consider equal.
    
    This function is essentially the same as the math.isclose function which
    was added in Python 3.5 but is created here to increase compatibility across
    all Python 3 versions.
    """
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

if sys.version_info < (3, 5):
    isclose = math.isclose
else:
    isclose = my_isclose

from ctip.utils import frange
    
    
def lists_fequal(A, B):
    """Compare two lists using floating point equality with a tolerance.

    Args:
        A: List containing real numbers.
        B: Another list containing real numbers.
        tolerance: Maximum allowed difference between elements that are considered equal.
        
    Returns:
        True if every element in A is considered equal to its cooresponding element in B.
    """
    
    if len(A) != len(B):
        return False
        
    return all([isclose(i,j) for i,j in zip(A,B)])


class TestFrange(object):
    """Tests for the frange function."""
    
    smol = [0, 1e-9, 2e-9, 3e-9, 4e-9, 5e-9, 6e-9, 7e-9, 8e-9, 9e-9, 1e-8]
    
    def test_frange_from_zero(self):
        """Test frange with start value of 0."""
        
        assert [0, 1, 2] == list(frange(2))
        assert list(frange(2)) == list(frange(0, 2))
        assert list(frange(2)) == list(frange(0, 2.0))
        assert lists_fequal([0, 0.5, 1, 1.5, 2], list(frange(2, inc=0.5)))
        assert lists_fequal([0, 0.5, 1, 1.5, 2], list(frange(2.2, inc=0.5)))
        
    def test_frange_to_zero(self):
        """Test frange with end value of 0."""
        
        assert [-2, -1, 0] == list(frange(-2, 0))
        assert list(frange(-2, 0)) == list(frange(-2))
        assert list(frange(-2, 0)) == list(frange(-2.0))
        assert lists_fequal([-2, -1.5, -1, -0.5, 0], list(frange(-2, inc=0.5)))
        assert lists_fequal([-2, -1.4, -0.8, -0.2], list(frange(-2, inc=0.6)))
        
    def test_frange_negative_increment(self):
        """Test frange with negative increments."""
        
        assert lists_fequal([1, 0.5, 0, -0.5, -1], list(frange(1, -1, -0.5)))
        assert lists_fequal([100, 99.7, 99.4, 99.1], list(frange(100, 99, -0.3)))
        assert lists_fequal([-4.65, -5, -5.35, -5.7, -6.05], list(frange(-4.65, -6.1, -0.35)))
        assert lists_fequal([1, 0.75, 0.5, 0.25, 0], list(frange(1, inc=-0.25)))
        assert lists_fequal([0, -0.2, -0.4], list(frange(-0.5, inc=-0.2)))
    
    def test_frange_swapped_start_end(self):
        """Test flexible order of frange bounds."""
        
        assert [5, 7, 9, 11] == list(frange(5, 11, 2))
        assert [5, 7, 9, 11] == list(frange(11, 5, 2))
        assert [11, 9, 7, 5] == list(frange(5, 11, -2))
        assert [11, 9, 7, 5] == list(frange(11, 5, -2))
    
    def test_frange_identical_bounds(self):
        """Test frange with identical bounds."""
        
        assert [0] == list(frange(0))
        assert [77.7] == list(frange(77.7, 77.7, inc=1e-5))
        
    def test_frange_invalid_increment(self):
        """Test frange with invalid increments."""
        
        with pytest.raises(ValueError):
            next(frange(5, inc=0))
            
        with pytest.raises(ValueError):
            next(frange(77.7, 77.7, inc=1e-35))
            
    def test_frange_small_increments(self):
        """Test frange using very small increments."""
        
        assert lists_fequal(self.smol, list(frange(1e-8, inc=1e-9)))
        assert lists_fequal(self.smol, list(frange(1.05e-8, inc=1e-9)))
        assert lists_fequal(self.smol[::-1], list(frange(1e-8, inc=-1e-9)))
            