from rest_framework import serializers
from apps.inventory.models import InventoryLoss

class ReportFilterSerializer(serializers.Serializer):
    date_from = serializers.DateField(required=False)
    date_to = serializers.DateField(required=False)

    def validate(self, attrs):
        date_from = attrs.get('date_from')
        date_to = attrs.get('date_to')
        if date_from and date_to and date_from > date_to:
            raise serializers.ValidationError({'date_to': 'Ngay ket thuc khong duoc nho hon ngay bat dau.'})
        return attrs


class DiscrepancyFilterSerializer(serializers.Serializer):
    product_id = serializers.UUIDField(required=False)
    category_id = serializers.UUIDField(required=False)


class ExportRequestSerializer(serializers.Serializer):
    format = serializers.ChoiceField(choices=['excel', 'pdf'], required=False, default='excel')
    date_from = serializers.DateField(required=False)
    to_date = serializers.DateField(required=False) # Supporting both names for flexibility
    date_to = serializers.DateField(required=False)
    loss_type = serializers.ChoiceField(choices=InventoryLoss.LossType.choices, required=False)
    category_id = serializers.UUIDField(required=False)
    audit_id = serializers.UUIDField(required=False)

    def validate(self, attrs):
        # Handle to_date vs date_to
        date_from = attrs.get('date_from')
        date_to = attrs.get('date_to') or attrs.get('to_date')
        if date_to:
            attrs['date_to'] = date_to
            
        if date_from and date_to and date_from > date_to:
            raise serializers.ValidationError({'date_to': 'Ngay ket thuc khong duoc nho hon ngay bat dau.'})
        return attrs
