import os, subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    try:
        target_path = os.path.abspath(os.path.join(working_directory, file_path))
        working_directory = os.path.abspath(working_directory)
        if not target_path.startswith(working_directory):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(target_path):
            return f'Error: File "{file_path}" not found.'
        
        if not target_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'
        
        try:
            completed_process = subprocess.run(
                ["python", target_path, *args],
                capture_output=True,
                text=True,
                cwd=working_directory,
                timeout=30
            )

            output = ""
            if completed_process.stdout:
                output += f"STDOUT: {completed_process.stdout}\n"
            if completed_process.stderr:
                output += f" STDERR: {completed_process.stderr}\n"
            if completed_process.returncode != 0:
                output += f" Process exited with code {completed_process.returncode}"
            if not completed_process.stdout and not completed_process.stderr:
                output = "No output produced."
            return output
        
        except Exception as e:
            return f"Error: executing Python file: {e}"
        
    except Exception as e:
        return f"Error: {e}"
    

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run python file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path of python file.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                    description="A single argument."
                ),
                description="A list of arguments to pass to the python file.",
            ),
        },
    ),
)