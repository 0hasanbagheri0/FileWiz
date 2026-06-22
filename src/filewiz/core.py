"""
توابع اصلی کار با فایل‌ها
"""

import os
import shutil
from pathlib import Path
from typing import Union, Optional, Dict, Any

def ensure_directory(path: Union[str, Path]) -> Path:
    """ایجاد پوشه در صورت وجود نداشتن"""
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path

def copy_file(source: Union[str, Path], destination: Union[str, Path], 
              overwrite: bool = False) -> bool:
    """
    کپی کردن فایل
    
    Args:
        source: مسیر فایل مبدا
        destination: مسیر فایل مقصد
        overwrite: بازنویسی فایل مقصد در صورت وجود
    
    Returns:
        True در صورت موفقیت، False در غیر این صورت
    """
    source = Path(source)
    dest = Path(destination)
    
    if not source.exists() or not source.is_file():
        raise FileNotFoundError(f"فایل مبدا وجود ندارد: {source}")
    
    if dest.exists() and not overwrite:
        raise FileExistsError(f"فایل مقصد وجود دارد: {dest}")
    
    ensure_directory(dest.parent)
    shutil.copy2(source, dest)
    return True

def move_file(source: Union[str, Path], destination: Union[str, Path],
              overwrite: bool = False) -> bool:
    """جابجایی فایل"""
    source = Path(source)
    dest = Path(destination)
    
    if not source.exists() or not source.is_file():
        raise FileNotFoundError(f"فایل مبدا وجود ندارد: {source}")
    
    if dest.exists() and not overwrite:
        raise FileExistsError(f"فایل مقصد وجود دارد: {dest}")
    
    ensure_directory(dest.parent)
    shutil.move(str(source), str(dest))
    return True

def delete_file(path: Union[str, Path], force: bool = False) -> bool:
    """
    حذف فایل
    
    Args:
        path: مسیر فایل
        force: حذف اجباری حتی اگر فایل محافظت‌شده باشد
    
    Returns:
        True در صورت موفقیت
    """
    path = Path(path)
    
    if not path.exists():
        if force:
            return False
        raise FileNotFoundError(f"فایل وجود ندارد: {path}")
    
    if path.is_dir():
        raise IsADirectoryError(f"مسیر یک پوشه است: {path}")
    
    os.remove(path)
    return True

def copy_folder(source: Union[str, Path], destination: Union[str, Path],
                overwrite: bool = False) -> bool:
    """کپی پوشه به همراه تمام محتویات"""
    source = Path(source)
    dest = Path(destination)
    
    if not source.exists() or not source.is_dir():
        raise FileNotFoundError(f"پوشه مبدا وجود ندارد: {source}")
    
    if dest.exists():
        if not overwrite:
            raise FileExistsError(f"پوشه مقصد وجود دارد: {dest}")
        shutil.rmtree(dest)
    
    shutil.copytree(source, dest)
    return True

def move_folder(source: Union[str, Path], destination: Union[str, Path],
                overwrite: bool = False) -> bool:
    """جابجایی پوشه به همراه تمام محتویات"""
    return copy_folder(source, destination, overwrite)

def delete_folder(path: Union[str, Path], force: bool = False) -> bool:
    """حذف پوشه به همراه تمام محتویات"""
    path = Path(path)
    
    if not path.exists():
        if force:
            return False
        raise FileNotFoundError(f"پوشه وجود ندارد: {path}")
    
    if not path.is_dir():
        raise NotADirectoryError(f"مسیر یک فایل است: {path}")
    
    shutil.rmtree(path)
    return True

def get_file_size(path: Union[str, Path]) -> int:
    """دریافت حجم فایل به بایت"""
    path = Path(path)
    if not path.exists() or not path.is_file():
        raise FileNotFoundError(f"فایل وجود ندارد: {path}")
    return path.stat().st_size

def get_folder_size(path: Union[str, Path]) -> int:
    """دریافت حجم کل پوشه به بایت"""
    path = Path(path)
    if not path.exists() or not path.is_dir():
        raise FileNotFoundError(f"پوشه وجود ندارد: {path}")
    
    total = 0
    for item in path.rglob('*'):
        if item.is_file():
            total += item.stat().st_size
    return total

def get_file_info(path: Union[str, Path]) -> Dict[str, Any]:
    """
    دریافت اطلاعات کامل یک فایل
    
    Returns:
        دیکشنری شامل: name, size, extension, created, modified, is_hidden
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"فایل وجود ندارد: {path}")
    
    stat = path.stat()
    return {
        "name": path.name,
        "size": stat.st_size,
        "extension": path.suffix,
        "created": stat.st_ctime,
        "modified": stat.st_mtime,
        "is_hidden": is_hidden_file(path),
        "is_file": path.is_file(),
        "is_dir": path.is_dir(),
        "parent": str(path.parent)
    }

def is_hidden_file(path: Union[str, Path]) -> bool:
    """تشخیص فایل یا پوشه مخفی"""
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