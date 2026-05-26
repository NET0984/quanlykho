from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_remove_warehousetransaction_warehouse_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CustomerDebt',
        ),
    ]
