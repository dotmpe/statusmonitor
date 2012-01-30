"""


"""
from txjsonrpc.web import jsonrpc
from twisted.web import server
from twisted.internet import reactor

class RPCServer(jsonrpc.JSONRPC):
    """
    An example object to be published.
    """
    def jsonrpc_list_screens(self):
        """
        Return sum of arguments.
        """
        return a + b



reactor.listenTCP(7080, server.Site(RPCServer()))
reactor.run()

from twisted.internet import reactor, protocol


class Protocol(protocol.Protocol):

    def connectionMade(self):
        self.transport.write(" ")
        self.transport.loseConnection()


class Factory(protocol.ServerFactory):

    protocol = Protocol

    def __init__(self, script):
        self.script = script
    s = datastore.get_session(rc.dbref)
        w = Worker.fetch(jobid)


if __name__ == 'main':

    options = parser_argv()

    jobid = options.jobid

    if Worker.isRunning(jobid):
        log = Worker.getLogPath(jobid)
    else:
        w = Worker.fetch(jobid)
        w.start()
        log = w.getLogPath() 

    factory = LogParserServerFactory(log)
    port = reactor.listenTCP(port, factory, interface=options.iface)
    reactor.run()



