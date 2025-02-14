from rest_framework import serializers

from apps.alerts.serializers import AlertLiteSerializer
from apps.products.models import Product
from utils.helpers import output_date_format


class ProductSerializer(serializers.ModelSerializer):
    alerts = serializers.SerializerMethodField()
    expiration_date = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'

    @staticmethod
    def get_alerts(obj):
        try:
            return AlertLiteSerializer(instance=obj.alert_set.all(), many=True).data
        except:
            return None

    @staticmethod
    def get_expiration_date(obj):
        try:
            return output_date_format(obj.expiration_date)
        except:
            return None
