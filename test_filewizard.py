"""
تست جامع کتابخانه FileWizard
"""

import os
import tempfile
import shutil
from pathlib import Path

# ایمپورت توابع کتابخانه
from filewizard import (
    copy_file, move_file, delete_file,
    copy_folder, move_folder, delete_folder,
    get_file_size, get_folder_size, get_file_info,
    zip_folder, unzip_file, zip_files,
    find_duplicate_files, clean_folder,
    rename_files_pattern, ensure_directory,
    is_hidden_file
)

def create_test_files():
    """ایجاد فایل‌های تست"""
    test_dir = Path("test_files")
    test_dir.mkdir(exist_ok=True)
    
    # ایجاد فایل‌های متنی
    for i in range(1, 4):
        file_path = test_dir / f"file_{i}.txt"
        file_path.write_text(f"محتوای فایل شماره {i}\n", encoding='utf-8')
    
    # ایجاد یک فایل تکراری
    dup_file = test_dir / "file_1_copy.txt"
    dup_file.write_text("محتوای فایل شماره 1\n", encoding='utf-8')
    
    # ایجاد یک پوشه با فایل‌های داخلی
    sub_dir = test_dir / "sub_folder"
    sub_dir.mkdir(exist_ok=True)
    for i in range(1, 3):
        file_path = sub_dir / f"sub_file_{i}.txt"
        file_path.write_text(f"محتوای فایل زیرپوشه {i}\n", encoding='utf-8')
    
    return test_dir

def test_basic_operations(test_dir):
    """تست عملیات پایه"""
    print("\n" + "="*50)
    print("تست عملیات پایه")
    print("="*50)
    
    # تست کپی فایل
    source = test_dir / "file_1.txt"
    dest = test_dir / "file_1_copy_new.txt"
    copy_file(source, dest, overwrite=True)
    print(f"✅ کپی فایل: {source} -> {dest}")
    
    # تست جابجایی فایل
    source = test_dir / "file_2.txt"
    dest = test_dir / "moved_file.txt"
    move_file(source, dest, overwrite=True)
    print(f"✅ جابجایی فایل: {source} -> {dest}")
    
    # تست حذف فایل
    file_to_delete = test_dir / "file_3.txt"
    delete_file(file_to_delete)
    print(f"✅ حذف فایل: {file_to_delete}")
    
    # تست کپی پوشه
    source_folder = test_dir / "sub_folder"
    dest_folder = test_dir / "sub_folder_copy"
    copy_folder(source_folder, dest_folder, overwrite=True)
    print(f"✅ کپی پوشه: {source_folder} -> {dest_folder}")
    
    # تست حذف پوشه
    folder_to_delete = test_dir / "sub_folder_copy"
    delete_folder(folder_to_delete)
    print(f"✅ حذف پوشه: {folder_to_delete}")

def test_file_info(test_dir):
    """تست دریافت اطلاعات فایل"""
    print("\n" + "="*50)
    print("تست دریافت اطلاعات فایل")
    print("="*50)
    
    file_path = test_dir / "file_1.txt"
    
    # تست حجم فایل
    size = get_file_size(file_path)
    print(f"✅ حجم فایل: {size} بایت")
    
    # تست اطلاعات کامل فایل
    info = get_file_info(file_path)
    print(f"✅ اطلاعات فایل:")
    for key, value in info.items():
        print(f"   {key}: {value}")

def test_folder_operations(test_dir):
    """تست عملیات پوشه"""
    print("\n" + "="*50)
    print("تست عملیات پوشه")
    print("="*50)
    
    # تست حجم پوشه
    total_size = get_folder_size(test_dir)
    print(f"✅ حجم کل پوشه: {total_size} بایت")
    
    # تست پوشه مخفی
    hidden = is_hidden_file(test_dir)
    print(f"✅ آیا پوشه مخفی است؟ {hidden}")

def test_compression(test_dir):
    """تست فشرده‌سازی"""
    print("\n" + "="*50)
    print("تست فشرده‌سازی")
    print("="*50)
    
    # تست فشرده‌سازی پوشه
    zip_path = Path("test_archive.zip")
    zip_folder(test_dir, zip_path)
    print(f"✅ فشرده‌سازی پوشه: {zip_path}")
    
    # تست دریافت اطلاعات ZIP
    from filewizard.compress import get_zip_info
    info_list = get_zip_info(zip_path)
    print(f"✅ تعداد فایل‌های داخل ZIP: {len(info_list)}")
    
    # تست خارج‌سازی ZIP
    extract_dir = Path("extracted")
    unzip_file(zip_path, extract_dir, overwrite=True)
    print(f"✅ خارج‌سازی ZIP: {extract_dir}")
    
    # تست فشرده‌سازی چند فایل
    files_to_zip = [test_dir / "file_1.txt", test_dir / "file_1_copy_new.txt"]
    if all(f.exists() for f in files_to_zip):
        zip_files(files_to_zip, "multi_files.zip")
        print(f"✅ فشرده‌سازی چند فایل: multi_files.zip")
    
    # پاکسازی
    zip_path.unlink(missing_ok=True)
    shutil.rmtree(extract_dir, ignore_errors=True)
    Path("multi_files.zip").unlink(missing_ok=True)

def test_utilities(test_dir):
    """تست توابع کمکی"""
    print("\n" + "="*50)
    print("تست توابع کمکی")
    print("="*50)
    
    # تست ایجاد پوشه
    new_dir = Path("new_test_folder")
    ensure_directory(new_dir)
    print(f"✅ ایجاد پوشه: {new_dir}")
    
    # تست تغییر نام گروهی
    renamed = rename_files_pattern(test_dir, "test_{:03d}", [".txt"])
    print(f"✅ تغییر نام گروهی: {len(renamed)} فایل")
    for old, new in renamed[:3]:
        print(f"   {old} -> {new}")
    
    # تست پاکسازی پوشه (فقط فایل‌های .txt)
    deleted = clean_folder(test_dir, extensions=[".txt"], min_size=1)
    print(f"✅ پاکسازی پوشه: {len(deleted)} فایل حذف شد")
    
    # تست پیدا کردن فایل‌های تکراری
    # یک پوشه تکراری برای تست ایجاد می‌کنیم
    dup_dir = Path("dup_test")
    dup_dir.mkdir(exist_ok=True)
    for i in range(1, 4):
        file_path = dup_dir / f"dup_{i}.txt"
        file_path.write_text("محتوای یکسان برای تست تکراری\n", encoding='utf-8')
    
    duplicates = find_duplicate_files(dup_dir)
    print(f"✅ پیدا کردن فایل‌های تکراری: {len(duplicates)} گروه پیدا شد")
    for group in duplicates:
        print(f"   {len(group)} فایل تکراری: {group}")
    
    # پاکسازی
    shutil.rmtree(dup_dir, ignore_errors=True)
    shutil.rmtree(new_dir, ignore_errors=True)

def main():
    """اجرای همه تست‌ها"""
    print("\n" + "="*50)
    print("شروع تست جامع FileWizard")
    print("="*50)
    
    # ایجاد فایل‌های تست
    test_dir = create_test_files()
    
    try:
        test_basic_operations(test_dir)
        test_file_info(test_dir)
        test_folder_operations(test_dir)
        test_compression(test_dir)
        test_utilities(test_dir)
        
        print("\n" + "="*50)
        print("✅ همه تست‌ها با موفقیت انجام شدند!")
        print("="*50)
        
    except Exception as e:
        print(f"\n❌ خطا در تست: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # پاکسازی فایل‌های تست
        shutil.rmtree(test_dir, ignore_errors=True)
        print("\n🧹 فایل‌های تست پاکسازی شدند.")

if __name__ == "__main__":
    main()