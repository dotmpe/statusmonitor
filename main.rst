StatusMonitor is fullscreen graphical monitor for system properties and
proccesses.

1. The project to aims to provide an integrated view of assorted workflows
in a medium sized SaaS/web-development company. 
2. It should do away with manual inspection of servers. 
3. It will provide a continuous slideshow of reports, emphasizing important screens.
4. It will run as DHTML application, fully interactively browsable.

Introduction
------------
The initial version will use Python, SQLAlchemy, and a relational database.
During development an SQLite3 storage is used. jQuery will be responsible
for the frontend.

The server will be an Twisted internet daemon.

Cross-platform compatibility is targetted, though in fairness the intended
deployment (of both server and clients) is on \*nix boxes (Linux, BSD).

Later on, if viable, the GUI may be replaced by an NME application. Which
means a (partial) port to HaXe. The main reason is the graphics capabilities
of NME: vector and bitmap animations, interaction, opengl.

In browser this may mean the client turns HTML5, or if Flash would be the
only alternative maybe native binaries using the cross-platform SDL 
graphics library. As HaXe/NME has its own remoting facilities, perhaps the 
server can run from neko or native linux too, but twisted will probably 
be better.

Status
------
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


