def run_react():
    """Run React server using shell script"""
    import os
    import subprocess
    from rich import print as rprint

    os.chdir("..")
    current_path = os.getcwd()
    script_path = os.path.join(current_path, "config", "react")
    os.chdir(script_path)

    try:
        subprocess.run(["bash", "./startapp.sh"], check=True, shell=True)

    except Exception as e:
        rprint(f"An error occurred while starting react local server {e}")
