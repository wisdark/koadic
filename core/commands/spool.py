DESCRIPTION = "write output to a file"

def autocomplete(shell, line, text, state):
    pass

def help(shell):
    shell.print_plain("")
    shell.print_plain("Use %s to spool to /tmp/koadic.spool" % (shell.colors.colorize("spool on", shell.colors.BOLD)))
    shell.print_plain("Use %s to spool to a defined file" % (shell.colors.colorize("spool FILEPATH", shell.colors.BOLD)))
    shell.print_plain("Use %s to stop spooling" % (shell.colors.colorize("spool off", shell.colors.BOLD)))
    shell.print_plain("")

def execute(shell, cmd):

    splitted = cmd.split()

    if len(splitted) > 1:
        option = splitted[1]
        if option == 'on':
            shell.spool = '/tmp/koadic.spool'
            shell.print_status("Spooling to /tmp/koadic.spool...")
        elif option == 'off':
            if shell.spool:
                shell.spool = False
                shell.print_status("Spooling stopped...")
        else:
            shell.spool = option
            shell.print_status("Spooling to "+option+"...")
    else:
        help(shell)
