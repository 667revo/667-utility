import subprocess
import sys
import shutil
from typing import Tuple

def install_by_winget_id(winget_id: str) -> Tuple[int, str]:
    if shutil.which("winget"):
        cmd = [
            "winget", "install", "--id", winget_id, "-e",
            "--accept-package-agreements", "--accept-source-agreements"
        ]
    elif sys.platform.startswith("linux"):
        if shutil.which("apt"):
            pkg_name = winget_id
            cmd = ["sudo", "apt", "install", "-y", pkg_name]
        elif shutil.which("snap"):
            pkg_name = winget_id
            cmd = ["sudo", "snap", "install", pkg_name]
        else:
            return -3, "No supported package manager found on this system."
    else:
        return -1, "winget not found on PATH and OS not supported."

    try:
        res = subprocess.run(
            cmd,
            check=False,
            capture_output=True,
            text=True
        )
        out = ""
        if res.stdout:
            out += res.stdout
        if res.stderr:
            out += ("\n[stderr]\n" + res.stderr)
        return res.returncode, out or f"command exited with code {res.returncode}"
    except FileNotFoundError:
        return -2, "Error: installer command not found (FileNotFoundError)"
    except Exception as e:
        return -4, f"Unexpected exception: {e}"