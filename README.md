# 📁 FileWiz

**FileWiz** یک کتابخانه قدرتمند و سبک برای مدیریت و پردازش فایل‌ها و پوشه‌ها در پایتون است. با این کتابخانه، کارهای تکراری و پیچیده مانند کپی، جابجایی، حذف، فشرده‌سازی، پیدا کردن فایل‌های تکراری و تغییر نام گروهی را با چند خط کد انجام دهید.

[![PyPI version](https://badge.fury.io/py/filewiz.svg)](https://badge.fury.io/py/filewiz)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## ✨ ویژگی‌های کلیدی

- **مدیریت فایل‌ها**: کپی، جابجایی و حذف فایل‌ها و پوشه‌ها
- **فشرده‌سازی و خارج‌سازی**: پشتیبانی کامل از فرمت ZIP با قابلیت تنظیم سطح فشرده‌سازی
- **پیدا کردن فایل‌های تکراری**: با استفاده از الگوریتم‌های هش (MD5, SHA1, SHA256)
- **تغییر نام گروهی**: با الگوهای دلخواه (مثلاً `photo_001.jpg`)
- **پاکسازی هوشمند**: بر اساس پسوند یا حجم فایل‌ها
- **اطلاعات کامل**: دریافت جزئیات فایل‌ها (حجم، تاریخ، مخفی بودن و ...)
- **پشتیبانی از مسیرهای طولانی**: در ویندوز
- **بدون وابستگی‌های اضافی**: فقط با ماژول‌های استاندارد پایتون

---

## 📦 نصب

```bash
pip install filewiz
```

برای نصب آخرین نسخه در حال توسعه:
```bash
pip install git+https://github.com/0hasanbagheri0/FileWiz.git
```

---

## 🚀 شروع سریع

### ۱. عملیات پایه فایل و پوشه

```python
from filewiz import copy_file, move_file, delete_file, copy_folder, delete_folder

# کپی فایل
copy_file("source.txt", "destination.txt", overwrite=True)

# جابجایی فایل
move_file("old_location.txt", "new_location.txt", overwrite=True)

# حذف فایل (با گزینه force برای نادیده گرفتن خطا)
delete_file("unnecessary.log", force=True)

# کپی کل پوشه
copy_folder("my_project", "my_project_backup", overwrite=True)

# حذف پوشه و تمام محتویات آن
delete_folder("temp_folder", force=True)
```

### ۲. دریافت اطلاعات فایل‌ها

```python
from filewiz import get_file_info, get_file_size, get_folder_size

# دریافت اطلاعات کامل فایل
info = get_file_info("my_file.txt")
print(f"نام: {info['name']}")
print(f"حجم: {info['size']} بایت")
print(f"پسوند: {info['extension']}")
print(f"تاریخ تغییر: {info['modified']}")
print(f"مخفی است؟: {info['is_hidden']}")

# حجم یک فایل (به بایت)
size = get_file_size("my_file.txt")

# حجم کل یک پوشه (به بایت)
folder_size = get_folder_size("my_project")
```

### ۳. فشرده‌سازی و خارج‌سازی

```python
from filewiz import zip_folder, unzip_file, zip_files

# فشرده‌سازی یک پوشه
zip_folder("my_project", "project_backup.zip")

# فشرده‌سازی چند فایل مشخص
zip_files(["file1.txt", "file2.csv"], "my_files.zip")

# خارج‌سازی فایل ZIP (با حفظ ساختار پوشه‌ها)
unzip_file("archive.zip", "extracted_files", overwrite=True)

# دریافت لیست فایل‌های داخل ZIP (بدون خارج‌سازی)
from filewiz.compress import get_zip_info
contents = get_zip_info("archive.zip")
for item in contents:
    print(f"{item['name']} - {item['size']} bytes")
```

### ۴. ابزارهای پیشرفته

```python
from filewiz import (
    find_duplicate_files, 
    clean_folder, 
    rename_files_pattern,
    ensure_directory
)

# ایجاد پوشه در صورت وجود نداشتن (به همراه پوشه‌های والد)
ensure_directory("new_project/data/images")

# پیدا کردن فایل‌های تکراری در یک پوشه
duplicates = find_duplicate_files("downloads")
for group in duplicates:
    print(f"{len(group)} فایل تکراری: {group}")

# تغییر نام گروهی با الگو (مثلاً برای عکس‌ها)
renamed = rename_files_pattern("photos", "photo_{:03d}", [".jpg", ".png"])
for old, new in renamed:
    print(f"{old} -> {new}")

# پاکسازی پوشه (مثلاً حذف فایل‌های موقت)
deleted = clean_folder(
    directory="temp",
    extensions=[".tmp", ".log"],
    min_size=1024  # حداقل حجم ۱ کیلوبایت
)
print(f"{len(deleted)} فایل حذف شد")
```

---

## 📚 راهنمای کامل توابع

### توابع اصلی (`filewiz.core`)

| تابع | توضیح |
|------|-------|
| `copy_file(src, dst, overwrite=False)` | کپی فایل با قابلیت بازنویسی |
| `move_file(src, dst, overwrite=False)` | جابجایی فایل |
| `delete_file(path, force=False)` | حذف فایل |
| `copy_folder(src, dst, overwrite=False)` | کپی کل پوشه (به همراه زیرپوشه‌ها) |
| `move_folder(src, dst, overwrite=False)` | جابجایی پوشه |
| `delete_folder(path, force=False)` | حذف پوشه و تمام محتویات |
| `get_file_size(path)` | دریافت حجم فایل (بایت) |
| `get_folder_size(path)` | دریافت حجم کل پوشه (بایت) |
| `get_file_info(path)` | دریافت اطلاعات کامل فایل (نام، حجم، تاریخ، و ...) |
| `ensure_directory(path)` | ایجاد پوشه در صورت عدم وجود |

### توابع فشرده‌سازی (`filewiz.compress`)

| تابع | توضیح |
|------|-------|
| `zip_folder(src, dst, compression=ZIP_DEFLATED)` | فشرده‌سازی پوشه به ZIP |
| `unzip_file(zip_path, extract_to, overwrite=False)` | خارج‌سازی فایل ZIP |
| `zip_files(files, output, compression=ZIP_DEFLATED)` | فشرده‌سازی چند فایل |
| `get_zip_info(zip_path)` | دریافت لیست محتویات ZIP |

### توابع کمکی (`filewiz.utils`)

| تابع | توضیح |
|------|-------|
| `find_duplicate_files(directory)` | پیدا کردن فایل‌های تکراری |
| `clean_folder(directory, extensions, min_size, max_size)` | پاکسازی پوشه بر اساس شرایط |
| `rename_files_pattern(directory, pattern, extensions)` | تغییر نام گروهی فایل‌ها |
| `get_file_extension(path)` | دریافت پسوند فایل |
| `is_hidden_file(path)` | تشخیص فایل یا پوشه مخفی |

---

## 🛠️ نیازمندی‌ها

- **Python 3.7** یا بالاتر
- بدون وابستگی‌های خارجی

---

## 🤝 مشارکت

خوشحال می‌شویم در بهبود این کتابخانه مشارکت کنید:

1. مخزن را **Fork** کنید.
2. یک شاخه جدید بسازید (`git checkout -b feature/amazing-feature`).
3. تغییرات را Commit کنید (`git commit -m 'Add amazing feature'`).
4. به شاخه خود Push کنید (`git push origin feature/amazing-feature`).
5. یک **Pull Request** باز کنید.

---

## 📄 مجوز

این پروژه تحت مجوز **MIT** منتشر شده است.

---

## 📧 ارتباط با من

- **ایمیل**: hasan111bagher@gmail.com
- **گیت‌هاب**: [0hasanbagheri0](https://github.com/0hasanbagheri0)

---

**✨ اگر این کتابخانه برای شما مفید بود، به آن یک ⭐ در گیت‌هاب بدهید!**
