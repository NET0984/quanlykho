#!/bin/bash
# Shell script để chạy unit tests trên Linux/Mac

echo "============================================"
echo "Django Unit Tests Runner"
echo "============================================"
echo ""

if [ -z "$1" ]; then
    echo "Sử dụng:"
    echo ""
    echo "Chạy tất cả tests:"
    echo "  ./run_tests.sh all"
    echo ""
    echo "Chạy authentication tests:"
    echo "  ./run_tests.sh auth"
    echo ""
    echo "Chạy product tests:"
    echo "  ./run_tests.sh product"
    echo ""
    echo "Chạy with verbose:"
    echo "  ./run_tests.sh verbose"
    echo ""
    exit 1
fi

case "$1" in
    all)
        echo "Chạy TẤT CẢ tests..."
        python manage.py test
        ;;
    auth)
        echo "Chạy AUTHENTICATION tests..."
        python manage.py test apps.authentication.test_services
        ;;
    product)
        echo "Chạy PRODUCT tests..."
        python manage.py test apps.product.test_services
        ;;
    verbose)
        echo "Chạy tất cả tests với VERBOSE mode..."
        python manage.py test --verbosity=2
        ;;
    keep)
        echo "Chạy tests và giữ database (nhanh hơn)..."
        python manage.py test --keepdb
        ;;
    *)
        echo "Tham số không hợp lệ: $1"
        exit 1
        ;;
esac

echo ""
echo "============================================"
echo "Hoàn thành!"
echo "============================================"
