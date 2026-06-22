"""
توابع فشرده‌سازی و خارج‌سازی فایل‌ها
"""

import os
import zipfile
from pathlib import Path
from typing import Union, List, Optional
import shutil

def zip_folder(source: Union[str, Path], output: Union[str, Path],
               compression: int = zipfile.ZIP_DEFLATED) -> str:
    """
    فشرده‌سازی یک پوشه به صورت ZIP
    
    Args:
        source: مسیر پوشه مبدا
        output: مسیر فایل ZIP خروجی
        compression: نوع فشرده‌سازی (پیش‌فرض: ZIP_DEFLATED)
    
    Returns:
        مسیر فایل ZIP ساخته شده
    """
    source = Path(source)
    output = Path(output)
    
    if not source.exists() or not source.is_dir():
        raise FileNotFoundError(f"پوشه مبدا وجود ندارد: {source}")
    
    # اطمینان از وجود پوشه خروجی
    output.parent.mkdir(parents=True, exist_ok=True)
    
    with zipfile.ZipFile(output, 'w', compression) as zipf:
        for item in source.rglob('*'):
            if item.is_file():
                arcname = item.relative_to(source)
                zipf.write(item, arcname)
    
    return str(output)

def unzip_file(zip_path: Union[str, Path], extract_to: Union[str, Path],
               overwrite: bool = False) -> str:
    """
    خارج‌سازی فایل ZIP
    
    Args:
        zip_path: مسیر فایل ZIP
        extract_to: مسیر پوشه مقصد
        overwrite: بازنویسی فایل‌های موجود
    
    Returns:
        مسیر پوشه مقصد
    """
    zip_path = Path(zip_path)
    extract_to = Path(extract_to)
    
    if not zip_path.exists() or not zip_path.is_file():
        raise FileNotFoundError(f"فایل ZIP وجود ندارد: {zip_path}")
    
    if not zipfile.is_zipfile(zip_path):
        raise ValueError(f"فایل معتبر ZIP نیست: {zip_path}")
    
    extract_to.mkdir(parents=True, exist_ok=True)
    
    with zipfile.ZipFile(zip_path, 'r') as zipf:
        for member in zipf.namelist():
            target = extract_to / member
            if target.exists() and not overwrite:
                raise FileExistsError(f"فایل وجود دارد: {target}")
        
        zipf.extractall(extract_to)
    
    return str(extract_to)

def zip_files(files: List[Union[str, Path]], output: Union[str, Path],
              compression: int = zipfile.ZIP_DEFLATED) -> str:
    """
    فشرده‌سازی چند فایل مشخص در یک ZIP
    
    Args:
        files: لیست مسیر فایل‌ها
        output: مسیر فایل ZIP خروجی
    
    Returns:
        مسیر فایل ZIP ساخته شده
    """
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    
    with zipfile.ZipFile(output, 'w', compression) as zipf:
        for file_path in files:
            file_path = Path(file_path)
            if not file_path.exists() or not file_path.is_file():
                raise FileNotFoundError(f"فایل وجود ندارد: {file_path}")
            zipf.write(file_path, file_path.name)
    
    return str(output)

def get_zip_info(zip_path: Union[str, Path]) -> List[dict]:
    """
    دریافت اطلاعات محتویات فایل ZIP
    
    Returns:
        لیست دیکشنری‌های شامل: نام، حجم، تاریخ
    """
    zip_path = Path(zip_path)
    if not zip_path.exists() or not zip_path.is_file():
        raise FileNotFoundError(f"فایل ZIP وجود ندارد: {zip_path}")
    
    info_list = []
    with zipfile.ZipFile(zip_path, 'r') as zipf:
        for info in zipf.infolist():
            info_list.append({
                "name": info.filename,
                "size": info.file_size,
                "compressed_size": info.compress_size,
                "date": f"{info.date_time[0]}-{info.date_time[1]:02d}-{info.date_time[2]:02d}",
                "is_dir": info.filename.endswith('/')
            })
    
    return info_list

def extract_all(zip_path: Union[str, Path], extract_to: Union[str, Path]) -> List[str]:
    """
    خارج‌سازی همه فایل‌ها از ZIP با حفظ ساختار
    
    Returns:
        لیست مسیر فایل‌های خارج‌شده
    """
    zip_path = Path(zip_path)
    extract_to = Path(extract_to)
    
    if not zip_path.exists() or not zip_path.is_file():
        raise FileNotFoundError(f"فایل ZIP وجود ندارد: {zip_path}")
    
    extract_to.mkdir(parents=True, exist_ok=True)
    
    extracted_files = []
    with zipfile.ZipFile(zip_path, 'r') as zipf:
        zipf.extractall(extract_to)
        for member in zipf.namelist():
            extracted_path = extract_to / member
            if extracted_path.is_file():
                extracted_files.append(str(extracted_path))
    
    return extracted_files