import os
from google.genai import types

def get_files_info(working_directory, directory=None):
    try:
        target_path = os.path.abspath(os.path.join(working_directory, directory or ""))
        working_directory = os.path.abspath(working_directory)

        if not target_path.startswith(working_directory):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(target_path):
            return f'Error: "{directory}" is not a directory'

        contents = os.listdir(target_path)
        content_list = []
        for name in contents:
            full_path = os.path.join(target_path, name)
            size = os.path.getsize(full_path)
            is_dir = os.path.isdir(full_path)
            content_list.append(f"- {name}: file_size={size} bytes, is_dir={is_dir}")
        return '\n'.join(content_list)
    except Exception as e:
        return f"Error: {e}"

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)