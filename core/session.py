import random
import threading
import uuid
import time
from core.job import Job

class Session(object):
    SESSION_ID = 0
    SESSION_ID_LOCK = threading.Lock()

    DEAD = 0
    ALIVE = 1

    ELEVATED_UNKNOWN = -1
    ELEVATED_FALSE = 0
    ELEVATED_TRUE = 1

    def __init__(self, stager, ip, user_agent):
        with Session.SESSION_ID_LOCK:
            self.id = Session.SESSION_ID
            Session.SESSION_ID += 1

        self.key = uuid.uuid4().hex
        self.jobs = []
        self.killed = False

        self.os = ""
        self.elevated = self.ELEVATED_UNKNOWN
        self.user = ""
        self.computer = ""
        self.dc = ""
        self.domain = ""
        self.arch = ""
        self.realcwd = ""

        self.ip = ip
        self.user_agent = user_agent

        self.stager = stager
        self.shell = stager.shell
        self.status = Session.ALIVE
        self.first_seen = time.time()
        self.update_active()

        self.shell.print_good(
            "Zombie %d: Staging new connection (%s)" % (self.id, self.ip))


    def parse_user_info(self, data):
        try:
            self.shell.print_verbose("session::parse_user_info() - %s" % data)

            if self.os != "" or self.user != "" or self.computer != "" or self.elevated != self.ELEVATED_UNKNOWN:
                return False

            try:
                data = data.decode().split("~~~")
            except UnicodeDecodeError:
                try:
                    data = data.decode('utf-8').split("~~~")
                except UnicodeDecodeError:
                    data = data.decode('unicode-escape').split("~~~")

            if len(data) != 6:
                return False

            self.user = data[0]
            self.domain = data[0].split("\\")[0]
            self.elevated = self.ELEVATED_TRUE if "*" in data[0] else self.ELEVATED_FALSE
            self.computer = data[1]
            self.os = data[2]
            self.dc = data[3] if data[3] else "Unknown"
            #self.dc = data[3].split("___")[0] if data[3] else "Unknown"
            #self.fqdn = data[3].split("___")[1]
            #self.netbios = data[0].split("\\")[0].lower()
            #if not (self.fqdn, self.netbios) in self.shell.domain_info:
            #    self.shell.domain_info[(self.fqdn, self.netbios)] = {}
                #self.shell.domain_admins[(self.fqdn, self.netbios)] = data[3].split("___")[2:]
            if data[4] != "Unknown":
                self.arch = "64" if data[4] == "AMD64" else "32"
            else:
                self.arch = data[4]
            self.realcwd = data[5].rstrip()
        except Exception as e:
            self.shell.print_warning("parsing error")
            self.shell.print_warning(repr(e))

        self.shell.print_good(
            "Zombie %d: %s @ %s -- %s" % (self.id, self.user, self.computer, self.os))


    def kill(self):
        self.killed = True
        self.set_dead()

    def set_dead(self):
        if self.status != self.DEAD:
            self.status = self.DEAD
            self.shell.print_warning("Zombie %d: Timed out." % self.id)

    def set_reconnect(self):
        if not self.killed:
            self.shell.print_good("Zombie %d: Re-connected." % self.id)
            self.status = self.ALIVE

    def update_active(self):
        self.last_active = time.time()

    def get_job(self, job_key):
        for job in self.jobs:
            if job.key == job_key:
                self.shell.print_verbose("session::get_job() - fetched job_key = %s" % (job_key))
                return job

        self.shell.print_verbose("session::get_job() - NOT FOUND job_key = %s" % (job_key))
        return None

    def get_created_job(self):
        shell = self.stager.shell

        for job in self.jobs:
            #if job.completed != Job.COMPLETE:
            if job.completed == Job.CREATED:
                self.shell.print_verbose("session::get_created_job - fetched job.key = %s" % (job.key))
                return job

        return None
