from django.db.models import Q
from django.db.models.deletion import ProtectedError

from apps.product.models import Product

candidates = Product.objects.filter(
    Q(stock__isnull=True) | Q(stock__quantity__lte=0)
).distinct().order_by('name')

candidate_count = candidates.count()
deleted_names = []
skipped = []

for product in candidates:
    try:
        product.delete()
        deleted_names.append(product.name)
    except ProtectedError as exc:
        skipped.append((product.name, len(exc.protected_objects)))

print('CLEANUP_DONE')
print(f'CANDIDATES={candidate_count}')
print(f'DELETED={len(deleted_names)}')
for name in deleted_names:
    print(f'- DELETED: {name}')

print(f'SKIPPED={len(skipped)}')
for name, refs in skipped:
    print(f'- SKIPPED: {name} (protected refs: {refs})')

print(f'TOTAL_PRODUCTS_NOW={Product.objects.count()}')
