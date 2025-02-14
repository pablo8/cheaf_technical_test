from celery import shared_task
from django.utils.timezone import now
from django.core.mail import send_mail
from django.conf import settings

from utils.constants import STATUS_ACTIVE_ID, STATUS_EXPIRED_ID

from apps.alerts.models import Alert
from apps.core.models import User

@shared_task
def update_alerts():
    """
    Tarea programada para actualizar los campos `days_to_activation` y `days_since_activation`
    en todas las alertas activas. Si `days_to_activation` llega a 0, dispara la notificación.
    """
    today = now().date()

    alerts = Alert.objects.filter(activation_date__isnull=False, status=STATUS_ACTIVE_ID)

    updated_alerts = []
    alerts_to_notify = []

    for alert in alerts:
        activation_date = alert.activation_date.date()
        alert.days_to_activation = max((activation_date - today).days, 0)
        alert.days_since_activation = max((today - activation_date).days, 0)

        # Si la alerta se activa hoy, se notifica
        if alert.days_to_activation == 0:
            alerts_to_notify.append(alert.id)

        updated_alerts.append(alert)

    Alert.objects.bulk_update(updated_alerts, ['days_to_activation', 'days_since_activation'])

    # Validar si hay alertas que vencerán hoy
    if alerts_to_notify:
        send_alert_notifications.delay(alerts_to_notify)
    return f"Actualizadas {len(updated_alerts)} alertas. Alertas notificadas: {len(alerts_to_notify)}"



@shared_task
def send_alert_notifications(alert_ids):
    """
    Tarea programada para enviar notificaciones a usuarios cuando una alerta vence
    y actualizar el estado de la alerta a `STATUS_EXPIRED_ID`.
    """
    alerts = Alert.objects.filter(id__in=alert_ids, status=STATUS_ACTIVE_ID)

    if not alerts.exists():
        return "No hay alertas para notificar"

    # Obtener usuarios de prueba para enviar notificaciones
    test_users = list(User.objects.filter(is_staff=True).values_list("email", flat=True))

    if not test_users:
        return "No hay usuarios de prueba para notificar"

    # Construir el cuerpo del email
    email_subject = "Productos por vencer"
    email_body = "Atención: Los siguientes productos están por caducar:\n\n"
    email_body += "\n".join(
        [f"- {alert.product.name} (Expira: {alert.activation_date.strftime('%d/%m/%Y')})" for alert in alerts]
    )
    email_body += "\n\n Por favor, revisa los productos antes de su expiración."

    # Enviar correo
    try:
        send_mail(
            subject=email_subject,
            message=email_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=test_users,
            fail_silently=False  # Para capturar errores correctamente
        )
    except Exception as e:
        return f"Error enviando notificaciones: {str(e)}"

    # Actualizar estado de las alertas a expiradas
    alerts.update(status=STATUS_EXPIRED_ID)

    return f"Notificaciones enviadas correctamente a {len(test_users)} usuarios y {alerts.count()} alertas actualizadas."

