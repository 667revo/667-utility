import subprocess
import shlex
import sys

if sys.platform == "win32":
    import winreg

else:
    winreg = None

def run_cmd(cmd: list):
    try:
        return subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=30
        )
    except subprocess.TimeoutExpired:
        print(f"Timeout: {cmd}")
        return None

def get_installed_programs() -> list[dict]:
    if winreg is None:
        print("This feature is only available on Windows.")
        return[]
    programs = []
    keys = [
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"),
        (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
    ]

    for hive, path in keys:
        try:
            key = winreg.OpenKey(hive, path)
            for i in range(winreg.QueryInfoKey(key)[0]):
                try:
                    subkey_name = winreg.EnumKey(key, i)
                    subkey = winreg.OpenKey(key, subkey_name)
                    name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                    try:
                        uninstall_str = winreg.QueryValueEx(subkey, "UninstallString")[0]
                    except:
                        uninstall_str = ""
                    if name and name.strip():
                        programs.append({
                            "name": name.strip(),
                            "uninstall_str": uninstall_str
                        })
                except:
                    continue
        except:
            continue

    seen = set()
    unique = []
    for p in programs:
        if p["name"] not in seen:
            seen.add(p["name"])
            unique.append(p)

    return sorted(unique, key=lambda x: x["name"].lower())

def uninstall_program(uninstall_str: str) -> bool:
    if winreg is None:
        print("This feature is only available on Windows.")
        return
    if not uninstall_str:
        return False
    try:
        if "msiexec" in uninstall_str.lower():
            import re

            match = re.search(r"\{[A-F0-9\-]+\}", uninstall_str, re.IGNORECASE)
            if match:
                result = run_cmd(["msiexec", "/x", match.group(), "/qn", "/norestart"])
            else:
                result = run_cmd(
                    ["msiexec", "/x", uninstall_str.split()[-1], "/qn", "/norestart"]
                )
        else:
            result = run_cmd(shlex.split(uninstall_str))

        return result.returncode == 0 if result else False
    except Exception as e:
        print(f"Uninstall error: {e}")
        return False

BLOATWARE = [
    "Microsoft.BingNews",
    "Microsoft.BingWeather",
    "Microsoft.GetHelp",
    "Microsoft.Getstarted",
    "Microsoft.MicrosoftOfficeHub",
    "Microsoft.MicrosoftSolitaireCollection",
    "Microsoft.People",
    "Microsoft.PowerAutomateDesktop",
    "Microsoft.Todos",
    "Microsoft.WindowsAlarms",
    "Microsoft.WindowsCamera",
    "Microsoft.WindowsFeedbackHub",
    "Microsoft.WindowsMaps",
    "Microsoft.WindowsSoundRecorder",
    "Microsoft.Xbox.TCUI",
    "Microsoft.XboxApp",
    "Microsoft.XboxGameOverlay",
    "Microsoft.XboxGamingOverlay",
    "Microsoft.XboxIdentityProvider",
    "Microsoft.XboxSpeechToTextOverlay",
    "Microsoft.YourPhone",
    "Microsoft.ZuneMusic",
    "Microsoft.ZuneVideo",
    "MicrosoftTeams",
]

def remove_bloatware() -> bool:

    for app in BLOATWARE:
        subprocess.run([
            "powershell.exe", "-Command",
            f"Get-AppxPackage *{app}* | Remove-AppxPackage"
        ], capture_output=True, text=True, encoding="utf-8", errors="replace")

    
    subprocess.run([
        "powershell.exe", "-Command",
        r"Get-ChildItem 'C:\Program Files (x86)\Microsoft\Edge\Application\*\Installer' | "
        r"ForEach-Object { Start-Process -FilePath (Join-Path $_.FullName 'setup.exe') "
        r"-ArgumentList '--uninstall --system-level --verbose-logging --force-uninstall' -Wait }"
    ], capture_output=True, text=True, encoding="utf-8", errors="replace")

    return True