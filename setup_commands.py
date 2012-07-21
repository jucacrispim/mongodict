#-*- coding: utf-8 -*-

import sys
import shutil
from glob import glob
from pkg_resources import normalize_path, require
from pkg_resources import working_set, add_activation_listener
from setuptools.command.test import test
from lib2to3.main import main as cmd2to3


class Test3k(test):
    """
    Run 2to3 on test files before run
    the tests itself.
    """

    test_files_glob = 'test_*.py'
    fixes_modules = ['lib2to3.fixes', 'fixes']

    def fix_2to3(self):
        # Here is a INPLACE change!
        for fname in glob(self.test_files_glob):
            for fixes_module in self.fixes_modules:
                cmd2to3(fixes_module, ['-f', 'all', '-w', fname])

    def restore_backup(self):
        for fname in glob('*.bak'):
            orig_fname = fname.rsplit('.', 1)[0]
            shutil.move(fname, orig_fname)

    def with_project_on_sys_path(self, func):
        # Copy and paste from setuptools test command
        # with minor changes to run 2to3.

        # Here we are always running 2to3, so don't do this inplace:
        # Ensure metadata is up-to-date
        self.reinitialize_command('build_py', inplace=0)
        self.run_command('build_py')
        bpy_cmd = self.get_finalized_command("build_py")
        build_path = normalize_path(bpy_cmd.build_lib)

        # Build extensions
        self.reinitialize_command('egg_info', egg_base=build_path)
        self.run_command('egg_info')

        self.reinitialize_command('build_ext', inplace=0)
        self.run_command('build_ext')

        ei_cmd = self.get_finalized_command("egg_info")

        old_path = sys.path[:]
        old_modules = sys.modules.copy()

        try:
            sys.path.insert(0, normalize_path(ei_cmd.egg_base))
            working_set.__init__()
            add_activation_listener(lambda dist: dist.activate())
            require('%s==%s' % (ei_cmd.egg_name, ei_cmd.egg_version))
            # modifying test files
            # test files are inplace modified!
            self.fix_2to3()
            func()
        finally:
            # restoring files
            self.restore_backup()
            sys.path[:] = old_path
            sys.modules.clear()
            sys.modules.update(old_modules)
            working_set.__init__()
