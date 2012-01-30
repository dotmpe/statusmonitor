"""
While the worker is running, it should serve until the current log line.
Normally a Worker will be invoked as part of a Job (a scheduled script)
by the local cron system.
"""

from __future__ import print_function
import datetime
import sys
from subprocess import PIPE, Popen
from threading  import Thread

import rc
import datastore
from datastore import Job, get_session

from Queue import Queue, Empty

ON_POSIX = 'posix' in sys.builtin_module_names


def enqueue_output(out, queue):
    for line in iter(out.readline, ''):
        queue.put(line)
    out.close()


class Worker(object):

    def __init__(self, script, matchbox):
        self.script = script
        self.matchbox = matchbox
        self.p = Popen([self.script], 
            stdout=PIPE, bufsize=1, close_fds=ON_POSIX)

    @staticmethod
    def is_running(dbms, jobid):
        q = dbms.query(Job).filter(Job.id == jobid)
        try:
            job = q.one()
        except:
            return False
        return job.is_running

    @staticmethod
    def fetch(dbms, jobid):
        assert not Worker.is_running(dbms, jobid)
        q = dbms.query(Job).filter(Job.id == jobid)
        job = q.one()
        extracts = [re.compile(xt.regex) for xt in job.script.extracts]
        return Worker(job.script.path, extracts)

    def run(self:
        start_time = datetime.now()
        self.q = Queue()
        t = Thread(target=enqueue_output, args=(self.p.stdout, self.q))
        t.daemon = True # thread dies with the program
        t.start()

    def read(self):
        try:  
            line = self.q.get_nowait() # or q.get(timeout=.1)
        except Empty:
            return
        else:
            print(line, end='')


class LogReader(object):
    
    def __init__(self):
        pass


if __name__ == '__main__':
    jobid = None
    dbms = get_session(rc.dbref)

    if not Worker.is_running(dbms, jobid):
        w = Worker.fetch(dbms, jobid)
        w.run()
        LogReader(w).run()
        #reactor.callWhenRunning(w.read())
    else:
        l = open(Worker.getLogPath(jobid))
        LogReader(l).run()


