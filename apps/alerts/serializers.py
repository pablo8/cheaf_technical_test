from rest_framework import serializers

from apps.alerts.models import Alert
from utils.constants import ALERT_STATUSES
from utils.helpers import output_date_format


class AlertSerializer(serializers.ModelSerializer):
    activation_date = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = Alert
        fields = '__all__'

    @staticmethod
    def get_activation_date(obj):
        try:
            return output_date_format(obj.activation_date)
        except:
            return None

    @staticmethod
    def get_status(obj):
        try:
            return {
                'id': obj.status,
                'value': dict(ALERT_STATUSES)[obj.status]
            }
        except:
            return None
