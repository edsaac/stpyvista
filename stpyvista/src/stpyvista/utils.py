import urllib.parse as parse
from subprocess import run
from functools import partial
from pyvista import start_xvfb as pv_start_xvfb
from streamlit.runtime.scriptrunner import get_script_run_ctx
from datetime import datetime

_run_command = partial(run, capture_output=True, text=True)


def is_the_app_embedded():
    """Check if the app is embedded based on the query parameters"""

    ctx = get_script_run_ctx()
    query_params = parse.parse_qs(ctx.query_string)
    return True if query_params.get("embed") else False


def _is_pgrep_installed():
    """
    Check if `pgrep` is installed in the environment
    """
    is_pgrep_installed = _run_command(["which", "pgrep"])
    return True if is_pgrep_installed.returncode == 0 else False


def start_xvfb():
    """
    This is a thin wrapper over pv.start_xvfb().
    Check if virtual framebuffer Xvfb is already running on the machine and starts it if not.
    Only available on Linux. Be sure to install `libgl1-mesa-glx` and `xvfb` in your package manager.
    """

    if not _is_pgrep_installed():
        raise OSError(
            "pgrep is not installed. Be sure to install `procps` in your package manager."
        )

    is_xvfb_running = _run_command(["pgrep", "Xvfb"])
    print(datetime.now().strftime(r"%y-%m-%d %H:%M:%S"))
    
    if is_xvfb_running.returncode == 1:
        print("--> Initialize")
        pv_start_xvfb()

    elif is_xvfb_running.returncode == 0:
        print(f"--> PID: {is_xvfb_running.stdout.strip()}")

    else:
        raise OSError(
            "Something went wrong checking for the machine processes"
            f"{is_xvfb_running.stdout}"
            f"{is_xvfb_running.stderr}"
        )

