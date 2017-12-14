DESCRIPTION = "shows collected credentials"

def autocomplete(shell, line, text, state):
    pass

def help(shell):
    shell.print_plain("")
    shell.print_plain("Use %s for full credential details" % (shell.colors.colorize("creds -a", shell.colors.BOLD)))
    shell.print_plain("Use %s for specific user credentials" % (shell.colors.colorize("creds -u user1,user2,user3,...", shell.colors.BOLD)))
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

def execute(shell, cmd):
    nodupes = [dict(tmp) for tmp in set(tuple(item.items()) for item in shell.creds)]
    shell.creds = nodupes

    splitted = cmd.strip().split(" ")

    if len(splitted) > 1:
        if splitted[1] == "-a":
            print_creds_detailed(shell)
        elif splitted[1] == "-u":
            print_creds_detailed(shell, splitted[2])
        else:
            shell.print_plain("Error: Unknown option '"+splitted[1]+"'")
    else:
        print_creds(shell)
