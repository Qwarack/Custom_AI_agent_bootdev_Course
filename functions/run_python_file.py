import logging
import os
import subprocess

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Executes a Python file relative to the working directory with optional arguments, returning its standard output, standard error, and any nonzero exit code.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path of the Python file to execute, relative to the working directory.",
                },
                "args": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Optional command-line arguments to pass to the Python file.",
                },
            },
            "required": ["file_path"],
        },
    },
}


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))

        # Will be True or False
        valid_target_dir = (
            os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        )

        if not valid_target_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_dir):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not target_dir.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_dir]
        if args is not None:
            command.extend(args)

        full_process = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
            cwd=working_dir_abs,
        )

        output_string = ""

        if full_process.returncode != 0:
            output_string += f"Process exited with code {full_process.returncode}"

        if full_process.stdout is None or full_process.stderr is None:
            output_string += "No output produced"
        else:
            output_string += f"STDOUT: {full_process.stdout}"
            output_string += f"STDERR: {full_process.stderr}"

        return output_string

    except Exception as e:
        logging.exception("Standard library error")
        return f"Error: executing Python file: {e}"
