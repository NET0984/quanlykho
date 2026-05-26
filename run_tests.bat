@echo off
REM Batch file để chạy unit tests trên Windows
REM Lưu file này tại thư mục gốc của project

echo ============================================
echo Django Unit Tests Runner
echo ============================================
echo.

REM Kiểm tra nếu không có tham số
if "%1"=="" (
    echo Sử dụng:
    echo.
    echo Chạy tất cả tests:
    echo   run_tests.bat all
    echo.
    echo Chạy authentication tests:
    echo   run_tests.bat auth
    echo.
    echo Chạy product tests:
    echo   run_tests.bat product
    echo.
    echo Chạy with verbose:
    echo   run_tests.bat verbose
    echo.
    exit /b 1
)

if "%1"=="all" (
    echo Chạy TẤT CẢ tests...
    python manage.py test
) else if "%1"=="auth" (
    echo Chạy AUTHENTICATION tests...
    python manage.py test apps.authentication.test_services
) else if "%1"=="product" (
    echo Chạy PRODUCT tests...
    python manage.py test apps.product.test_services
) else if "%1"=="verbose" (
    echo Chạy tất cả tests với VERBOSE mode...
    python manage.py test --verbosity=2
) else if "%1"=="keep" (
    echo Chạy tests và giữ database (nhanh hơn)...
    python manage.py test --keepdb
) else (
    echo Tham số không hợp lệ: %1
    exit /b 1
)

echo.
echo ============================================
echo Hoàn thành!
echo ============================================
