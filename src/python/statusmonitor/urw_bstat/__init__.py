#
# Urwid example lazy directory browser / tree view
#    Copyright (C) 2004-2011  Ian Ward
#    Copyright (C) 2010  Kirk McDonald
#    Copyright (C) 2010  Rob Lanphier
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
# Urwid web site: http://excess.org/urwid/

"""
Based on `browse.py` tree view of Urwid examples.

See frontend statusmonitor.urw_bstat.main for complete doc-str description.
"""

import itertools
import re
import os

import urwid


class FlagFileWidget(urwid.TreeWidget):

    # apply an attribute to the expand/unexpand icons
    unexpanded_icon = urwid.AttrMap(urwid.TreeWidget.unexpanded_icon,
        'dirmark')
    expanded_icon = urwid.AttrMap(urwid.TreeWidget.expanded_icon,
        'dirmark')

    def __init__(self, node):
        self.__super.__init__(node)
        # insert an extra AttrWrap for our own use
        self._w = urwid.AttrWrap(self._w, None)
        self.flagged = False
        self.update_w()

    def selectable(self):
        return True

    def keypress(self, size, key):
        """allow subclasses to intercept keystrokes"""
        print("keypress %r" % key)
        key = self.__super.keypress(size, key)
        if key:
            key = self.unhandled_keys(size, key)
        return key

    def unhandled_keys(self, size, key):
        """
        Override this method to intercept keystrokes in subclasses.
        Default behavior: Toggle flagged on space, ignore other keys.
        """
        print("unhandled_keys %r" % key)
        if key == " ":
            print(self.flagged and "flagged" or "not flagged")
            self.flagged = not self.flagged
            self.update_w()
        else:
            return key

    def update_w(self):
        """Update the attributes of self.widget based on self.flagged.
        """
        if self.flagged:
            self._w.attr = 'flagged'
            self._w.focus_attr = 'flagged focus'
        else:
            self._w.attr = 'body'
            self._w.focus_attr = 'focus'


class FileTreeWidget(FlagFileWidget):
    """Widget for individual files."""
    def __init__(self, node):
        self.__super.__init__(node)
        path = node.get_value()
        add_widget(path, self)

    def get_display_text(self):
        return self.get_node().get_key()



class EmptyWidget(urwid.TreeWidget):
    """A marker for expanded directories with no contents."""
    def get_display_text(self):
        return ('flag', '(empty directory)')


class ErrorWidget(urwid.TreeWidget):
    """A marker for errors reading directories."""

    def get_display_text(self):
        return ('error', "(error/permission denied)")


class DirectoryWidget(FlagFileWidget):
    """Widget for a directory."""
    def __init__(self, node):
        self.__super.__init__(node)
        path = node.get_value()
        add_widget(path, self)
        assert node.data
        self.expanded = starts_expanded(node)
        self.update_expanded_icon()

    def get_display_text(self):
        node = self.get_node()
        if node.get_depth() == 0:
            return "/"
        else:
            return node.get_key()


class FileNode(urwid.TreeNode):
    """Metadata storage for individual files"""

    def __init__(self, path, parent=None):
        depth = path.count(dir_sep())
        key = os.path.basename(path)
        urwid.TreeNode.__init__(self, path, key=key, parent=parent, depth=depth)

    def load_parent(self):
        parentname, myname = os.path.split(self.get_value())
        parent = DirectoryNode(parentname)
        parent.set_child_node(self.get_key(), self)
        return parent

    def load_widget(self):
        return FileTreeWidget(self)


class EmptyNode(urwid.TreeNode):
    def load_widget(self):
        return EmptyWidget(self)


class ErrorNode(urwid.TreeNode):
    def load_widget(self):
        return ErrorWidget(self)


class DirectoryNode(urwid.ParentNode):
    """Metadata storage for directories"""

    def __init__(self, path, parent=None):
        if path == dir_sep():
            depth = 0
            key = None
        else:
            depth = path.count(dir_sep())
            key = os.path.basename(path)
        urwid.ParentNode.__init__(self, path, key=key, parent=parent,
                                  depth=depth)

    def load_parent(self):
        parentname, myname = os.path.split(self.get_value())
        parent = DirectoryNode(parentname)
        parent.set_child_node(self.get_key(), self)
        return parent

    def load_child_keys(self):
        dirs = []
        files = []
        try:
            path = self.get_value()
            # separate dirs and files
            for a in os.listdir(path):
                if os.path.isdir(os.path.join(path,a)):
                    dirs.append(a)
                else:
                    files.append(a)
        except OSError, e:
            depth = self.get_depth() + 1
            self._children[None] = ErrorNode(self, parent=self, key=None,
                                             depth=depth)
            return [None]

        # sort dirs and files
        dirs.sort(key=alphabetize)
        files.sort(key=alphabetize)
        # store where the first file starts
        self.dir_count = len(dirs)
        # collect dirs and files together again
        keys = dirs + files
        if len(keys) == 0:
            depth=self.get_depth() + 1
            self._children[None] = EmptyNode(self, parent=self, key=None,
                                             depth=depth)
            keys = [None]
        return keys

    def load_child_node(self, key):
        """Return either a FileNode or DirectoryNode"""
        index = self.get_child_index(key)
        if key is None:
            return EmptyNode(None)
        else:
            path = os.path.join(self.get_value(), key)
            if index < self.dir_count:
                return DirectoryNode(path, parent=self)
            else:
                path = os.path.join(self.get_value(), key)
                return FileNode(path, parent=self)

    def load_widget(self):
        return DirectoryWidget(self)


class DirectoryBrowser:
    palette = [
        ('body', 'black', 'light gray'),#, '', '#fff', '#60d'),
        #('body', 'dark gray', 'black'),
        #('body', 'light gray', 'dark gray'),
        ('flagged', 'black', 'dark green', ('bold','underline')),
        ('focus', 'light gray', 'dark blue', 'standout'),
        ('flagged focus', 'yellow', 'dark cyan',
                ('bold','standout','underline')),
        ('head', 'yellow', 'black', 'standout'),
        ('foot', 'light gray', 'black'),
        ('key', 'light cyan', 'black','underline'),
        ('title', 'white', 'black', 'bold'),
        ('dirmark', 'black', 'dark cyan', 'bold'),
        ('flag', 'dark gray', 'light gray'),
        ('error', 'dark red', 'light gray'),

        ('passed', 'light green,standout', 'light gray', '', '', ''),
        ('errored', 'light red,standout', 'light gray', '', '', ''),
        ('failed', 'yellow,standout', 'light gray', '', '', ''),

        ('failedf', 'brown', 'light gray', '', '', ''),
        #('failedf', 'brown', 'dark gray', '', '', ''),
        ('erroredf', 'dark red', 'light gray', '', '', ''),
    ]

    footer_text = [
        ('title', "Directory Browser"), "    ",
        ('key', "UP"), ",", ('key', "DOWN"), ",",
        ('key', "PAGE UP"), ",", ('key', "PAGE DOWN"),
        "  ",
        ('key', "SPACE"), "  ",
        ('key', "+"), ",",
        ('key', "-"), "  ",
        ('key', "LEFT"), "  ",
        ('key', "HOME"), "  ",
        ('key', "END"), "  ",
        ('key', "Q"),
    ]


    def __init__(self, tree):
        cwd = os.getcwd()
        store_initial_cwd(cwd)
        self.header = urwid.Text("")
        self.listbox = urwid.TreeListBox(urwid.TreeWalker(tree))
        self.listbox.offset_rows = 1
        self.footer = urwid.AttrWrap(urwid.Text(self.footer_text),
            'foot')
        self.view = urwid.Frame(
            urwid.AttrWrap(self.listbox, 'body'),
            header=urwid.AttrWrap(self.header, 'head'),
            footer=self.footer)

    def on_data(self):
        print("TODO: data changed, reload")
        #self.fp.readlines()

    def main(self, fp):
        """Run the program."""

        self.loop = urwid.MainLoop(self.view, self.palette,
            unhandled_input=self.unhandled_input)

        #self.fp = fp
        #self.loop.watch_file(fp.fileno(), self.on_data)
        self.loop.run()

        # on exit, write the flagged filenames to the console
        names = [escape_filename_sh(x) for x in get_flagged_names()]
        print(" ".join(names))

    def unhandled_input(self, k):
        # update display of focus directory
        if k in ('q','Q'):
            raise urwid.ExitMainLoop()


#######
# global cache of widgets
_widget_cache = {}

def add_widget(path, widget):
    """Add the widget for a given path"""

    _widget_cache[path] = widget

def get_flagged_names():
    """Return a list of all filenames marked as flagged."""

    l = []
    for w in _widget_cache.values():
        if w.flagged:
            l.append(w.get_node().get_value())
    return l



######
# store path components of initial current working directory
_initial_cwd = []

def store_initial_cwd(name):
    """Store the initial current working directory path components."""

    global _initial_cwd
    _initial_cwd = name.split(dir_sep())

def starts_expanded(node):
    """Return True if directory is a parent of initial cwd."""

    if 'status' in node.data and node.data['status']:
        return True
    return False


def escape_filename_sh(name):
    """Return a hopefully safe shell-escaped version of a filename."""

    # check whether we have unprintable characters
    for ch in name:
        if ord(ch) < 32:
            # found one so use the ansi-c escaping
            return escape_filename_sh_ansic(name)

    # all printable characters, so return a double-quoted version
    name.replace('\\','\\\\')
    name.replace('"','\\"')
    name.replace('`','\\`')
    name.replace('$','\\$')
    return '"'+name+'"'


def escape_filename_sh_ansic(name):
    """Return an ansi-c shell-escaped version of a filename."""

    out =[]
    # gather the escaped characters into a list
    for ch in name:
        if ord(ch) < 32:
            out.append("\\x%02x"% ord(ch))
        elif ch == '\\':
            out.append('\\\\')
        else:
            out.append(ch)

    # slap them back together in an ansi-c quote  $'...'
    return "$'" + "".join(out) + "'"

SPLIT_RE = re.compile(r'[a-zA-Z]+|\d+')
def alphabetize(s):
    L = []
    for isdigit, group in itertools.groupby(SPLIT_RE.findall(s), key=lambda x: x.isdigit()):
        if isdigit:
            for n in group:
                L.append(('', int(n)))
        else:
            L.append((''.join(group).lower(), 0))
    return L

def dir_sep():
    """Return the separator used in this os."""
    return getattr(os.path,'sep','/')




def exit_on_q(key):
    if key in ('q', 'Q'):
        raise urwid.ExitMainLoop()



class BStatMain:

    """
    Initialize main bstat view
    """

    def __init__(self):
        self.view = urwid.SolidFill()
        self.div = urwid.Divider()
        self.outside = urwid.AttrMap(self.div, 'outside')
        self.inside = urwid.AttrMap(self.div, 'inside')
        self.txt = urwid.Text(('banner', u" Hello World "), align='center')
        self.streak = urwid.AttrMap(self.txt, 'streak')

    def init(self):

        self.loop.screen.set_terminal_properties(colors=256)
        self.loop.widget = urwid.AttrMap(self.view, 'bg')
        self.loop.widget.original_widget = urwid.Filler(urwid.Pile([]))

        pile = self.loop.widget.base_widget # .base_widget skips the decorations

        for item in [self.outside, self.inside, self.streak, self.inside, self.outside]:
            pile.contents.append((item, pile.options()))

    def main(self, palette, unhandled_input=exit_on_q):

        """
        Start main loop.
        """

        self.loop = urwid.MainLoop(self.view, palette, unhandled_input=unhandled_input)
        self.init()
        self.loop.run()




