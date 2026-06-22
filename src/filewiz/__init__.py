"""
FileWizard - ابزارهای پیشرفته برای مدیریت فایل‌ها
"""

from .core import (
    copy_file, move_file, delete_file,
    copy_folder, move_folder, delete_folder,
    get_file_size, get_folder_size, get_file_info
)
from .compress import (
    zip_folder, unzip_file, zip_files,
    get_zip_info, extract_all
)
from .utils import (
    find_duplicate_files, clean_folder,
    rename_files_pattern, get_file_extension,
    ensure_directory, is_hidden_file
)

__version__ = "0.1.0"
__all__ = [
    "copy_file", "move_file", "delete_file",
    "copy_folder", "move_folder", "delete_folder",
    "get_file_size", "get_folder_size", "get_file_info",
    "zip_folder", "unzip_file", "zip_files",
    "get_zip_info", "extract_all",
    "find_duplicate_files", "clean_folder",
    "rename_files_pattern", "get_file_extension",
    "ensure_directory", "is_hidden_file"
]