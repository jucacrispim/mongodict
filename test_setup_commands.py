#-*- coding: utf-8 -*-

from distutils.dist import Distribution
from unittest import TestCase
from mock import Mock, patch
import setup_commands


@patch.object(setup_commands, 'glob', Mock())
class Test3kTestCase(TestCase):
    def setUp(self):
        dist_mock = Mock(spec=Distribution)
        dist_mock.verbose = Mock()
        self.test3k = setup_commands.Test3k(dist_mock)

    @patch.object(setup_commands, 'cmd2to3', Mock())
    def test_fix_2to3(self):
        # Tests if 2to3 is called correctly

        setup_commands.glob.return_value = ['test_a.py', 'test_b.py']
        self.test3k.fix_2to3()

        call_args_list = [args[0] for args in \
                              setup_commands.cmd2to3.call_args_list]

        expected_call_args_list = [
            ('lib2to3.fixes', ['-f', 'all', '-w', 'test_a.py']),
            ('fixes', ['-f', 'all', '-w', 'test_a.py']),
            ('lib2to3.fixes', ['-f', 'all', '-w', 'test_b.py']),
            ('fixes', ['-f', 'all', '-w', 'test_b.py']), ]

        self.assertEqual(call_args_list, expected_call_args_list)

    @patch.object(setup_commands.shutil, 'move', Mock())
    def test_restore_backup(self):
        # Tests if the backup files are
        # restored correctly
        setup_commands.glob.return_value = ['test_a.py.bak', 'test_b.py.bak']
        self.test3k.restore_backup()

        call_args_list = [args[0] for args in \
                              setup_commands.shutil.move.call_args_list]
        expected_call_args_list = [
            ('test_a.py.bak', 'test_a.py'),
            ('test_b.py.bak', 'test_b.py'), ]

        self.assertEqual(call_args_list, expected_call_args_list)

    @patch.object(setup_commands, 'normalize_path', Mock())
    @patch.object(setup_commands, 'working_set', Mock())
    @patch.object(setup_commands, 'add_activation_listener', Mock())
    @patch.object(setup_commands, 'require', Mock())
    def test_with_project_on_sys_path(self):
        # Tests if test files are fixed by 2to3 and
        # if backup files are restored

        self.test3k.fix_2to3 = Mock()
        self.test3k.restore_backup = Mock()
        self.test3k.run_command = Mock()
        
        self.test3k.with_project_on_sys_path(Mock())

        self.assertTrue(self.test3k.fix_2to3.called)
        self.assertTrue(self.test3k.restore_backup.called)                                             
