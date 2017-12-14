DESCRIPTION = "shows collected credentials"

def autocomplete(shell, line, text, state):
    pass

def help(shell):
    pass

def print_creds(shell):
    nodupes = [dict(tmp) for tmp in set(tuple(item.items()) for item in shell.creds)]
    shell.creds = nodupes
    formats = "\t{0:<20}{1:<20}{2:<25}{3:<20}"

    shell.print_plain("")

    shell.print_plain(formats.format("USERNAME", "DOMAIN", "PASSWORD", "HASH"))
    shell.print_plain(formats.format("-"*8,  "-"*6, "-"*8, "-"*4))
    for cred in shell.creds:
        shell.print_plain(formats.format(cred["Username"], cred["Domain"], cred["Password"], cred["Hash"]))

    shell.print_plain("")

def execute(shell, cmd):

    splitted = cmd.strip().split(" ")

    print_creds(shell)
