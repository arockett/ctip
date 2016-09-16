# -*- coding: utf-8 -*-
"""
Provides entry point main(argv) when running from the command line.

Created on Sat Jul  9 12:45:39 2016

@author: Aaron Beckett
"""

import os
import argparse

import ctip.commands as cmd

# Version information (parsed by setup.py
__version__ = "0.1.1"

# Get help text from file in docs folder
with open("docs" + os.path.sep + "help_message.txt") as f:
    help_text = f.read()


def main(argv):

    # If the user just runs 'ctip' then print the help message
    if (len(argv) == 1):
        print(help_text)
        exit(0)

    # Create the command line parser
    parser = create_cli_parser()

    # Parse the command line arguments with the parser
    args = parser.parse_args(argv[1:])

    # Call the correct function
    args.func(args)


def create_cli_parser():
    """Create CTIP ArgumentParser."""
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers()
    parser_run = subparsers.add_parser('run')
    parser_check = subparsers.add_parser('check')
    parser_stop = subparsers.add_parser('stop')
    parser_clean = subparsers.add_parser('clean')
    parser_set = subparsers.add_parser('set')
    parser_env = subparsers.add_parser('env')
    parser_tables = subparsers.add_parser('tables')
    parser_list = subparsers.add_parser('list')
    parser_update = subparsers.add_parser('update')
    parser_log = subparsers.add_parser('log')

    # run
    parser_run.add_argument('experiment')
    parser_run.add_argument('-f', '--genfile', required=True)
    parser_run.add_argument('-n', '--name', required=True)
    parser_run.add_argument('-e', '--env')
    parser_run.set_defaults(func=cmd.run)

    # check
    parser_check.add_argument('session_id', type=int, nargs='?')
    parser_check.set_defaults(func=cmd.check)

    # stop
    parser_stop.add_argument('session_id', type=int, nargs='?')
    parser_stop.set_defaults(func=cmd.stop)

    # clean
    parser_clean.add_argument('session_id', type=int, nargs='?')
    parser_clean.set_defaults(func=cmd.clean)

    # set
    subparsers_set = parser_set.add_subparsers()
    parser_set_exp = subparsers_set.add_parser('experiment-dir')
    parser_set_env = subparsers_set.add_parser('environment-dir')
    # set experiment-dir
    parser_set_exp.add_argument('dir')
    parser_set_exp.set_defaults(func=cmd.set_experiment_dir)
    # set environment-dir
    parser_set_env.add_argument('dir')
    parser_set_env.set_defaults(func=cmd.set_environment_dir)

    # env
    parser_env.add_argument('keyval')
    parser_env.set_defaults(func=cmd.set_ctip_env_variable)

    # tables
    parser_tables.set_defaults(func=cmd.tables)

    # list
    parser_list.add_argument('table_name')
    parser_list.add_argument('where_clause', nargs='*')
    parser_list.set_defaults(func=cmd.list)

    # update
    subparsers_update = parser_update.add_subparsers()
    parser_update_status = subparsers_update.add_parser('status')
    parser_update_id = subparsers_update.add_parser('id')
    # update status
    parser_update_status.add_argument('job_id')
    parser_update_status.add_argument('new_status')
    parser_update_status.set_defaults(func=cmd.update_status)
    # update id
    parser_update_id.add_argument('job_id')
    parser_update_id.add_argument('new_id')
    parser_update_id.set_defaults(func=cmd.update_id)

    # log
    subparsers_log = parser_log.add_subparsers()
    parser_log_start = subparsers_log.add_parser('start')
    parser_log_pause = subparsers_log.add_parser('pause')
    parser_log_resume = subparsers_log.add_parser('resume')
    parser_log_end = subparsers_log.add_parser('end')
    parser_log.add_argument('job_id')
    # log start
    parser_log_start.set_defaults(func=cmd.log_start)
    # log pause
    parser_log_pause.set_defaults(func=cmd.log_pause)
    # log resume
    parser_log_resume.set_defaults(func=cmd.log_resume)
    # log end
    parser_log_end.set_defaults(func=cmd.log_end)

    return parser