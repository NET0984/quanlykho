from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('order', '0003_remove_customerdebt'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salesorder',
            name='status',
            field=models.CharField(
                choices=[
                    ('CONFIRMED', 'Da xac nhan'),
                    ('WAITING', 'Cho lay hang'),
                    ('PICKED', 'Da lay hang'),
                    ('DONE', 'Hoan thanh'),
                    ('CANCELLED', 'Da huy'),
                ],
                default='CONFIRMED',
                max_length=15,
            ),
        ),
    ]
