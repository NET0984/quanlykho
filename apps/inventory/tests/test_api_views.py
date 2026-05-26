from datetime import date
from decimal import Decimal

from rest_framework import status
from rest_framework.test import APITestCase

from apps.authentication.models import User
from apps.inventory.models import InventoryAudit, InventoryAuditItem, InventoryLoss
from apps.reports.models import ReportExportLog
from apps.product.models import Category, Product
from apps.warehouse.models import ProductStock


class InventoryApiFlowTests(APITestCase):
    def setUp(self):
        self.kho_user = User.objects.create_user(
            username='kho_inventory',
            password='Kho@123',
            full_name='Thu kho Inventory',
            role='KHO',
        )
        self.ketoan_user = User.objects.create_user(
            username='ketoan_inventory',
            password='KeToan@123',
            full_name='Ke toan Inventory',
            role='KE_TOAN',
        )

        self.category = Category.objects.create(name='Vat lieu test inventory')
        self.product_1 = Product.objects.create(
            name='Xi mang test inventory',
            base_price=Decimal('100000'),
            base_unit='Bao',
            category=self.category,
        )
        self.product_2 = Product.objects.create(
            name='Thep test inventory',
            base_price=Decimal('120000'),
            base_unit='Kg',
            category=self.category,
        )

        ProductStock.objects.create(
            product=self.product_1,
            quantity=Decimal('100'),
            reserved_quantity=Decimal('10'),
        )
        ProductStock.objects.create(
            product=self.product_2,
            quantity=Decimal('50'),
            reserved_quantity=Decimal('0'),
        )

    def test_audit_submit_approve_updates_stock_and_creates_loss(self):
        self.client.force_authenticate(user=self.kho_user)

        create_response = self.client.post(
            '/api/inventory/audits/',
            {
                'audit_date': date.today().isoformat(),
                'note': 'Kiem ke dinh ky',
                'product_ids': [str(self.product_1.id)],
            },
            format='json',
        )
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)

        audit_id = create_response.data['audit_id']
        detail_response = self.client.get(f'/api/inventory/audits/{audit_id}/')
        self.assertEqual(detail_response.status_code, status.HTTP_200_OK)

        item_id = detail_response.data['items'][0]['id']
        update_response = self.client.patch(
            f'/api/inventory/audits/{audit_id}/items/{item_id}/',
            {'actual_quantity': '90', 'note': 'Thieu hang khi kiem ke'},
            format='json',
        )
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)

        submit_response = self.client.post(f'/api/inventory/audits/{audit_id}/submit/', {}, format='json')
        self.assertEqual(submit_response.status_code, status.HTTP_200_OK)

        self.client.force_authenticate(user=self.ketoan_user)
        approve_response = self.client.post(f'/api/inventory/audits/{audit_id}/approve/', {}, format='json')
        self.assertEqual(approve_response.status_code, status.HTTP_200_OK)

        stock = ProductStock.objects.get(product=self.product_1)
        self.assertEqual(stock.quantity, Decimal('90'))
        self.assertEqual(stock.reserved_quantity, Decimal('10'))

        loss = InventoryLoss.objects.get(audit_item__audit_id=audit_id)
        self.assertEqual(loss.status, InventoryLoss.Status.PENDING)
        self.assertEqual(loss.loss_quantity, Decimal('10'))
        self.assertEqual(loss.product_id, self.product_1.id)

    def test_manual_loss_approve_decreases_stock(self):
        self.client.force_authenticate(user=self.kho_user)

        create_response = self.client.post(
            '/api/inventory/losses/',
            {
                'product_id': str(self.product_2.id),
                'loss_quantity': '5',
                'loss_type': InventoryLoss.LossType.DAMAGE,
                'loss_reason': 'Vo trong qua trinh van chuyen',
                'loss_date': date.today().isoformat(),
                'unit_cost': '120000',
            },
            format='json',
        )
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        loss_id = create_response.data['loss_id']

        self.client.force_authenticate(user=self.ketoan_user)
        approve_response = self.client.post(f'/api/inventory/losses/{loss_id}/approve/', {}, format='json')
        self.assertEqual(approve_response.status_code, status.HTTP_200_OK)

        stock = ProductStock.objects.get(product=self.product_2)
        self.assertEqual(stock.quantity, Decimal('45'))

    def test_discrepancy_report_returns_shortage_summary(self):
        audit = InventoryAudit.objects.create(
            audit_code='KK-TEST-001',
            audit_date=date.today(),
            note='Kiem ke nhanh',
            status=InventoryAudit.Status.APPROVED,
            created_by=self.kho_user,
            approved_by=self.ketoan_user,
        )
        InventoryAuditItem.objects.create(
            audit=audit,
            product=self.product_1,
            system_quantity=Decimal('100'),
            actual_quantity=Decimal('95'),
        )

        self.client.force_authenticate(user=self.kho_user)
        response = self.client.get('/api/inventory/discrepancy/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['summary']['shortage_count'], 1)
        statuses = [item['status'] for item in response.data['items']]
        self.assertIn('SHORTAGE', statuses)

    def test_stock_summary_export_excel_creates_log(self):
        self.client.force_authenticate(user=self.ketoan_user)
        response = self.client.get('/api/reports/stock-summary/export/?format=excel')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', response['Content-Type'])

        export_log = ReportExportLog.objects.filter(report_type='STOCK_SUMMARY').latest('exported_at')
        self.assertEqual(export_log.export_format, 'EXCEL')
        self.assertEqual(export_log.exported_by, self.ketoan_user)
        self.assertEqual(export_log.row_count, 2)

    def test_import_history_export_rejects_invalid_date_range(self):
        self.client.force_authenticate(user=self.ketoan_user)
        response = self.client.get('/api/reports/import-history/export/?date_from=2026-04-10&date_to=2026-04-01')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('date_to', response.data['errors'])
