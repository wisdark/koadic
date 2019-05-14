DESCRIPTION = "shows info about repeating jobs"

def autocomplete(shell, line, text, state):
    pass

def help(shell):
    shell.print_plain("")
    # shell.print_plain("Use %s to view job results (if any)" % (shell.colors.colorize("jobs JOB_ID", shell.colors.BOLD)))
    # shell.print_plain("")

def print_repatjob(shell, id):
    for job in shell.repeatjobs:
        if job == id:
            for o in shell.repeatjobs[id][6].options:
                if not o.hidden:
                    shell.print_plain(str([o.name, o.value]))

            # print([[s.name, s.value] for s in shell.repeatjobs[id][6].options if not s.hidden])

def print_all_repeatjobs(shell):
    formats = "\t{0:<4}{1:<40}{2:<7}{3:<5}{4:<7}"

    shell.print_plain("")

    shell.print_plain(formats.format("ID", "NAME", "TTR", "CR", "TBR"))
    shell.print_plain(formats.format("-"*2, "-"*4, "-"*5, "-"*3, "-"*5))
    for rjob in shell.repeatjobs:
        rjobobj = shell.repeatjobs[rjob]
        shell.print_plain(formats.format(rjob, rjobobj[5], str(rjobobj[0]), str(rjobobj[1]-1), str(rjobobj[4])))

    shell.print_plain("")

def kill_repeatjob(shell, id):
    tmp = shell.repeatjobs
    if id in tmp:
        del tmp[id]
        shell.repeatjobs = tmp
        shell.print_good("Repeating job '"+id+"' has been deleted.")
    else:
        shell.print_error("Repeating job '"+id+"' does not exist.")

def killall_repeatjobs(shell):
    shell.repeatjobs = {}
    shell.print_good("All repeating jobs have been deleted.")

def execute(shell, cmd):

    splitted = cmd.split()

    if len(splitted) > 1:
        id = splitted[-1]
        flag = splitted[1]
        if len(splitted) > 2:
            if flag == "-k":
                kill_repeatjob(shell, id)
                return
            else:
                shell.print_error("Unknown option '%s'" % flag)
                return

        else:
            if flag == "-K":
                killall_repeatjobs(shell)
                return
            else:
                print_repatjob(shell, id)
                return

    print_all_repeatjobs(shell)
