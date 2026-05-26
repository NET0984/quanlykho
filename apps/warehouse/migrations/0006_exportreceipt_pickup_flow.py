from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('warehouse', '0005_exportreceipt_sales_order_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='exportreceipt',
            name='picked_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='exportreceipt',
            name='pickup_photo',
            field=models.ImageField(blank=True, null=True, upload_to='export_receipts/pickups/'),
        ),
        migrations.AddField(
            model_name='exportreceipt',
            name='picked_by',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='export_receipts_picked',
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name='exportreceipt',
            name='stock_deducted',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='exportreceipt',
            name='status',
            field=models.CharField(
                choices=[
                    ('PREPARING', 'Cho lay hang'),
                    ('PENDING', 'Cho duyet'),
                    ('APPROVED', 'Da duyet'),
                    ('REJECTED', 'Tu choi'),
                ],
                default='PENDING',
                max_length=10,
            ),
        ),
    ]
