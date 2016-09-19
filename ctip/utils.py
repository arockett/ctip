# -*- coding: utf-8 -*-
"""
Created on Sun Jul 10 10:25:42 2016

@author: Aaron Beckett
"""

import sqlite3 as sql


class DBConn(object):

    def __init__(self, dbpath):
        self.conn = sql.connect(dbpath)
        self.conn.row_factory = sql.Row

    def __del__(self):
        self.conn.close()


def frange(a, b = 0, inc = 1):
    """Generate sequence of values between a and b inclusive.
    
    The order of a and b does not matter, only the sign of the increment is
    needed to determine the start and end values of the sequence. If inc is
    positive the starting value will be the smaller of a and b. If inc is
    negative the starting value will be the larger of a and b.
    
    The sequence ends when the next value would be larger or smaller than the
    end value (depending on direction) and NOT if the next value would equal
    the end value. This is different from Python's built-in range function
    which uses exclusive upper bounds.
    
    Args:
        a: Either the upper or lower bound.
        b: Optional second bound, defaults to 0.
        inc: incremental difference between consecutive values, defaults to 1.

    Yields:
        The next number in the sequence.

    Raises:
        StopIteration: There are no more values in the sequence.
        ValueError: The increment provided was 0.
    """
    
    if inc == 0:
        raise ValueError("Increment cannot be 0.")
    elif a + inc == a:
        raise ValueError("Increment is too small.")
        
    start = min(a,b) if inc > 0 else max(a,b)
    end = max(a,b) if inc > 0 else min(a,b)
    
    i = 0
    nextval = start
    while (inc > 0 and nextval <= end) or (inc < 0 and nextval >= end):
        yield nextval
        i += 1
        nextval = start + inc*i
