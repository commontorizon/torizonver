
import os
import subprocess
import slint # type: ignore
from slint import Timer, TimerMode
from datetime import timedelta

# load the components using load_file to set the style
app_components = slint.load_file("./ui/AppWindow.slint", style="fluent-light")
class AppWindow(app_components.AppWindow): # type: ignore

    def __on_load(self):
        self.Height = 390
        self.Width = 450

        def exec_bash(command):
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            return result

        if "WSL_DISTRO_NAME" in os.environ:
            _ret = exec_bash("source /etc/os-release && echo $VERSION_ID")
            if _ret.returncode != 0 or not _ret.stdout:
                self.hide()

            self.Version = _ret.stdout.strip()

            _ret = exec_bash("uname -s")
            if _ret.returncode != 0 or not _ret.stdout:
                self.hide()

            self.OS = _ret.stdout.strip()

            _ret = exec_bash("uname -r")
            if _ret.returncode != 0 or not _ret.stdout:
                self.hide()

            self.OSVersion = _ret.stdout.strip()

            _ret = exec_bash("uname -m")
            if _ret.returncode != 0 or not _ret.stdout:
                self.hide()

            self.OSArch = _ret.stdout.strip()

            _ret = exec_bash("wsl.exe --version | iconv -f UTF16 -t UTF8 | tr -d '\r'")
            if _ret.returncode != 0 or not _ret.stdout:
                self.hide()

            self.WSLVersions = _ret.stdout.strip()
        else:
            # it means that propably the app is running in test mode
            self.timer.start(
                TimerMode.SingleShot,
                timedelta(milliseconds=10000),
                self.Close
            )


    def __init__(self):
        super().__init__()

        self.Width = 455
        self.Height = 390
        self.Version = "0.0.0"
        self.OS = "Windows"
        self.OSVersion = "11"
        self.OSArch = "x86_64"
        self.WSLVersions = "WSL version: 2.3.17.0\nKernel version: 5.15.153.1-2\nWSLg version: 1.0.64\nMSRDC version: 1.2.5326\nDirect3D version: 1.611.1-81528511\nDXCore version: 10.0.26100.1-240331-1435.ge-release\nWindows version: 10.0.26120.1542"

        self.timer = Timer()
        self.timer.start(
            TimerMode.SingleShot,
            timedelta(milliseconds=100),
            self.__on_load
        )



    @slint.callback
    def Close(self):
        self.hide()


app = AppWindow()
app.run()
