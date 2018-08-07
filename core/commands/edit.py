DESCRIPTION = "shell out to an editor for the current module"

def autocomplete(shell, line, text, state):
    return None

def help(shell):
    pass

def execute(shell, cmd):
    import subprocess, os

    if not os.environ['EDITOR']:
        shell.print_error("$EDITOR env variable not setting, falling back to vi!")
        editor = 'vi'
    else:
        editor = os.environ['EDITOR']

    py_file = "modules/"+shell.state+".py"
    js_file = "data/"+shell.state+".js"
    vbs_file = "data/"+shell.state+".vbs"

    splitted = cmd.split()

    if len(splitted) > 1:
        ftype = splitted[1].lower()
        if ftype == "py" or ftype == "python":
            file = py_file
        elif ftype == "js" or ftype == "javascript":
            file = js_file
        elif ftype == "vbs" or ftype == "vbscript":
            file = vbs_file

        editcmd = [editor, file]
    else:
        editcmd = [editor, py_file]
    
    subprocess.call(editcmd)
    shell.run_command('load')
