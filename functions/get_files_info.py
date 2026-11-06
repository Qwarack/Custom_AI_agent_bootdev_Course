import logging
import os


def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

        # Will be True or False
        valid_target_dir = (
            os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        )

        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        items_indir = os.listdir(target_dir)
        result = []
        for item in items_indir:
            # Compile name, byte size and dir bool
            name = item
            item_path = os.path.join(target_dir, item)
            size = os.path.getsize(item_path)
            is_dir = os.path.isdir(item_path)

            full_str = f"- {name}: file_size={size} bytes, is_dir={is_dir}"
            result.append(full_str)

        result_string = "\n".join(result)
        return result_string

    except Exception as e:
        logging.exception("Standard library error")
        return f"Error: {e}"
