"""
apps/product/views.py - updated for product and stock display.
"""
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.views import View

from middlewares.upload_middleware import xu_ly_va_luu_anh, xoa_anh_cu

from .forms import CategoryForm, ProductForm
from .services import CategoryService, ProductService
from .validators import ProductUnitValidator


def _get_stock_map():
    """Lay dict {product_id: quantity} tu ton kho, mac dinh 0."""
    try:
        from apps.warehouse.models import ProductStock
        stocks = ProductStock.objects.all().values('product_id', 'quantity')
        return {str(s['product_id']): float(s['quantity']) for s in stocks}
    except Exception:
        return {}


def _build_pagination_items(current_page, total_pages, window=1):
    if total_pages <= 0:
        return []

    pages = {1, total_pages}
    for page_num in range(current_page - window, current_page + window + 1):
        if 1 <= page_num <= total_pages:
            pages.add(page_num)

    sorted_pages = sorted(pages)
    items = []
    previous = None
    for page_num in sorted_pages:
        if previous is not None and page_num - previous > 1:
            items.append('ellipsis')
        items.append(page_num)
        previous = page_num
    return items


class ProductListView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'product.view_product'
    raise_exception = True

    def get(self, request):
        service = ProductService()
        cat_service = CategoryService()

        search_query = request.GET.get('search', '').strip()
        category_id = request.GET.get('category', '')
        page_number = request.GET.get('page', 1)

        queryset = service.get_all_products(
            search=search_query if search_query else None,
            category=category_id if category_id else None,
        )

        paginator = Paginator(queryset, 5)
        page_obj = paginator.get_page(page_number)
        pagination_items = _build_pagination_items(page_obj.number, paginator.num_pages, window=1)
        stock_map = _get_stock_map()
        for product in page_obj.object_list:
            stock_map.setdefault(str(product.id), 0)

        return render(request, 'product/product_list.html', {
            'products': page_obj.object_list,
            'categories': cat_service.get_list(),
            'tong_so_luong': paginator.count,
            'search_query': search_query,
            'category_id': category_id,
            'paginator': paginator,
            'page_obj': page_obj,
            'pagination_items': pagination_items,
            'stock_map_json': __import__('json').dumps(stock_map),
        })


class ProductDetailView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'product.view_product'
    raise_exception = True

    def get(self, request, pk):
        service = ProductService()
        product = service.repository.get_by_id(pk)
        units = service.unit_repository.get_by_product(pk)

        return render(request, 'product/detail.html', {
            'product': product,
            'units': units,
        })


class ProductCreateView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'product.add_product'
    raise_exception = True

    def post(self, request):
        form = ProductForm(request.POST, request.FILES)
        if not form.is_valid():
            messages.error(request, 'Dữ liệu không hợp lệ, vui lòng kiểm tra lại.')
            return redirect('product:product_list')

        form_data = {
            'name': form.cleaned_data['name'],
            'category': form.cleaned_data['category'],
            'base_price': form.cleaned_data['base_price'],
            'base_unit': form.cleaned_data['base_unit'],
        }

        file_anh = form.cleaned_data.get('anh_san_pham')
        if file_anh:
            try:
                form_data['image_url'] = xu_ly_va_luu_anh(file_anh, thu_muc_con='san-pham')
            except ValueError as exc:
                messages.error(request, f'Lỗi ảnh: {exc}')
                return redirect('product:product_list')

        ProductService().create_product(form_data)
        messages.success(request, 'Tạo sản phẩm thành công!')
        return redirect('product:product_list')


class ProductUpdateView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'product.change_product'
    raise_exception = True

    def get(self, request, pk):
        return redirect('product:product_list')

    def post(self, request, pk):
        service = ProductService()
        product = service.repository.get_by_id(pk)
        form = ProductForm(request.POST, request.FILES, instance=product)

        if not form.is_valid():
            messages.error(request, 'Lỗi cập nhật. Vui lòng kiểm tra lại thông tin.')
            return redirect('product:product_list')

        update_data = {
            'name': form.cleaned_data['name'],
            'category': form.cleaned_data['category'],
            'base_price': form.cleaned_data['base_price'],
            'base_unit': form.cleaned_data['base_unit'],
            'image_url': product.image_url,
        }

        file_anh = form.cleaned_data.get('anh_san_pham')
        if file_anh:
            try:
                xoa_anh_cu(product.image_url)
                update_data['image_url'] = xu_ly_va_luu_anh(file_anh, thu_muc_con='san-pham')
            except ValueError as exc:
                messages.error(request, f'Lỗi ảnh: {exc}')
                return redirect('product:product_list')

        service.repository.update(product, update_data)
        messages.success(request, 'Cập nhật sản phẩm thành công!')
        return redirect('product:product_list')


class ProductDeleteView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'product.delete_product'
    raise_exception = True

    def post(self, request, pk):
        service = ProductService()
        product = service.repository.get_by_id(pk)

        if product:
            xoa_anh_cu(product.image_url)
            service.repository.delete(product)
            messages.warning(request, 'Đã xóa sản phẩm thành công.')
        else:
            messages.error(request, 'Không tìm thấy sản phẩm để xóa.')

        return redirect('product:product_list')


class CategoryListView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'product.view_category'
    raise_exception = True

    def get(self, request):
        service = CategoryService()
        categories = service.get_list()
        return render(request, 'categories/category_list.html', {
            'categories': categories,
            'form': CategoryForm(),
        })

    def post(self, request):
        form = CategoryForm(request.POST)
        if form.is_valid():
            category, msg = CategoryService().create_category(form.cleaned_data['name'])
            if category:
                messages.success(request, 'Da them danh muc moi thanh cong!')
            else:
                messages.error(request, msg or 'Du lieu khong hop le, vui long kiem tra lai.')
        else:
            messages.error(request, 'Du lieu khong hop le, vui long kiem tra lai.')
        return redirect('product:category_list')


class CategoryUpdateView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'product.change_category'
    raise_exception = True

    def post(self, request, pk):
        service = CategoryService()
        category = service.repository.get_by_id(pk)
        name = request.POST.get('name')

        if name:
            service.repository.update(category, name)
            messages.success(request, 'Cap nhat danh muc thanh cong!')
        else:
            messages.error(request, 'Ten danh muc khong duoc de trong.')
        return redirect('product:category_list')


class CategoryDeleteView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'product.delete_category'
    raise_exception = True

    def post(self, request, pk):
        service = CategoryService()
        category = service.repository.get_by_id(pk)

        if category.products.exists():
            messages.error(request, 'Khong the xoa danh muc dang co san pham!')
        else:
            service.repository.delete(category)
            messages.warning(request, 'Da xoa danh muc.')
        return redirect('product:category_list')


class ProductUnitListView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'product.view_productunit'
    raise_exception = True

    def get(self, request):
        service = ProductService()
        units = service.unit_repository.get_all()
        products = service.repository.get_all()
        return render(request, 'units/unit_list.html', {
            'units': units,
            'products': products,
            'title': 'Quan ly Don vi & Quy doi',
        })


class ProductUnitCreateView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'product.add_productunit'
    raise_exception = True

    def post(self, request):
        data = {
            'unit_name': request.POST.get('unit_name', ''),
            'conversion_rate': request.POST.get('conversion_rate', ''),
            'product_id': request.POST.get('product_id', ''),
        }

        errors = ProductUnitValidator.validate_create(data)
        if errors:
            for message in errors.values():
                messages.error(request, message)
            return redirect('product:units_list')

        unit, msg = ProductService().add_new_unit_to_product(
            data['product_id'],
            data['unit_name'],
            data['conversion_rate'],
        )

        if unit:
            messages.success(request, f"Da them don vi {data['unit_name']} thanh cong.")
        else:
            messages.error(request, msg)
        return redirect('product:units_list')


class ProductUnitUpdateView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'product.change_productunit'
    raise_exception = True

    def post(self, request, pk):
        service = ProductService()
        unit = service.unit_repository.get_by_id(pk)

        if not unit:
            messages.error(request, 'Khong tim thay don vi tinh.')
            return redirect('product:units_list')

        unit_name = request.POST.get('unit_name')
        conversion_rate = request.POST.get('conversion_rate')

        if unit_name and conversion_rate:
            service.unit_repository.update(unit, {
                'unit_name': unit_name,
                'conversion_rate': conversion_rate,
            })
            messages.success(request, 'Cap nhat thanh cong!')
        else:
            messages.error(request, 'Vui long dien du thong tin.')
        return redirect('product:units_list')


class ProductUnitDeleteView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'product.delete_productunit'
    raise_exception = True

    def post(self, request, pk):
        service = ProductService()
        if service.unit_repository.delete(pk):
            messages.warning(request, 'Da xoa don vi tinh thanh cong.')
        else:
            messages.error(request, 'Khong tim thay don vi tinh de xoa.')
        return redirect('product:units_list')
