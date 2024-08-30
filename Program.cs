using Slint;
using AppWindow;
using Torizon.Shell;

Environment.SetEnvironmentVariable("SLINT_STYLE", "fluent-light");

var win = new Window();

win.Close += () => {
    Environment.Exit(0);
};

Slint.Timer.Start(TimerMode.SingleShot, 100, () => {
    win.Height = 390;
    win.Width = 450;

    var _ret = Exec.Bash("source /etc/os-release && echo $VERSION_ID");
    if (_ret.exitCode != 0 || _ret.output == null) Environment.Exit(0);

    win.Version = _ret.output.Trim();

    _ret = Exec.Bash("uname -s");
    if (_ret.exitCode != 0 || _ret.output == null) Environment.Exit(0);

    win.OS = _ret.output.Trim();

    _ret = Exec.Bash("uname -r");
    if (_ret.exitCode != 0 || _ret.output == null) Environment.Exit(0);

    win.OSVersion = _ret.output.Trim();

    _ret = Exec.Bash("wsl.exe --version | iconv -f UTF16 -t UTF8 | tr -d '\r'");
    if (_ret.exitCode != 0 || _ret.output == null) Environment.Exit(0);

    win.WSLVersions = _ret.output.Trim();
});

win.Run();
