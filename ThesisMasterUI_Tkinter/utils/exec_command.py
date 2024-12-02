from typing import Any
import subprocess


def execute_command(command: str, directory: str) -> Any:
    try:
        # Run the command and capture both stdout and stderr
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            check=True,
            cwd=directory,
        )
        # Store the output in a variable
        output = result.stdout
        error = result.stderr
        return output, error
    except subprocess.CalledProcessError as e:
        # Handle the error and store the stderr
        return None, e
