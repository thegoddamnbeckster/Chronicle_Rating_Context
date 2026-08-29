# -*- coding: utf-8 -*-
"""Chronicle Rating - Context Menu Button

Context menu addon that adds "Rate on Chronicle" to a movie or episode's
context menu. Its only job is reading the focused ListItem's DBTYPE/DBID and
handing off to script.chronicle.rating via RunScript -- all the actual rating
logic (dialog, submission, etc.) lives there. See addon.xml's own docstring
for why this has to be a separate addon rather than bundled into that one's
extensions.

Mirrors context.simkl.rate/addon.py's architecture, minus the episode/season
-> show resolution SIMKL needs (SIMKL only rates at the show level; Chronicle
rates movies and episodes directly, matching script.chronicle.rating's
existing kodi.context.item visibility condition of movie/episode only).
"""

import xbmc
import xbmcgui

VERSION = '1.0.0'


def log(message):
    xbmc.log('[context.chronicle.rate v{0}] {1}'.format(VERSION, message), xbmc.LOGINFO)


def log_error(message):
    xbmc.log('[context.chronicle.rate v{0}] ERROR: {1}'.format(VERSION, message), xbmc.LOGERROR)


def get_media_type():
    """ListItem.DBTYPE rather than Container.Content() -- works in every view
    (library, in-progress, recently added, etc.), not just the main library
    listing."""
    dbtype = xbmc.getInfoLabel('ListItem.DBTYPE')
    log("ListItem.DBTYPE = '{0}'".format(dbtype))
    if dbtype in ('movie', 'episode'):
        return dbtype
    return None


if __name__ == '__main__':
    log('=' * 40)
    log('CONTEXT MENU TRIGGERED')
    log('=' * 40)

    try:
        dbid = xbmc.getInfoLabel('ListItem.DBID')
        media_type = get_media_type()

        log("DBID = '{0}'".format(dbid))
        log("Media Type = '{0}'".format(media_type))

        if not dbid:
            log_error('No DBID found - cannot rate')
        elif not media_type:
            log_error('Unknown or unsupported media type - cannot rate')
        else:
            command = 'RunScript(script.chronicle.rating,action=rate,media_type={0},dbid={1})'.format(
                media_type, dbid)
            log('Executing: {0}'.format(command))
            xbmc.executebuiltin(command)
            log('Command sent to script.chronicle.rating')

        log('=' * 40)
        log('CONTEXT MENU COMPLETE')
        log('=' * 40)

    except Exception as exc:
        log_error('Exception in context menu: {0}'.format(exc))
