# -*- coding: utf-8 -*-
"""The context-menu entry: it reads the focused item's DBTYPE/DBID and hands off to script.chronicle.rating."""
import os
import runpy
import sys
import types
import unittest
from unittest import mock

_ADDON = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'addon.py')


def _run(labels):
    xbmc = types.ModuleType('xbmc')
    xbmc.LOGINFO, xbmc.LOGERROR = 2, 4
    xbmc.log = mock.Mock()
    xbmc.getInfoLabel = mock.Mock(side_effect=lambda key: labels.get(key, ''))
    xbmc.executebuiltin = mock.Mock()
    with mock.patch.dict(sys.modules, {'xbmc': xbmc, 'xbmcgui': types.ModuleType('xbmcgui')}):
        runpy.run_path(_ADDON, run_name='__main__')
    return xbmc


class TestContextEntry(unittest.TestCase):
    def test_a_movie_or_an_episode_is_handed_to_the_rating_addon(self):
        for dbtype in ('movie', 'episode'):
            xbmc = _run({'ListItem.DBTYPE': dbtype, 'ListItem.DBID': '42'})
            xbmc.executebuiltin.assert_called_once_with(
                'RunScript(script.chronicle.rating,action=rate,media_type={0},dbid=42)'.format(dbtype))

    def test_other_types_and_missing_ids_do_nothing(self):
        for labels in ({'ListItem.DBTYPE': 'tvshow', 'ListItem.DBID': '42'}, {'ListItem.DBTYPE': 'movie', 'ListItem.DBID': ''},
                       {'ListItem.DBTYPE': '', 'ListItem.DBID': '42'}):
            xbmc = _run(labels)
            xbmc.executebuiltin.assert_not_called()

    def test_a_failure_is_logged_not_raised(self):
        xbmc = types.ModuleType('xbmc')
        xbmc.LOGINFO, xbmc.LOGERROR = 2, 4
        xbmc.log = mock.Mock()
        xbmc.getInfoLabel = mock.Mock(side_effect=RuntimeError('skin gone'))
        with mock.patch.dict(sys.modules, {'xbmc': xbmc, 'xbmcgui': types.ModuleType('xbmcgui')}):
            runpy.run_path(_ADDON, run_name='__main__')
        self.assertTrue(any('Exception' in str(c) for c in xbmc.log.call_args_list))


if __name__ == '__main__':
    unittest.main()
