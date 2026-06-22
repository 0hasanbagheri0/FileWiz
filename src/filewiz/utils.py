"""
توابع کمکی و ابزاری
"""

import os
import hashlib
from pathlib import Path
from typing import Union, List, Optional, Tuple

def ensure_directory(path: Union[str, Path]) -> Path:
    """ایجاد پوشه در صورت وجود نداشتن"""
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path

def find_duplicate_files(directory: Union[str, Path],
                         hash_algorithm: str = "md5") -> List[List[str]]:
    """پیدا کردن فایل‌های تکراری در یک پوشه"""
    directory = Path(directory)
    if not directory.exists() or not directory.is_dir():
        raise FileNotFoundError(f"پوشه وجود ندارد: {directory}")
    
    hashes = {}
    for file_path in directory.rglob('*'):
        if not file_path.is_file():
            continue
        hasher = hashlib.new(hash_algorithm)
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                hasher.update(chunk)
        file_hash = hasher.hexdigest()
        if file_hash not in hashes:
            hashes[file_hash] = []
        hashes[file_hash].append(str(file_path))
    
    return [group for group in hashes.values() if len(group) > 1]

def clean_folder(directory: Union[str, Path],
                 extensions: Optional[List[str]] = None,
                 min_size: Optional[int] = None,
                 max_size: Optional[int] = None) -> List[str]:
    """پاکسازی پوشه بر اساس پسوند یا حجم"""
    directory = Path(directory)
    if not directory.exists() or not directory.is_dir():
        raise FileNotFoundError(f"پوشه وجود ندارد: {directory}")
    
    deleted = []
    for file_path in directory.rglob('*'):
        if not file_path.is_file():
            continue
        should_delete = False
        size = file_path.stat().st_size
        if extensions and file_path.suffix.lower() in extensions:
            should_delete = True
        if min_size is not None and size < min_size:
            should_delete = True
        if max_size is not None and size > max_size:
            should_delete = True
        if should_delete:
            os.remove(file_path)
            deleted.append(str(file_path))
    
    return deleted

def rename_files_pattern(directory: Union[str, Path],
                         pattern: str = "file_{:03d}",
                         extensions: Optional[List[str]] = None) -> List[Tuple[str, str]]:
    """تغییر نام گروهی فایل‌ها با الگو"""
    directory = Path(directory)
    if not directory.exists() or not directory.is_dir():
        raise FileNotFoundError(f"پوشه وجود ندارد: {directory}")
    
    files = []
    for file_path in directory.iterdir():
        if file_path.is_file():
            if extensions is None or file_path.suffix.lower() in extensions:
                files.append(file_path)
    
    files.sort(key=lambda x: x.stat().st_mtime)
    renamed = []
    for idx, file_path in enumerate(files, start=1):
        new_name = pattern.format(idx) + file_path.suffix
        new_path = directory / new_name
        counter = 1
        while new_path.exists():
            new_name = pattern.format(idx) + f"_{counter}" + file_path.suffix
            new_path = directory / new_name
            counter += 1
        old_path = str(file_path)
        file_path.rename(new_path)
        renamed.append((old_path, str(new_path)))
    
    return renamed

def get_file_extension(file_path: Union[str, Path]) -> str:
    """دریافت پسوند فایل (با نقطه)"""
    return Path(file_path).suffix

def is_hidden_file(path: Union[str, Path]) -> bool:
    """تشخیص فایل مخفی"""
    path = Path(path)
    if os.name == 'nt':  # Windows
        try:
            import ctypes
            attrs = ctypes.windll.kernel32.GetFileAttributesW(str(path))
            return attrs != -1 and bool(attrs & 2)
        except:
            return path.name.startswith('.')
    else:  # Linux/Mac
        return path.name.startswith('.')