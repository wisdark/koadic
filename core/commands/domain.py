DESCRIPTION = "shows collected domain information"

def autocomplete(shell, line, text, state):
    pass

def help(shell):
    shell.print_plain("")
    shell.print_plain("Use %s for full domain details" % (shell.colors.colorize("domain -a DOMAIN", shell.colors.BOLD)))
    shell.print_plain("Use %s for domain admins" % (shell.colors.colorize("domain -d DOMAIN", shell.colors.BOLD)))
    shell.print_plain("Use %s for domain users" % (shell.colors.colorize("domain -u DOMAIN", shell.colors.BOLD)))
    shell.print_plain("Use %s for domain password policy" % (shell.colors.colorize("domain -p DOMAIN", shell.colors.BOLD)))
    shell.print_plain("Use %s for domain controllers" % (shell.colors.colorize("domain -c DOMAIN", shell.colors.BOLD)))
    shell.print_plain("Use %s to run implant/gather/enum_domain_info on a zombie" % (shell.colors.colorize("domain -z ZOMBIE_ID", shell.colors.BOLD)))
    shell.print_plain("Use %s to export domain information" % (shell.colors.colorize("domain -x [DOMAIN]", shell.colors.BOLD)))
    shell.print_plain("")

def print_domains(shell):
    shell.print_plain("")
    shell.print_plain("Available Domains:")
    for domain in shell.domain_info:
        shell.print_plain("\tFQDN: "+domain[0]+" | NetBIOS: "+domain[1])
    shell.print_plain("")

def print_domain_detailed(shell, domain):
    domains = [j for i in shell.domain_info for j in i]
    if not domain.lower() in domains:
        shell.print_error("Supplied domain not known")
        return

    print_domain_admins(shell, domain)
    print_domain_users(shell, domain)
    print_domain_password_policy(shell, domain)
    print_domain_controllers(shell, domain)

def print_domain_admins(shell, domain):
    domains = [j for i in shell.domain_info for j in i]
    if not domain.lower() in domains:
        shell.print_error("Supplied domain not known")
        return

    domain_key = [i for i in shell.domain_info if domain.lower() in i][0]

    if not "Domain Admins" in shell.domain_info[domain_key]:
        shell.print_error("Domain Admins not gathered for target domain. Please run implant/gather/enum_domain_info")
        return

    das = shell.domain_info[domain_key]["Domain Admins"]

    shell.print_plain("")
    shell.print_plain("Domain Admins")
    shell.print_plain("-------------")
    shell.print_plain("\n".join(["   ".join(da_row) for da_row in [das[x:x+4] for x in range(0, len(das), 4)]]))

    shell.print_plain("")

def print_domain_users(shell, domain):
    domains = [j for i in shell.domain_info for j in i]
    if not domain.lower() in domains:
        shell.print_error("Supplied domain not known")
        return

    domain_key = [i for i in shell.domain_info if domain.lower() in i][0]

    if not "Domain Users" in shell.domain_info[domain_key]:
        shell.print_error("Domain Users not gathered for target domain. Please run implant/gather/enum_domain_info")
        return

    users = shell.domain_info[domain_key]["Domain Users"]

    shell.print_plain("")
    shell.print_plain("Domain Users")
    shell.print_plain("------------")
    shell.print_plain("\n".join(["   ".join(user_row) for user_row in [users[x:x+4] for x in range(0, len(users), 4)]]))

    shell.print_plain("")

def print_domain_password_policy(shell, domain):
    domains = [j for i in shell.domain_info for j in i]
    if not domain.lower() in domains:
        shell.print_error("Supplied domain not known")
        return

    domain_key = [i for i in shell.domain_info if domain.lower() in i][0]

    if not "Password Policy" in shell.domain_info[domain_key]:
        shell.print_error("Password Policy not gathered for target domain. Please run implant/gather/enum_domain_info")
        return

    shell.print_plain("")
    shell.print_plain("Password Policy")
    policy_string =  "\tForce user logoff how long after time expires?:       %s\n"
    policy_string += "\tMinimum password age (days):                          %s\n"
    policy_string += "\tMaximum password age (days):                          %s\n"
    policy_string += "\tMinimum password length:                              %s\n"
    policy_string += "\tLength of password history maintained:                %s\n"
    policy_string += "\tLockout threshold:                                    %s\n"
    policy_string += "\tLockout duration (minutes):                           %s\n"
    policy_string += "\tLockout observation window (minutes):                 %s\n"
    policy_string = policy_string % tuple(shell.domain_info[domain_key]["Password Policy"])

    shell.print_plain(policy_string)

    shell.print_plain("")

def print_domain_controllers(shell, domain):
    domains = [j for i in shell.domain_info for j in i]
    if not domain.lower() in domains:
        shell.print_error("Supplied domain not known")
        return

    domain_key = [i for i in shell.domain_info if domain.lower() in i][0]

    if not "Domain Controllers" in shell.domain_info[domain_key]:
        shell.print_error("Domain Controllers not gathered for target domain. Please run implant/gather/enum_domain_info")
        return

    shell.print_plain("")
    shell.print_plain("Domain Controllers")
    for dc in shell.domain_info[domain_key]["Domain Controllers"]:
        shell.print_plain("\tDC: "+dc[0]+" ("+dc[1]+")")

    shell.print_plain("")

def export_domain_info(shell, domain="*"):
    if domain != "*":
        domains = [j for i in shell.domain_info for j in i]
        if not domain.lower() in domains:
            shell.print_error("Supplied domain not known")
            return

    if domain == "*":
        export = open('/tmp/domain_info.txt', 'w')
        domain_key = "*"
    else:
        export = open('/tmp/'+domain+'_domain_info.txt', 'w')
        domain_key = [i for i in shell.domain_info if domain.lower() in i][0]

    for key in shell.domain_info:
        if domain == "*" or domain_key == key:
            export.write(str(key)+"\n")
            for subkey in shell.domain_info[key]:
                export.write(str(key)+"-"+subkey+"\n")
                for value in shell.domain_info[key][subkey]:
                    export.write(str(value)+"\n")
                export.write("/"+str(key)+"-"+subkey+"\n")
            export.write("/"+str(key)+"\n")


    shell.print_good("Domain info written to "+export.name)
    export.close()

def execute(shell, cmd):

    splitted = cmd.split()

    if len(splitted) > 1 and splitted[1] == "-z":
        if len(splitted) < 3:
            shell.print_error("Need to provide a zombie ID!")
            return
        plugin = shell.plugins["implant/gather/enum_domain_info"]
        old_zombie = plugin.options.get("ZOMBIE")
        plugin.options.set("ZOMBIE", splitted[2])
        plugin.run()
        plugin.options.set("ZOMBIE", old_zombie)
        return

    if shell.domain_info:
        if len(splitted) > 2:
            if splitted[1] == "-a":
                print_domain_detailed(shell, splitted[2])
            elif splitted[1] == "-d":
                print_domain_admins(shell, splitted[2])
            elif splitted[1] == "-u":
                print_domain_users(shell, splitted[2])
            elif splitted[1] == "-p":
                print_domain_password_policy(shell, splitted[2])
            elif splitted[1] == "-c":
                print_domain_controllers(shell, splitted[2])
            elif splitted[1] == "-x":
                export_domain_info(shell, splitted[2])
            else:
                shell.print_error("Unknown option '"+splitted[1]+"'")
        elif len(splitted) > 1 and splitted[1] == "-x":
            export_domain_info(shell)
        else:
            print_domains(shell)
    else:
        shell.print_error("No domain information gathered. Please run implant/gather/enum_domain_info.")

