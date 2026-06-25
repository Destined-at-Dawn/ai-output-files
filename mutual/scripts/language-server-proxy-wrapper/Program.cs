using System.Diagnostics;

const string proxy = "http://127.0.0.1:10808";

string exeDir = AppContext.BaseDirectory.TrimEnd(Path.DirectorySeparatorChar, Path.AltDirectorySeparatorChar);
string realExe = Path.Combine(exeDir, "language_server.real.exe");
string logDir = Path.Combine(
    Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData),
    "Antigravity",
    "logs");
Directory.CreateDirectory(logDir);
File.AppendAllText(
    Path.Combine(logDir, "language_server_proxy_wrapper.log"),
    $"{DateTimeOffset.Now:O} proxy={proxy} realExe={realExe} args={string.Join(' ', args.Select(a => a.Contains(' ') ? '\"' + a + '\"' : a))}{Environment.NewLine}");

if (!File.Exists(realExe))
{
    Console.Error.WriteLine($"language_server.real.exe not found: {realExe}");
    return 127;
}

var psi = new ProcessStartInfo
{
    FileName = realExe,
    UseShellExecute = false,
};

foreach (string arg in args)
{
    psi.ArgumentList.Add(arg);
}

psi.Environment["HTTP_PROXY"] = proxy;
psi.Environment["HTTPS_PROXY"] = proxy;
psi.Environment["ALL_PROXY"] = proxy;
psi.Environment["NO_PROXY"] = "localhost,127.0.0.1,::1,*.local";
psi.Environment["http_proxy"] = proxy;
psi.Environment["https_proxy"] = proxy;
psi.Environment["all_proxy"] = proxy;
psi.Environment["no_proxy"] = "localhost,127.0.0.1,::1,*.local";

using Process child = Process.Start(psi)
    ?? throw new InvalidOperationException($"Failed to start {realExe}");
child.WaitForExit();
return child.ExitCode;
