"""Run the full reproducibility path with one command."""
import subprocess
import sys


def run(*args: str) -> None:
    subprocess.run([sys.executable, *args], check=True)


run("-m", "unittest", "discover", "-s", "tests", "-v")
run("-m", "reference.demo")
run("-m", "reference.verify_all")

