# -*- coding: utf-8 -*-
"""
Created on Sat Sep 17  9:07:17 2016

@author: Aaron Beckett
"""

import sqlite3 as sql


class DatabaseManager(object):
    """Handles interactions with the local SQLite Database used by ctip."""

    dbname = "C:\\Users\\aminor\\Dev\\ctip\\ctip.db"
    reserved_table_names = ['sessions', 'jobs']

    def __init__(self):
        self.conn = sql.connect(self.dbname)
        self.conn.row_factory = sql.Row
        self.conn.executescript("""
                CREATE TABLE IF NOT EXISTS sessions(
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    exp TEXT,
                    genfile TEXT,
                    where_clause TEXT,
                    env TEXT,
                    date TEXT
                );
                CREATE TABLE IF NOT EXISTS jobs(
                    session_id INT,
                    config_id INT,
                    job_id TEXT,
                    status TEXT,
                    time_log TEXT,
                    runtime TEXT,
                    PRIMARY KEY (session_id, job_id)
                );
            """)

    def __del__(self):
        self.conn.close()