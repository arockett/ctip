# -*- coding: utf-8 -*-
"""
Test the GenSchema API.

Created on Fri Sep  9 10:08:01 2016

@author: Aaron Beckett
"""

import pytest
import mock

import ctip.entrypoint as cli


# intercept the args object
def sentry(intercepted_args):
    global args
    args = intercepted_args


##################### RUN COMMAND ###################################

class TestRunCommand(object):
    def test_basic_run_command(self):
        # Use -n flag for name and -f flag for genfile
        with mock.patch('ctip.entrypoint.cmd.run', side_effect=sentry) as run_function:
            cli.main(['ctip', 'run', 'P3Brain', '-f', 'genfile.gen', '-n', 'test_run'])

        run_function.assert_called_once()
        assert args.experiment == 'P3Brain'
        assert args.genfile == 'genfile.gen'
        assert args.name == 'test_run'
        assert not args.env

        # Use --name flag of name and --genfile flag for genfile
        with mock.patch('ctip.entrypoint.cmd.run', side_effect=sentry) as run_function:
            cli.main(['ctip', 'run', 'P3Brain', '--genfile', 'genfile.gen', '--name', 'test_run'])

        run_function.assert_called_once()
        assert args.experiment == 'P3Brain'
        assert args.genfile == 'genfile.gen'
        assert args.name == 'test_run'
        assert not args.env

    def test_run_command_with_env(self):
        # Use -e flag for environment
        with mock.patch('ctip.entrypoint.cmd.run', side_effect=sentry) as run_function:
            cli.main(['ctip', 'run', 'MarkovBrain', '-f', 'new_genfile.gen', '-n', 'local_run', '-e', 'Local'])

        run_function.assert_called_once()
        assert args.experiment == 'MarkovBrain'
        assert args.genfile == 'new_genfile.gen'
        assert args.name == 'local_run'
        assert args.env == 'Local'

        # Use --env flag for environment
        with mock.patch('ctip.entrypoint.cmd.run', side_effect=sentry) as run_function:
            cli.main(['ctip', 'run', 'MarkovBrain', '-f', 'new_genfile.gen', '-n', 'local_run', '--env', 'Local'])

        run_function.assert_called_once()
        assert args.experiment == 'MarkovBrain'
        assert args.genfile == 'new_genfile.gen'
        assert args.name == 'local_run'
        assert args.env == 'Local'

    def test_missing_experiment(self):
        with mock.patch('ctip.entrypoint.cmd.run', side_effect=sentry) as run_function:
            with pytest.raises(SystemExit):
                cli.main(['ctip', 'run', '-f', 'genfile.gen', '-n', 'test_run'])

    def test_missing_genfile(self):
        with mock.patch('ctip.entrypoint.cmd.run', side_effect=sentry) as run_function:
            with pytest.raises(SystemExit):
                cli.main(['ctip', 'run', 'P3Brain', '-n', 'test_run'])

    def test_missing_name(self):
        with mock.patch('ctip.entrypoint.cmd.run', side_effect=sentry) as run_function:
            with pytest.raises(SystemExit):
                cli.main(['ctip', 'run', 'P3Brain', '-f', 'gen.gen'])


##################### CHECK COMMAND ###################################

class TestCheckCommand(object):
    def test_without_session_id(self):
        with mock.patch('ctip.entrypoint.cmd.check', side_effect=sentry) as check_function:
            cli.main(['ctip', 'check'])

        check_function.assert_called_once()
        assert not args.session_id

    def test_with_session_id(self):
        with mock.patch('ctip.entrypoint.cmd.check', side_effect=sentry) as check_function:
            cli.main(['ctip', 'check', '3'])

        check_function.assert_called_once()
        assert args.session_id == 3


##################### STOP COMMAND ###################################

class TestStopCommand(object):
    def test_without_session_id(self):
        with mock.patch('ctip.entrypoint.cmd.stop', side_effect=sentry) as stop_function:
            cli.main(['ctip', 'stop'])

        stop_function.assert_called_once()
        assert not args.session_id

    def test_with_session_id(self):
        with mock.patch('ctip.entrypoint.cmd.stop', side_effect=sentry) as stop_function:
            cli.main(['ctip', 'stop', '7'])

        stop_function.assert_called_once()
        assert args.session_id == 7


##################### CLEAN COMMAND ###################################

class TestCleanCommand(object):
    def test_without_session_id(self):
        with mock.patch('ctip.entrypoint.cmd.clean', side_effect=sentry) as clean_function:
            cli.main(['ctip', 'clean'])

        clean_function.assert_called_once()
        assert not args.session_id

    def test_with_session_id(self):
        with mock.patch('ctip.entrypoint.cmd.clean', side_effect=sentry) as clean_function:
            cli.main(['ctip', 'clean', '2'])

        clean_function.assert_called_once()
        assert args.session_id == 2


##################### SET COMMAND ###################################

class TestSetCommand(object):
    def test_set_experiment_dir(self):
        with mock.patch('ctip.entrypoint.cmd.set_experiment_dir', side_effect=sentry) as exp_dir_function:
            cli.main(['ctip', 'set', 'experiment-dir', '/home/me/research/experiments'])

        exp_dir_function.assert_called_once()
        assert args.dir == '/home/me/research/experiments'

    def test_missing_exp_dir(self):
        with mock.patch('ctip.entrypoint.cmd.set_experiment_dir', side_effect=sentry) as exp_dir_function:
            with pytest.raises(SystemExit):
                cli.main(['ctip', 'set', 'experiment-dir'])

    def test_set_environment_dir(self):
        with mock.patch('ctip.entrypoint.cmd.set_environment_dir', side_effect=sentry) as env_dir_function:
            cli.main(['ctip', 'set', 'environment-dir', '/home/me/research/environments'])

        env_dir_function.assert_called_once()
        assert args.dir == '/home/me/research/environments'

    def test_missing_env_dir(self):
        with mock.patch('ctip.entrypoint.cmd.set_environment_dir', side_effect=sentry) as env_dir_function:
            with pytest.raises(SystemExit):
                cli.main(['ctip', 'set', 'environment-dir'])


##################### ENV COMMAND ###################################

class TestEnvCommand(object):
    def test_env_command(self):
        with mock.patch('ctip.entrypoint.cmd.set_ctip_env_variable', side_effect=sentry) as env_function:
            cli.main(['ctip', 'env', 'mykey=myval'])

        env_function.assert_called_once()
        assert args.keyval == 'mykey=myval'

    def test_keyvalue_with_spaces(self):
        with mock.patch('ctip.entrypoint.cmd.set_ctip_env_variable', side_effect=sentry) as env_function:
            with pytest.raises(SystemExit):
                cli.main(['ctip', 'env', 'key', '=', 'val'])

    def test_without_keyvalue(self):
        with mock.patch('ctip.entrypoint.cmd.set_ctip_env_variable', side_effect=sentry) as env_function:
            with pytest.raises(SystemExit):
                cli.main(['ctip', 'env'])


##################### TABLES COMMAND ###################################

class TestTablesCommand(object):
    def test_tables_command(self):
        with mock.patch('ctip.entrypoint.cmd.tables', side_effect=sentry) as tables_function:
            cli.main(['ctip', 'tables'])

        tables_function.assert_called_once()


##################### LIST COMMAND ###################################

class TestListCommand(object):
    def test_without_where_clause(self):
        with mock.patch('ctip.entrypoint.cmd.list', side_effect=sentry) as list_function:
            cli.main(['ctip', 'list', 'table_name'])

        list_function.assert_called_once()
        assert args.table_name == 'table_name'
        assert not args.where_clause

    def test_missing_table_name(self):
        with mock.patch('ctip.entrypoint.cmd.list', side_effect=sentry) as list_function:
            with pytest.raises(SystemExit):
                cli.main(['ctip', 'list'])

    def test_with_where_clause(self):
        def test_without_where_clause(self):
            with mock.patch('ctip.entrypoint.cmd.list', side_effect=sentry) as list_function:
                cli.main(['ctip', 'list', 'jobs', "where status = 'error'"])

            list_function.assert_called_once()
            assert args.table_name == 'jobs'
            assert args.where_clause == "where status = 'error'"

    def test_where_clause_with_spaces(self):
        def test_without_where_clause(self):
            with mock.patch('ctip.entrypoint.cmd.list', side_effect=sentry) as list_function:
                with pytest.raises(SystemExit):
                    cli.main(['ctip', 'list', 'jobs', "where", 'status', '=', "'error'"])


##################### UPDATE COMMAND ###################################

class TestUpdateCommand(object):
    def test_update_status(self):
        with mock.patch('ctip.entrypoint.cmd.update_status', side_effect=sentry) as update_function:
            cli.main(['ctip', 'update', 'status', '43623', 'done'])

        update_function.assert_called_once()
        assert args.job_id == '43623'
        assert args.new_status == 'done'

    def test_update_id(self):
        with mock.patch('ctip.entrypoint.cmd.update_id', side_effect=sentry) as update_function:
            cli.main(['ctip', 'update', 'id', '261b', '12345ab'])

        update_function.assert_called_once()
        assert args.job_id == '261b'
        assert args.new_id == '12345ab'


##################### LOG COMMAND ###################################

class TestLogCommand(object):
    def test_log_start(self):
        with mock.patch('ctip.entrypoint.cmd.log_start', side_effect=sentry) as log_function:
            cli.main(['ctip', 'log', 'start', 'ab123'])

        log_function.assert_called_once()
        assert args.job_id == 'ab123'

    def test_log_pause(self):
        with mock.patch('ctip.entrypoint.cmd.log_pause', side_effect=sentry) as log_function:
            cli.main(['ctip', 'log', 'pause', 'ab123'])

        log_function.assert_called_once()
        assert args.job_id == 'ab123'

    def test_log_resume(self):
        with mock.patch('ctip.entrypoint.cmd.log_resume', side_effect=sentry) as log_function:
            cli.main(['ctip', 'log', 'resume', 'ab123'])

        log_function.assert_called_once()
        assert args.job_id == 'ab123'

    def test_log_end(self):
        with mock.patch('ctip.entrypoint.cmd.log_end', side_effect=sentry) as log_function:
            cli.main(['ctip', 'log', 'end', 'ab123'])

        log_function.assert_called_once()
        assert args.job_id == 'ab123'

