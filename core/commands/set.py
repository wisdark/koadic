import os

DESCRIPTION = "sets a variable for the current module"

def autocomplete(shell, line, text, state):

    env = shell.plugins[shell.state]
    # todo, here we can provide some defaults for bools/enums? i.e. True/False
    if len(line.split()) > 1:
        optionname = line.split()[1]
        if optionname in [x.name for x in env.options.options if not x.hidden]:
            option = [x for x in env.options.options if x.name == optionname][0]
            options = []
            if option.boolean:
                options = [x for x in ["true", "false"] if x.upper().startswith(text.upper())]
            if option.file:
                options = filepaths(text)
            if option.implant:
                pass
            if option.enum:
                options = [x for x in option.enum if x.upper().startswith(text.upper())]
            if options:
                return options[state]

    options = [x.name + " " for x in env.options.options if x.name.upper().startswith(text.upper()) and not x.hidden]
    options += [x.alias + " " for x in env.options.options if x.alias.upper().startswith(text.upper()) and not x.hidden and x.alias]

    try:
        return options[state]
    except:
        return None

def filepaths(text):
    if os.path.isfile(text):
        return None
    res = []
    if text:
        d = os.path.dirname(text)
    else:
        d = "."
    for name in os.listdir(d):
        path = os.path.join(d,name)
        if os.path.isdir(path):
            path += os.sep
        if (text and path.startswith(text)) or not text:
            res.append(path)

    return res

def help(shell):
    pass

def execute(shell, cmd):
    env = shell.plugins[shell.state]

    splitted = cmd.split()
    if len(splitted) > 1:
        key = splitted[1].upper()

        value = env.options.get(key)
        if value != None:

            # if it's >2, we set the third argument
            if len(splitted) > 2:
                value = cmd.split(None, 2)[2]
                if not env.options.set(key, value):
                    shell.print_error("That value is invalid")
                    return

            shell.print_good("%s => %s" % (key, value))
        else:
            shell.print_error("Option '%s' not found." % (key))
