import json
from decimal import Decimal

from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Sum
from django.http import HttpResponse
from django.utils import timezone

from apps.product.models import Product

from .excel_utils import build_template_workbook, export_receipts_workbook, workbook_to_response_bytes
from .models import ExportReceipt, ExportReceiptItem, ImportReceipt, ImportReceiptItem
from .services import ExportReceiptService, ImportReceiptService, StockService


PAGE_SIZE = 5


def _excel_response(workbook, filename):
    response = HttpResponse(
        workbook_to_response_bytes(workbook),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response


def _products_json():
    products = Product.objects.select_related('category').all().order_by('name')
    return [
        {
            'id': str(product.id),
            'name': product.name,
            'base_unit': product.base_unit,
            'base_price': float(product.base_price),
            'category': product.category.name if product.category else '',
        }
        for product in products
    ]


def _parse_items_from_post(post_data):
    items = []
    index = 0
    while True:
        product_id = post_data.get(f'product_id_{index}')
        if product_id is None:
            break
        if product_id:
            items.append(
                {
                    'product_id': product_id,
                    'quantity': post_data.get(f'quantity_{index}', 0),
                    'unit_price': post_data.get(f'unit_price_{index}', 0),
                    'note': post_data.get(f'item_note_{index}', ''),
                }
            )
        index += 1
    return items


def _get_import_receipt_stats():
    today = timezone.now().date()
    return {
        'total_receipts': ImportReceipt.objects.count(),
        'pending_receipts': ImportReceipt.objects.filter(status='PENDING').count(),
        'total_items': ImportReceiptItem.objects.aggregate(total=Sum('quantity'))['total'] or 0,
        'today_transactions': ImportReceipt.objects.filter(created_at__date=today).count(),
    }


def _get_export_receipt_stats():
    today = timezone.now().date()
    return {
        'total_receipts': ExportReceipt.objects.count(),
        'preparing_receipts': ExportReceipt.objects.filter(status='PREPARING').count(),
        'pending_receipts': ExportReceipt.objects.filter(status='PENDING').count(),
        'total_items': ExportReceiptItem.objects.aggregate(total=Sum('quantity'))['total'] or 0,
        'today_transactions': ExportReceipt.objects.filter(created_at__date=today).count(),
    }


PAGE_SIZE = 5  # Số phiếu mỗi trang


def _get_user_display_name(user):
    full_name = ''
    if hasattr(user, 'get_full_name'):
        full_name = (user.get_full_name() or '').strip()
    return full_name or getattr(user, 'username', '') or 'Khong ro'


def _format_report_number(value):
    decimal_value = Decimal(str(value))
    formatted = f"{decimal_value:,.10f}".rstrip('0').rstrip('.')
    return formatted or '0'


# ═══════════════════════════════════════════════════════════════
# NHẬP KHO
# ═══════════════════════════════════════════════════════════════

class ImportReceiptListView(LoginRequiredMixin, View):
    def get(self, request):
        service = ImportReceiptService()
        receipts = service.get_all()
        status_filter = request.GET.get('status', '')
        search_query = request.GET.get('search', '')
        page_number = request.GET.get('page', 1)

        if status_filter:
            receipts = receipts.filter(status=status_filter)
        if search_query:
            receipts = receipts.filter(Q(receipt_code__icontains=search_query) | Q(note__icontains=search_query))

        paginator = Paginator(receipts, PAGE_SIZE)
        page_obj = paginator.get_page(page_number)
        return render(
            request,
            'warehouse/import_receipt_list.html',
            {
                'receipts': page_obj,
                'page_obj': page_obj,
                'paginator': paginator,
                'products_json': json.dumps(_products_json(), ensure_ascii=False),
                'status_filter': status_filter,
                'search_query': search_query,
                'user_role': 'ADMIN' if request.user.is_superuser else request.user.role,
                'stats': _get_import_receipt_stats(),
            },
        )

    def post(self, request):
        if request.user.role not in ('KHO', 'ADMIN') and not request.user.is_superuser:
            messages.error(request, 'Ban khong co quyen tao phieu nhap kho.')
            return redirect('warehouse:import_list')

        receipt, error = ImportReceiptService().create_receipt(
            request.POST.get('note', ''),
            _parse_items_from_post(request.POST),
            request.user,
        )
        if receipt:
            messages.success(request, f'Da tao phieu nhap {receipt.receipt_code} thanh cong. Dang cho duyet.')
        else:
            messages.error(request, error)
        return redirect('warehouse:import_list')


class ImportReceiptExcelTemplateView(LoginRequiredMixin, View):
    def get(self, request):
        return _excel_response(build_template_workbook('import'), 'mau-phieu-nhap.xlsx')


class ImportReceiptExcelUploadView(LoginRequiredMixin, View):
    def post(self, request):
        if request.user.role not in ('KHO', 'ADMIN') and not request.user.is_superuser:
            messages.error(request, 'Ban khong co quyen import phieu nhap kho.')
            return redirect('warehouse:import_list')
        uploaded_file = request.FILES.get('excel_file')
        if not uploaded_file:
            messages.error(request, 'Vui long chon file Excel.')
            return redirect('warehouse:import_list')
        try:
            receipts = ImportReceiptService().import_receipts_from_excel(uploaded_file, request.user)
            messages.success(request, f'Da import {len(receipts)} phieu nhap tu Excel.')
        except ValueError as exc:
            messages.error(request, str(exc))
        return redirect('warehouse:import_list')


class ImportReceiptExcelExportView(LoginRequiredMixin, View):
    def get(self, request):
        queryset = ImportReceiptService().get_all()
        status_filter = request.GET.get('status', '')
        search_query = request.GET.get('search', '')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        if search_query:
            queryset = queryset.filter(Q(receipt_code__icontains=search_query) | Q(note__icontains=search_query))
        return _excel_response(export_receipts_workbook(queryset, 'import'), 'danh-sach-phieu-nhap.xlsx')


class ImportReceiptDetailView(LoginRequiredMixin, View):
    def get(self, request, pk):
        receipt = ImportReceiptService().get_by_id(pk)
        if not receipt:
            messages.error(request, 'Khong tim thay phieu nhap kho.')
            return redirect('warehouse:import_list')
        return render(
            request,
            'warehouse/import_receipt_detail.html',
            {
                'receipt': receipt,
                'products_json': json.dumps(_products_json(), ensure_ascii=False),
                'user_role': 'ADMIN' if request.user.is_superuser else request.user.role,
            },
        )


class ImportReceiptApproveView(LoginRequiredMixin, View):
    def post(self, request, pk):
        if request.user.role not in ('KE_TOAN', 'ADMIN') and not request.user.is_superuser:
            messages.error(request, 'Ban khong co quyen duyet phieu.')
            return redirect('warehouse:import_list')
        success, message = ImportReceiptService().approve_receipt(pk, request.user)
        messages.success(request, message) if success else messages.error(request, message)
        return redirect('warehouse:import_list')


class ImportReceiptRejectView(LoginRequiredMixin, View):
    def post(self, request, pk):
        if request.user.role not in ('KE_TOAN', 'ADMIN') and not request.user.is_superuser:
            messages.error(request, 'Ban khong co quyen tu choi phieu.')
            return redirect('warehouse:import_list')
        success, message = ImportReceiptService().reject_receipt(pk, request.user, request.POST.get('rejection_note', ''))
        messages.warning(request, message) if success else messages.error(request, message)
        return redirect('warehouse:import_list')


class ImportReceiptResubmitView(LoginRequiredMixin, View):
    def post(self, request, pk):
        if request.user.role not in ('KHO', 'ADMIN') and not request.user.is_superuser:
            messages.error(request, 'Ban khong co quyen gui lai phieu.')
            return redirect('warehouse:import_list')
        receipt, error = ImportReceiptService().resubmit_receipt(
            pk,
            request.POST.get('note', ''),
            _parse_items_from_post(request.POST),
            request.user,
        )
        if receipt:
            messages.success(request, f'Da gui lai phieu {receipt.receipt_code}. Dang cho duyet.')
        else:
            messages.error(request, error)
        return redirect('warehouse:import_list')


class StockListView(LoginRequiredMixin, View):
    def get(self, request):
        service = StockService()
        search_query = request.GET.get('search', '')
        page_number = request.GET.get('page', 1)
        stocks = service.get_all_stocks()
        if search_query:
            lowered = search_query.lower()
            stocks = [
                row
                for row in stocks
                if lowered in row['product'].name.lower()
                or lowered in (row['product'].category.name.lower() if row['product'].category else '')
            ]

        paginator = Paginator(stocks, 12)
        page_obj = paginator.get_page(page_number)

        return render(request, 'warehouse/stock_list.html', {
            'stocks': page_obj,
            'page_obj': page_obj,
            'paginator': paginator,
            'search_query': search_query,
            'user_role': 'ADMIN' if request.user.is_superuser else request.user.role,
        })




# ═══════════════════════════════════════════════════════════════
# XUẤT KHO — Tất cả role đều có thể duyệt
# ═══════════════════════════════════════════════════════════════

EXPORT_APPROVE_ROLES = ('KHO', 'KE_TOAN', 'ADMIN', 'SALE')


class ExportReceiptListView(LoginRequiredMixin, View):
    def get(self, request):
        service = ExportReceiptService()
        receipts = service.get_all()
        status_filter = request.GET.get('status', '')
        search_query = request.GET.get('search', '')
        page_number = request.GET.get('page', 1)

        if status_filter:
            receipts = receipts.filter(status=status_filter)
        if search_query:
            receipts = receipts.filter(
                Q(receipt_code__icontains=search_query)
                | Q(note__icontains=search_query)
                | Q(sales_order__order_code__icontains=search_query)
            )

        paginator = Paginator(receipts, PAGE_SIZE)
        page_obj = paginator.get_page(page_number)
        return render(
            request,
            'warehouse/export_receipt_list.html',
            {
                'receipts': page_obj,
                'page_obj': page_obj,
                'paginator': paginator,
                'products_json': json.dumps(_products_json(), ensure_ascii=False),
                'status_filter': status_filter,
                'search_query': search_query,
                'user_role': 'ADMIN' if request.user.is_superuser else request.user.role,
                'stats': _get_export_receipt_stats(),
            },
        )

    def post(self, request):
        if request.user.role not in ('KHO', 'ADMIN') and not request.user.is_superuser:
            messages.error(request, 'Ban khong co quyen tao phieu xuat kho.')
            return redirect('warehouse:export_list')

        receipt, error = ExportReceiptService().create_receipt(
            request.POST.get('note', ''),
            _parse_items_from_post(request.POST),
            request.user,
        )
        if receipt:
            messages.success(request, f'Da tao phieu xuat {receipt.receipt_code} thanh cong. Dang cho duyet.')
        else:
            messages.error(request, error)
        return redirect('warehouse:export_list')


class ExportReceiptExcelTemplateView(LoginRequiredMixin, View):
    def get(self, request):
        return _excel_response(build_template_workbook('export'), 'mau-phieu-xuat.xlsx')


class ExportReceiptExcelUploadView(LoginRequiredMixin, View):
    def post(self, request):
        if request.user.role not in ('KHO', 'ADMIN') and not request.user.is_superuser:
            messages.error(request, 'Ban khong co quyen import phieu xuat kho.')
            return redirect('warehouse:export_list')
        uploaded_file = request.FILES.get('excel_file')
        if not uploaded_file:
            messages.error(request, 'Vui long chon file Excel.')
            return redirect('warehouse:export_list')
        try:
            receipts = ExportReceiptService().import_receipts_from_excel(uploaded_file, request.user)
            messages.success(request, f'Da import {len(receipts)} phieu xuat tu Excel.')
        except ValueError as exc:
            messages.error(request, str(exc))
        return redirect('warehouse:export_list')


class ExportReceiptExcelExportView(LoginRequiredMixin, View):
    def get(self, request):
        queryset = ExportReceiptService().get_all()
        status_filter = request.GET.get('status', '')
        search_query = request.GET.get('search', '')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        if search_query:
            queryset = queryset.filter(
                Q(receipt_code__icontains=search_query)
                | Q(note__icontains=search_query)
                | Q(sales_order__order_code__icontains=search_query)
            )
        return _excel_response(export_receipts_workbook(queryset, 'export'), 'danh-sach-phieu-xuat.xlsx')


class ExportReceiptDetailView(LoginRequiredMixin, View):
    def get(self, request, pk):
        receipt = ExportReceiptService().get_by_id(pk)
        if not receipt:
            messages.error(request, 'Khong tim thay phieu xuat kho.')
            return redirect('warehouse:export_list')
        return render(
            request,
            'warehouse/export_receipt_detail.html',
            {
                'receipt': receipt,
                'products_json': json.dumps(_products_json(), ensure_ascii=False),
                'user_role': 'ADMIN' if request.user.is_superuser else request.user.role,
            },
        )


class ExportReceiptMarkPickedView(LoginRequiredMixin, View):
    def post(self, request, pk):
        if request.user.role not in ('KHO', 'ADMIN') and not request.user.is_superuser:
            messages.error(request, 'Ban khong co quyen xac nhan da lay hang.')
            return redirect('warehouse:export_list')
        success, message = ExportReceiptService().mark_as_picked(
            pk,
            request.user,
            pickup_photo=request.FILES.get('pickup_photo'),
        )
        messages.success(request, message) if success else messages.error(request, message)
        return redirect('warehouse:export_list')


class ExportReceiptApproveView(LoginRequiredMixin, View):
    def post(self, request, pk):
        if request.user.role not in EXPORT_APPROVE_ROLES and not request.user.is_superuser:
            messages.error(request, 'Bạn không có quyền duyệt phiếu xuất.')
            return redirect('warehouse:export_list')

        service = ExportReceiptService()
        success, msg = service.approve_receipt(pk, request.user)
        if success:
            messages.success(request, msg)
        else:
            messages.error(request, msg)
        return redirect('warehouse:export_list')


class ExportReceiptRejectView(LoginRequiredMixin, View):
    def post(self, request, pk):
        if request.user.role not in EXPORT_APPROVE_ROLES and not request.user.is_superuser:
            messages.error(request, 'Bạn không có quyền từ chối phiếu xuất.')
            return redirect('warehouse:export_list')

        service = ExportReceiptService()
        rejection_note = request.POST.get('rejection_note', '')
        success, msg = service.reject_receipt(pk, request.user, rejection_note)
        if success:
            messages.warning(request, msg)
        else:
            messages.error(request, msg)
        return redirect('warehouse:export_list')


class ExportReceiptResubmitView(LoginRequiredMixin, View):
    def post(self, request, pk):
        if request.user.role not in ('KHO', 'ADMIN') and not request.user.is_superuser:
            messages.error(request, 'Ban khong co quyen gui lai phieu.')
            return redirect('warehouse:export_list')
        receipt, error = ExportReceiptService().resubmit_receipt(
            pk,
            request.POST.get('note', ''),
            _parse_items_from_post(request.POST),
            request.user,
        )
        if receipt:
            messages.success(request, f'Da gui lai phieu {receipt.receipt_code}.')
        else:
            messages.error(request, error)
        return redirect('warehouse:export_list')
