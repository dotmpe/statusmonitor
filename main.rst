StatusMonitor is a fullscreen graphical monitor for system properties and
proccesses. It aims for a generic approach to accumulate and update externally
processed reports, and emphasizes on the presentation layer.

This should do away with any need for manual inspection of machines in a company
network. Except when writing new scripts, the monitor accumulates data from
external scripts and reports.

TODO: Configurations should set the main slideshow loop behaviour. Having
nested slideshows and event priorities and triggers is very high on the
wishlist.


Introduction
------------
For backend code, Python, SQLAlchemy, and a relational database
may be used.
The server might be an Twisted internet daemon?
During development an SQLite3 storage is used.

Cross-platform compatibility is targetted, though in fairness the intended
deployment (of both server and clients) is on \*nix boxes (Linux, BSD).

Client-Server communication is enabled by HaXe transparantly tro
Later on, if viable, the GUI may be replaced by an NME application. Which
means a (partial) port to HaXe. The main reason is the graphics capabilities
of NME: vector and bitmap animations, interaction, opengl. And no more browser.

Using jQuery for most of the frontend behaviour allows to have fairly simple
templated HTML. HaXe can do templating, but not something sophisticated as smarty?

.. note:: further thoughts

   In browser this may mean the client turns HTML5, or if Flash would be the
   only alternative maybe native binaries using the cross-platform SDL
   graphics library. As HaXe/NME has its own remoting facilities, perhaps the
   server can run from neko or native linux too.

   On the other hand, HaXe might replace all of that. jQuery would still be a
   requirement, so need to have a external class definition for that.


Status
------

Python Backend
_______________
Version 1 is the next milestone. Next version: 0.1. Description
below.

config (yaml/json)

server
  datastore (mysql)
  worker (threaded process to provide one or more datums)
  screen (template with datum requirements)

Version 1::

    dataserver ------> *workers
       |
       |-------> json rpc client
       '-------> socket streaming client

The RPC client will at first be for server ops/adm,
but may later be used by a multimedia frontend.
Its communication is by datastructures.

The streaming client is to facilitate a live view of running processes.
Its communication is simply line based, with relatively small datums.
In principle the data it returns is plain text, though to facilitate rich
rendering the line string is encoded in a json (line!). The structure
is used to encode the results the server got for the line.

Haxe Client/Server
___________________
Version 1 needs to be an fully running slideshow of html snippets.
Next version: 0.1.

Current state:
- Need to test.
- Not much done. Some HaXe code, Python for Sqlite store.

