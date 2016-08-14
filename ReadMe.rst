StatusMonitor
=============
:created: 2012-01-30
:updated: 2016-06-25

Old prototype code for a statusmonitor, ie. a view of a set of status items.

ReadMe-old.rst covers other code.

Concepts
--------
outline
  Of various purpuse but all forms of hierarchies, from very generic
  folder/separator/item type schemas to various schemas of folders/groups/dirs/feeds
  and/or with various types of items.

  TODO: put this into repo meant for generic outlines.

  book marks
    Web browsers, online services I/O.
    Elements folders, maybe dividers and smart folders.
    Items with href, label, descr, tags attrs.

  web feeds
    Summarized item lists with links to full content/publisher/author and other
    metadata. Publishing, syndiation format.

    Atom
      Set Syndication file format and protocol standards.

  note taking
    Leo
      Python embedded outline spread over several files, coupled?[*]_ using sentinel
      lines. Extensions to include other formats such as text markup.

      .. [*] Or does it use a main outline data structure?

    http://www.wasatch.edu/cms/lib/ut01000315/centricity/domain/572/wg1outlineformat.doc
      One-page specification for an outline. Outlining is to summarize documents, or
      more generically to create a summarized view of another, larger body of contained
      chapters, sections and text content.

      Elements:

      - headers and sub headers, having
      - roman numbered ideas, or chapters (capitalized/red highlighted words),
        under which smaller
      - numbered sub ideas items (green), or first sentence of section.


Components
----------
src
  python
    - 2012 SQL schema

    statusmonitor
      urw_bstat
      - 2016 Urwid based ncurses views for build monitor

  haxe
    - 2012 Prototype

bin
  pd-to-states.py

History
-------
- 2012 intial code HaXe for x-compilable HTML-based view generator. Some Py.
- 2016 Loked at NPM+blessed for NodeJS based, however chosen Py+Urwid.



http://www.wasatch.edu/cms/lib/ut01000315/centricity/domain/572/wg1outlineformat.doc

