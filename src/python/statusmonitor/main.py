#!/usr/bin/env python
#
# CLI-Curses frontend for dotmpe/statusmonitor bstat (build status monitor)

#    Copyright (C) 2016  Berend van Berkum
#
#    This library is free software; you can redistribute it and/or
#    modify it under the terms of the GNU Lesser General Public
#    License as published by the Free Software Foundation; either
#    version 2.1 of the License, or (at your option) any later version.
#
#    This library is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#    Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public
#    License along with this library; if not, write to the Free Software
#    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#

"""
Build Status monitor in curses.

Dev (redmine.dandy.wtwta.org)
    - Display status as a collection of blocks,
      either or mixed small and big/fuller representations.
    - Display status as a collection of tree table view record lines.

"""

import urwid


palette = [
    ('banner', '', '', '', '#ffa', '#60d'),
    ('streak', '', '', '', 'g50', '#60a'),
    ('inside', '', '', '', 'g38', '#808'),
    ('outside', '', '', '', 'g27', '#a06'),
    ('bg', '', '', '', 'g7', '#d06'),
]


if __name__ == '__main__':

    import sys
    from os.path import basename, realpath, splitext, join, dirname

    src_rp = realpath(__file__)
    src_f = splitext(basename(src_rp))[0] + '.py'
    src_p = dirname(src_rp)

    sys.path.insert(0, dirname(src_p))

    import statusmonitor
    from statusmonitor import simplebackend

    backend = simplebackend.load_tree_from_yaml('var/stm-v1.yml')

    statusmonitor.urw_bstat.DirectoryBrowser(backend).main()
    #statusmonitor.urw_bstat.BStatMain().main(palette)

