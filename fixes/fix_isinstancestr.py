#-*- coding: utf-8 -*-

from lib2to3.fixer_base import BaseFix


class FixIsinstancestr(BaseFix):

    PATTERN = """\
power< 'isinstance' trailer< '(' arglist< any ',' name='str'> ')' > > any*
"""

    def transform(self, node, results):
        name = results['name']
        name.value = 'bytes'
        name.changed()
