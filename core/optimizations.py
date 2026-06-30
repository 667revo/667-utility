import os
import subprocess

def run_cmd(cmd: list):
    try:
        return subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5
        )
    except subprocess.TimeoutExpired:
            print(f"Timeout: {cmd}")
            return None




class Optimizations:
    @staticmethod
    def disable_sysmain():
        result = run_cmd(
            ["sc", "stop", "SysMain"]
        )
        run_cmd(["sc", "config", "SysMain", "start=disabled"])
        return result.returncode == 0

    @staticmethod
    def enable_sysmain():
        run_cmd(["sc", "start", "SysMain"])
        run_cmd(["sc", "config", "SysMain", "start=auto"])


    @staticmethod
    def set_high_performance():
        result = run_cmd(
            ["powercfg", "/setactive", "8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c"]

        )
        run_cmd(["sc", "config", "SysMain", "start=disabled"])
        return result.returncode == 0

    @staticmethod
    def disable_telemetry():

        services = ["DiagTrack", "dmwappushservice"]

        for svc in services:
            run_cmd(["sc", "stop", svc])
            run_cmd(["sc", "config", svc, "start=disabled"])

    @staticmethod
    def enable_telemetry():
        services = ["DiagTrack", "dmwappushservice"]

        for svc in services:
            run_cmd(["sc", "start", svc])
            run_cmd(["sc", "config", svc, "start=auto"])

    @staticmethod
    def clear_temp():
        run_cmd(["cmd", "/c", "del /q /f /s %TEMP%\\*"])
        run_cmd(["cmd", "del /q /f /s" , "C:\Windows\\Temp\\*"])
        run_cmd(["cmd", "/c", "del /q /f /s", "C:\\Windows\\SoftwareDistribution\\Download\\*"])
        run_cmd(["cmd", "/c", "del /q /f /s", "C:\\Windows\\Prefetch\\*"])
        run_cmd(["cmd", "/c", "cleanmgr", "/sagerun:1"])

        return True

    @staticmethod
    def disable_search_index():
        result = run_cmd(
            ["sc", "stop", "WSearch"]
        )
        run_cmd(["sc", "config", "WSearch", "start=disabled"])
        return result.returncode == 0
    
    @staticmethod
    def enable_search_index():
        run_cmd(["sc", "start", "WSearch"]),
        run_cmd(["sc", "config", "WSearch", "start=auto"])


    @staticmethod
    def disable_xbox_services():
        print("Xbox disable started")
        xbox_services= ["XblAuthManager", "XblGameSave", "XboxNetAbiSvc", "XboxGipSvc"]

        for svc in xbox_services:
            run_cmd(["sc", "stop", svc])
            run_cmd(["sc", "config", svc, "start=disabled"])

        run_cmd([
            "powershell.exe", "-Command",
            "Get-AppxPackage", "Microsoft.GamingServices", "|", "Remove-AppxPackage", "-AllUsers"])
        run_cmd([
            "powershell.exe", "-Command",
            "Get-AppxPackage", "Microsoft.XboxGamingOverlay", "|", "Remove-AppxPackage"])
        
    @staticmethod
    def enable_xbox_services():
        print("Xbox enable started")
        xbox_services = ["XblAuthManager", "XblGameSave", "XboxNetAbiSvc", "XboxGipSvc"]

        for svc in xbox_services:
            run_cmd(["sc", "start", svc])
            run_cmd(["sc", "config", svc, "start=auto"])

        run_cmd([
            "powershell.exe", "-Command",
            "start ms-windows-store://pdp/?productid=9MWPM2CQNLHN"
        ])

    @staticmethod
    def reduce_services():

        un_services = ["Fax", "TabletInputService", "WerSvc", "seclogon", "NetTcpPortSharing", "CDPSvc", "CDPUserSvc",
                       "SharedAccess", "TermService", "SessionEnv", "wisvc", "WbioSrvc", "DusmSvc", "CscService", "UsoSvc", "Spooler", "SCardSvr", "MapsBroker", "RasSstp", "StorSvc", "MsNetMgt"]

        for svc in un_services:
            run_cmd(["sc", "stop", svc])
            run_cmd(["sc", "config", svc , "start=disabled"])
    
    @staticmethod 
    def restore_services():
        un_services = [
            "Fax",
            "TabletInputService",
            "WerSvc",
            "seclogon",
            "NetTcpPortSharing",
            "CDPSvc",
            "CDPUserSvc",
            "SharedAccess",
            "TermService",
            "SessionEnv",
            "wisvc",
            "WbioSrvc",
            "DusmSvc",
            "CscService",
            "UsoSvc",
            "Spooler",
            "SCardSvr",
            "MapsBroker",
            "RasSstp",
            "StorSvc",
            "MsNetMgt",
        ]
        for svc in un_services:
            run_cmd(["sc", "start", svc])
            run_cmd(["sc", "config", svc , "start=auto"])

    REGS_PATH = os.path.join(os.path.dirname(__file__), "..", "assets", "regs")

    @staticmethod
    def apply_all_reg() -> bool:

        files = [f for f in os.listdir(Optimizations.REGS_PATH) if f.endswith(".reg")]

        if not files:
                print("No reg file found")
                return False

        success = True

        for filename in files:
            path = os.path.join(Optimizations.REGS_PATH, filename)
            result = run_cmd(["regedit", "/s", path])
            if result and result.returncode != 0:
                success = False
                print(f"failed to apply {filename}")


    BAT_PATH = os.path.join(os.path.dirname(__file__), "..", "assets", "bat")

    @staticmethod
    def lower_input_delay():
        path = os.path.join(Optimizations.BAT_PATH, "lower_input_delay.bat")
        try:
            result = subprocess.run(
                ["cmd", "/c", path],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=60,
            )
            log_path = os.path.join(os.environ.get("TEMP", ""), "lower_input_delay.log")
            success = os.path.exists(log_path)
            if success:
                os.remove(log_path)
            return success
        except subprocess.TimeoutExpired:
            print("Timeout: lower_input_delay.bat")
            return False

    @staticmethod
    def disable_background_apps():
        commands = [
            "Get-AppxPackage | Where-Object {$_.IsFramework -eq $false} | ForEach-Object {Set-ItemProperty -Path \"HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\BackgroundAccessApplications\\$($_.PackageFamilyName)\" -Name 'Disabled' -Value 1 -Force -ErrorAction SilentlyContinue}",
            'reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\BackgroundAccessApplications" /v GlobalUserDisabled /t REG_DWORD /d 1 /f',
            'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\AppPrivacy" /v LetAppsRunInBackground /t REG_DWORD /d 2 /f',
        ]

        for cmd in commands:
            subprocess.run(
                ["powershell.exe", "-Command", cmd],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
            )

        return True

    @staticmethod
    def enable_background_apps():
        commands = [
            'reg delete "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\BackgroundAccessApplications" /v GlobalUserDisabled /f',
            'reg delete "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\AppPrivacy" /v LetAppsRunInBackground /f',
        ]

        for cmd in commands:
            subprocess.run(
                ["powershell.exe", "-Command", cmd],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
            )

        return True