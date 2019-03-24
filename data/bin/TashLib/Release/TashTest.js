var manifestPath = "TashLib.manifest";

var actCtx = new ActiveXObject( "Microsoft.Windows.ActCtx" );
actCtx.Manifest = manifestPath;
var tash =  actCtx.CreateObject("TashLib.TashLoader");

var errno = tash.Load("\x90\x90\xc3", "~~", 1);
WScript.Echo(errno);

