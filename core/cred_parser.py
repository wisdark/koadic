class CredParse(object):

    def __init__(self, job):
        self.job = job
        self.shell = job.shell
        self.session = job.session

    def parse_mimikatz(self, data):
        full_data = data
        data = data.split("mimikatz(powershell) # ")[1]
        if "token::elevate" in data and "Impersonated !" in data:
            self.job.print_good("token::elevate -> got SYSTEM!")
            return

        if "privilege::debug" in data and "OK" in data:
            self.job.print_good("privilege::debug -> got SeDebugPrivilege!")
            return

        if "ERROR kuhl_m_" in data:
            self.job.error("0", data.split("; ")[1].split(" (")[0], "Error", data)
            self.job.errstat = 1
            return

        if "Authentication Id :" in data and "sekurlsa::logonpasswords" in data:
            print("AWWWWYEE")
            from tabulate import tabulate
            nice_data = data.split('\n\n')
            cred_headers = ["msv","tspkg","wdigest","kerberos","ssp","credman"]
            msv_all = []
            tspkg_all = []
            wdigest_all = []
            kerberos_all = []
            ssp_all = []
            credman_all = []
            for section in nice_data:
                if 'Authentication Id' in section:
                    msv = collections.OrderedDict()
                    tspkg = collections.OrderedDict()
                    wdigest = collections.OrderedDict()
                    kerberos = collections.OrderedDict()
                    ssp = collections.OrderedDict()
                    credman = collections.OrderedDict()

                    for index, cred_header in enumerate(cred_headers):
                        cred_dict = locals().get(cred_header)
                        cred_sec1 = section.split(cred_header+" :\t")[1]
                        if index < len(cred_headers)-1:
                            cred_sec = cred_sec1.split("\t"+cred_headers[index+1]+" :")[0].splitlines()
                        else:
                            cred_sec = cred_sec1.splitlines()

                        for line in cred_sec:
                            if '\t *' in line:
                                cred_dict[line.split("* ")[1].split(":")[0].rstrip()] = line.split(": ")[1].split("\n")[0]
                        if cred_dict:
                            cred_list = locals().get(cred_header+"_all")
                            cred_list.append(cred_dict)

            for cred_header in cred_headers:
                cred_list = locals().get(cred_header+"_all")
                tmp = [collections.OrderedDict(t) for t in set([tuple(d.items()) for d in cred_list])]
                del cred_list[:]
                cred_list.extend(tmp)

            parsed_data = "Results\n\n"

            for cred_header in cred_headers:
                banner = cred_header+" credentials\n=================\n\n"
                cred_dict = locals().get(cred_header+"_all")
                if not cred_dict:
                    continue
                cred_dict = sorted(cred_dict, key=lambda k: k['Username'])
                keys = []
                [[keys.append(k) for k in row.keys() if k not in keys] for row in cred_dict]
                for cred in cred_dict:
                    c = {}
                    c["IP"] = self.session.ip
                    c["Username"] = cred["Username"]
                    c["Domain"] = cred["Domain"]
                    c["Password"] = ""
                    if "Password" in keys:
                        c["Password"] = cred["Password"]

                    c["Hash"] = ""
                    c["HashType"] = ""
                    if "NTLM" in keys:
                        c["Hash"] = cred["NTLM"]
                        c["HashType"] = "NTLM"
                    elif "SHA1" in keys:
                        c["Hash"] = cred["SHA1"]
                        c["HashType"] = "SHA1"

                    self.shell.creds.append(c)
                separators = collections.OrderedDict([(k, "-"*len(k)) for k in keys])
                cred_dict = [separators] + cred_dict
                parsed_data += banner
                parsed_data += tabulate(cred_dict, headers="keys", tablefmt="plain")
                parsed_data += "\n\n"

            return parsed_data
        return data
