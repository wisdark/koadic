try
{
    Koadic.http.upload("~RFILEF~", "data");
}
catch (e)
{
    Koadic.work.error(e);
}

Koadic.exit();
