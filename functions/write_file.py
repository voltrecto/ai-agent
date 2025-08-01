import os
from google.genai import types

def write_file(working_directory, file_path, content):
    try:
        target_path = os.path.abspath(os.path.join(working_directory, file_path))
        working_directory = os.path.abspath(working_directory)
        if not target_path.startswith(working_directory):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
        target_directory = os.path.dirname(target_path)
        try:
            os.makedirs(target_directory, exist_ok=True)
        except Exception as e:
            return f"Error: {e}" 
        try:
            with open(target_path, "w") as f:
                f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        except Exception as e:
            return f"Error: {e}"
        
    except Exception as e:
        return f"Error: {e}"
    
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write to a file in the file path, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path of file to be written.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to be written.",
            ),
        },
    ),
)