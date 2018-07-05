DESCRIPTION = "shows collected credentials"

def autocomplete(shell, line, text, state):
    pass

def help(shell):
    shell.print_plain("")
    shell.print_plain("Use %s for full credential details" % (shell.colors.colorize("creds -a", shell.colors.BOLD)))
    shell.print_plain("Use %s for specific user credentials" % (shell.colors.colorize("creds -u user1,user2,user3,...", shell.colors.BOLD)))
    shell.print_plain("Use %s for domain admin credentials" % (shell.colors.colorize("creds -d domain", shell.colors.BOLD)))
    shell.print_plain("Use %s to write credentials to a file" % (shell.colors.colorize("creds -x", shell.colors.BOLD)))
    shell.print_plain("")

def print_creds(shell):
    formats = "\t{0:9}{1:17}{2:<20}{3:<20}{4:<25}{5:<42}"
    shell.print_plain("")

    shell.print_plain(formats.format("Cred ID", "IP", "USERNAME", "DOMAIN", "PASSWORD", "NTLM"))
    shell.print_plain(formats.format("-"*7, "--", "-"*8,  "-"*6, "-"*8, "-"*4))
    for key in shell.creds_keys:
        tmpuser = shell.creds[key]["Username"]
        if len(tmpuser) > 18:
            tmpuser = tmpuser[:15] + "..."
        tmpdomain = shell.creds[key]["Domain"]
        if len(tmpdomain) > 18:
            tmpdomain = tmpdomain[:15] + "..."
        tmppass = shell.creds[key]["Password"]
        if len(tmppass) > 23:
            tmppass = tmppass[:20] + "..."
        if shell.creds[key]["Username"][-1] == '$' or (not shell.creds[key]["Password"] and not shell.creds[key]["NTLM"]) or shell.creds[key]["NTLM"] == '31d6cfe0d16ae931b73c59d7e0c089c0':
            continue
        shell.print_plain(formats.format(str(shell.creds_keys.index(key)), shell.creds[key]["IP"], tmpuser, tmpdomain, tmppass, shell.creds[key]["NTLM"]))

    shell.print_plain("")

def print_creds_detailed(shell, users="*"):
    shell.print_plain("")

    for key in shell.creds_keys:
        if (users == "*" or
            shell.creds[key]["Username"].lower() in [u.lower() for u in users.split(",")] or
            str(shell.creds_keys.index(key)) in [u.lower() for u in users.split(",")]):

            shell.print_plain("Cred ID: "+str(shell.creds_keys.index(key)))
            shell.print_plain("IP: "+shell.creds[key]["IP"])
            shell.print_plain("USERNAME: "+shell.creds[key]["Username"])
            shell.print_plain("DOMAIN: "+shell.creds[key]["Domain"])
            shell.print_plain("PASSWORD: "+shell.creds[key]["Password"]+" "+" ".join(shell.creds[key]["Extra"]["Password"]))
            shell.print_plain("NTLM: "+shell.creds[key]["NTLM"]+" "+" ".join(shell.creds[key]["Extra"]["NTLM"]))
            shell.print_plain("LM: "+shell.creds[key]["LM"]+" "+" ".join(shell.creds[key]["Extra"]["LM"]))
            shell.print_plain("SHA1: "+shell.creds[key]["SHA1"]+" "+" ".join(shell.creds[key]["Extra"]["SHA1"]))
            shell.print_plain("DCC: "+shell.creds[key]["DCC"]+" "+" ".join(shell.creds[key]["Extra"]["DCC"]))
            shell.print_plain("DPAPI: "+shell.creds[key]["DPAPI"]+" "+" ".join(shell.creds[key]["Extra"]["DPAPI"]))
            shell.print_plain("")

def print_creds_das(shell, domain):
    domains = [j for i in shell.domain_info for j in i]
    if not domain.lower() in domains:
        shell.print_error("Supplied domain not known")
        return

    domain_key = [i for i in shell.domain_info if domain.lower() in i][0]
    alt_domain = [i for i in domain_key if i != domain][0]

    if not "Domain Admins" in shell.domain_info[domain_key]:
        shell.print_error("Domain Admins not gathered for target domain. Please run implant/gather/enum_domain_info")
        return

    das = shell.domain_info[domain_key]["Domain Admins"]

    formats = "\t{0:9}{1:17}{2:<20}{3:<20}{4:<25}{5:<42}"
    shell.print_plain("")

    shell.print_plain(formats.format("Cred ID", "IP", "USERNAME", "DOMAIN", "PASSWORD", "HASH"))
    shell.print_plain(formats.format("-"*7, "--", "-"*8,  "-"*6, "-"*8, "-"*4))
    for key in shell.creds_keys:
        tmppass = shell.creds[key]["Password"]
        if len(tmppass) > 23:
            tmppass = tmppass[:20] + "..."
        creduser = shell.creds[key]["Username"]
        creddomain = shell.creds[key]["Domain"]
        credntlm = shell.creds[key]["NTLM"]
        if creduser.lower() in das and (creddomain.lower() == domain.lower() or creddomain.lower() == alt_domain.lower()) and (tmppass or credntlm):
            shell.print_plain(formats.format(str(shell.creds_keys.index(key)), shell.creds[key]["IP"], creduser, creddomain, tmppass, shell.creds[key]["NTLM"]))

    shell.print_plain("")

def condense_creds(shell):
    bad_keys = []
    for key in shell.creds_keys:
        if shell.creds[key]["Username"] == "(null)":
            bad_keys.append(key)

    if bad_keys:
        new_creds = dict(shell.creds)
        for key in bad_keys:
            del new_creds[key]
            shell.creds_keys.remove(key)
        shell.creds = new_creds

def export_creds(shell):
    export = open('/tmp/creds.txt', 'w')
    for key in shell.creds_keys:
        export.write("IP: "+shell.creds[key]["IP"]+"\n")
        export.write("USERNAME: "+shell.creds[key]["Username"]+"\n")
        export.write("DOMAIN: "+shell.creds[key]["Domain"]+"\n")
        export.write("PASSWORD: "+shell.creds[key]["Password"]+" "+" ".join(shell.creds[key]["Extra"]["Password"])+"\n")
        export.write("NTLM: "+shell.creds[key]["NTLM"]+" "+" ".join(shell.creds[key]["Extra"]["NTLM"])+"\n")
        export.write("LM: "+shell.creds[key]["LM"]+" "+" ".join(shell.creds[key]["Extra"]["LM"])+"\n")
        export.write("SHA1: "+shell.creds[key]["SHA1"]+" "+" ".join(shell.creds[key]["Extra"]["SHA1"])+"\n")
        export.write("DCC: "+shell.creds[key]["DCC"]+" "+" ".join(shell.creds[key]["Extra"]["DCC"])+"\n")
        export.write("DPAPI: "+shell.creds[key]["DPAPI"]+" "+" ".join(shell.creds[key]["Extra"]["DPAPI"])+"\n")
        export.write("\n")
    export.close()
    shell.print_good("Credential store written to /tmp/creds.txt")

def execute(shell, cmd):
    condense_creds(shell)

    splitted = cmd.split()

    if len(splitted) > 1:
        if splitted[1] == "-a":
            print_creds_detailed(shell)
        elif splitted[1] == "-u":
            print_creds_detailed(shell, splitted[2])
        elif splitted[1] == "-x":
            export_creds(shell)
        elif splitted[1] == "-d":
            if shell.domain_info:
                if len(splitted) < 3:
                    shell.print_good("Gathered domains")
                    for d in shell.domain_info:
                        shell.print_plain("\tLong: "+d[0]+", Short: "+d[1])
                else:
                    print_creds_das(shell, splitted[2])
            else:
                shell.print_error("No domain information gathered. Please run implant/gather/enum_domain_info.")

        else:
            shell.print_error("Unknown option '"+splitted[1]+"'")
    else:
        if shell.creds:
            print_creds(shell)
        else:
            shell.print_error("No credentials have been gathered yet")
