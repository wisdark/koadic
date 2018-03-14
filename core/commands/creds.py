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
    formats = "\t{0:17}{1:<20}{2:<20}{3:<25}{4:<42}{5:<6}"
    shell.print_plain("")

    shell.print_plain(formats.format("IP", "USERNAME", "DOMAIN", "PASSWORD", "HASH", "HASH TYPE"))
    shell.print_plain(formats.format("--", "-"*8,  "-"*6, "-"*8, "-"*4, "-"*9))
    for cred in shell.creds:
        tmppass = cred["Password"]
        if len(cred["Password"]) > 23:
            tmppass = cred["Password"][:20] + "..."
        if cred["Username"][-1] == '$':
            continue
        shell.print_plain(formats.format(cred["IP"], cred["Username"], cred["Domain"], tmppass, cred["Hash"], cred["HashType"]))

    shell.print_plain("")

def print_creds_detailed(shell, users="*"):
    shell.print_plain("")

    for cred in shell.creds:
        if users == "*" or cred["Username"].lower() in [u.lower() for u in users.split(",")]:
            shell.print_plain("IP: "+cred["IP"])
            shell.print_plain("USERNAME: "+cred["Username"])
            shell.print_plain("DOMAIN: "+cred["Domain"])
            shell.print_plain("PASSWORD: "+cred["Password"])
            shell.print_plain("HASH: "+cred["Hash"])
            shell.print_plain("HASH TYPE: "+cred["HashType"])
            shell.print_plain("")

def print_creds_das(shell, domain):
    domains = [j for i in shell.domain_info.keys() for j in i]
    if not domain.lower() in domains:
        shell.print_error("Supplied domain not known")
        return

    domain_key = [i for i in shell.domain_info.keys() if domain.lower() in i][0]
    alt_domain = [i for i in domain_key if i != domain][0]

    if not "Domain Admins" in shell.domain_info[domain_key]:
        shell.print_error("Domain Admins not gathered for target domain. Please run implant/gather/enum_domain_info")
        return

    formats = "\t{0:17}{1:<20}{2:<20}{3:<25}{4:<42}{5:<6}"
    shell.print_plain("")

    shell.print_plain(formats.format("IP", "USERNAME", "DOMAIN", "PASSWORD", "HASH", "HASH TYPE"))
    shell.print_plain(formats.format("--", "-"*8,  "-"*6, "-"*8, "-"*4, "-"*9))
    for cred in shell.creds:
        tmppass = cred["Password"]
        if len(cred["Password"]) > 23:
            tmppass = cred["Password"][:20] + "..."
        if cred["Username"].lower() in shell.domain_info[domain_key]["Domain Admins"] and (cred["Domain"].lower() == domain.lower() or cred["Domain"].lower() == alt_domain.lower()):
            shell.print_plain(formats.format(cred["IP"], cred["Username"], cred["Domain"], tmppass, cred["Hash"], cred["HashType"]))

    shell.print_plain("")

def condense_creds(shell):
    nodupes = [dict(tmp) for tmp in set(tuple(item.items()) for item in shell.creds)]
    tmp = list(nodupes)
    for c in tmp:
        if c["Username"] == "(null)" or c["Password"] == "(null)":
            nodupes.remove(c)

    creds = list(nodupes)
    return creds

def export_creds(shell):
    export = open('/tmp/creds.txt', 'w')
    for cred in shell.creds:
        export.write("IP: "+cred["IP"]+"\n")
        export.write("USERNAME: "+cred["Username"]+"\n")
        export.write("DOMAIN: "+cred["Domain"]+"\n")
        export.write("PASSWORD: "+cred["Password"]+"\n")
        export.write("HASH: "+cred["Hash"]+"\n")
        export.write("HASH TYPE: "+cred["HashType"]+"\n")
        export.write("\n")
    export.close()
    shell.print_good("Credential store written to /tmp/creds.txt")

def execute(shell, cmd):
    shell.creds = condense_creds(shell)

    splitted = cmd.strip().split(" ")

    if len(splitted) > 1:
        if splitted[1] == "-a":
            print_creds_detailed(shell)
        elif splitted[1] == "-u":
            print_creds_detailed(shell, splitted[2])
        elif splitted[1] == "-x":
            export_creds(shell)
        elif splitted[1] == "-d":
            if len(splitted) < 3:
                shell.print_good("Gathered domains")
                for d in shell.domain_info:
                    shell.print_plain("\tLong: "+d[0]+", Short: "+d[1])
            else:
                print_creds_das(shell, splitted[2])

        # need to get rid of this
        elif splitted[1] == "test":
            print(shell.domain_info)
        else:
            shell.print_error("Unknown option '"+splitted[1]+"'")
    else:
        if shell.creds:
            print_creds(shell)
        else:
            shell.print_error("No credentials have been gathered yet")
