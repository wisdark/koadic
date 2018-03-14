function ParseUsers(results)
{
    var retstring = "";
    var parse1 = results.split("-------\r\n")[1].split("The command completed")[0];
    var parse2 = parse1.split("\r\n");
    var tmp = [];
    for(var i = 0; i < parse2.length; i++)
    {
        tmp = parse2[i].split(" ");
        for(var j = 0; j < tmp.length; j++)
        {
            if(tmp[j])
            {
                retstring += tmp[j].toLowerCase() + "___";
            }
        }
    }
    return retstring;
}

function ParsePasswordPolicy(results)
{
    var retstring = "";
    retstring += results.split("time expires?:")[1].split("\r\n")[0].replace(/^\s+|\s+$/g, '') + "___";
    retstring += results.split("Minimum password age (days):")[1].split("\r\n")[0].replace(/^\s+|\s+$/g, '') + "___";
    retstring += results.split("Maximum password age (days):")[1].split("\r\n")[0].replace(/^\s+|\s+$/g, '') + "___";
    retstring += results.split("length:")[1].split("\r\n")[0].replace(/^\s+|\s+$/g, '') + "___";
    retstring += results.split("maintained:")[1].split("\r\n")[0].replace(/^\s+|\s+$/g, '') + "___";
    retstring += results.split("threshold:")[1].split("\r\n")[0].replace(/^\s+|\s+$/g, '') + "___";
    retstring += results.split("duration (minutes):")[1].split("\r\n")[0].replace(/^\s+|\s+$/g, '') + "___";
    retstring += results.split("window (minutes):")[1].split("\r\n")[0].replace(/^\s+|\s+$/g, '');
    return retstring;
}

function ParseDomainControllers(results)
{
    var retstring = "";
    var parse1 = results.split("Non-Site specific:\r\n")[1].split("The command completed")[0];
    var parse2 = parse1.split("\r\n");
    var tmp = [];
    for(var i = 0; i < parse2.length; i++)
    {
        var dcstring = "";
        tmp = parse2[i].split(" ");
        for(var j = 0; j < tmp.length; j++)
        {
            if(tmp[j])
            {
                dcstring += tmp[j].toLowerCase() + "___";
            }
        }
        retstring += dcstring.split("___")[0] + "*" + dcstring.split("___")[1] + "___"
    }
    return retstring;
}

try
{
    var fqdn = Koadic.WS.RegRead("HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Group Policy\\History\\MachineDomain");
    var net = new ActiveXObject("WScript.Network");
    var netbios = net.UserDomain;

    var headers = {};
    headers["Header"] = "Key";
    Koadic.work.report(fqdn + "___" + netbios, headers);

    var domain_admins = ParseUsers(Koadic.shell.exec("net group \"Domain Admins\" /domain", "~DIRECTORY~\\"+Koadic.uuid()+".txt"));
    headers["Header"] = "Admins";
    Koadic.work.report(domain_admins, headers);

    var domain_users = ParseUsers(Koadic.shell.exec("net user /domain", "~DIRECTORY~\\"+Koadic.uuid()+".txt"));
    headers["Header"] = "Users";
    Koadic.work.report(domain_users, headers);

    var password_policy = ParsePasswordPolicy(Koadic.shell.exec("net accounts /domain", "~DIRECTORY~\\"+Koadic.uuid()+".txt"));
    headers["Header"] = "PassPolicy";
    Koadic.work.report(password_policy, headers);

    var domain_controllers = ParseDomainControllers(Koadic.shell.exec("nltest /dnsgetdc:"+fqdn, "~DIRECTORY~\\"+Koadic.uuid()+".txt"));
    headers["Header"] = "DomainControllers";
    Koadic.work.report(domain_controllers, headers);

    Koadic.work.report("Complete");

}
catch(e)
{
    Koadic.work.error(e);
}
Koadic.exit();