#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Convenience wrapper for running ctip directly from the root project directory.

Created on Sat Jul  9 16:42:47 2016

@author: Aaron Beckett
"""

import sys
from ctip.entrypoint import main

if __name__ == '__main__':
    main(sys.argv)