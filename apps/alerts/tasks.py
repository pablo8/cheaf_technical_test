from datetime import date
from celery import chain

from celery import shared_task
from dateutil.relativedelta import relativedelta
from django.db.models import F, Case, When, IntegerField, Q, Count, Max
from django.db.models.functions import ExtractDay
from django.utils.timezone import now
from django.core.mail import send_mail
from django.conf import settings

from utils.constants import STATUS_ACTIVE_ID, STATUS_EXPIRED_ID

from apps.alerts.models import Alert
from apps.products.models import Product


@shared_task
def update_alerts(simulated_date=None):
    """
    Tarea programada para actualizar `days_to_activation` y `days_since_activation`
    en todas las alertas, sean activas o expiradas. Además, si `days_to_activation` llega a 0,
    marca la alerta como expirada y dispara la notificación.
    """
    today = simulated_date if simulated_date else now().date()

    # Filtramos todas las alertas con activación válida (activas o expiradas)
    alerts = Alert.objects.filter(activation_date__isnull=False)

    # Actualizamos los días basados en la fecha actual
    alerts.update(
        days_to_activation=Case(
            When(activation_date__gt=today, then=ExtractDay(F('activation_date') - today)),
            default=0,  # Si ya pasó la fecha de activación, el valor es 0
            output_field=IntegerField()
        ),
        days_since_activation=Case(
            When(activation_date__lte=today, then=ExtractDay(today - F('activation_date'))),
            default=0,
            output_field=IntegerField()
        ),
    )

    # Identificamos alertas activas que vencieron hoy
    alerts_to_expire = list(
        alerts.filter(status=STATUS_ACTIVE_ID, days_to_activation=0)
        .values_list('id', flat=True)
    )

    # Enviar notificaciones si hay alertas vencidas
    if alerts_to_expire:
        send_expiration_notifications.delay('alert', alerts_to_expire)

    return f"Actualizadas {alerts.count()} alertas. Alertas expiradas hoy: {len(alerts_to_expire)}"


@shared_task
def notify_products_before_expiration(simulated_date=None, *args, **kwargs):
    """
    Notifica cuando un producto tiene todas sus alertas expiradas y su fecha de expiración
    es al menos 4 días mayor o igual a la fecha actual.
    """
    today = simulated_date if simulated_date is not None else now().date()

    # Buscar productos con alertas expiradas
    products = Product.objects.annotate(
        total_alerts=Count('alerts'),
        expired_alerts=Count('alerts', filter=Q(alerts__status=STATUS_EXPIRED_ID)),
        last_expired_alert=Max('alerts__activation_date', filter=Q(alerts__status=STATUS_EXPIRED_ID))
        # Última alerta expirada
    ).filter(
        expired_alerts=F('total_alerts'),  # Ambas alertas están expiradas
        last_expired_alert__lt=today,  # La última alerta expirada debe haber pasado
        expiration_date__gt=today  # El producto aún no ha expirado (mayor a hoy)
    )

    # Extraemos los IDs de los productos a notificar
    product_ids = list(products.values_list("id", flat=True))

    # Llamamos a la función de notificación si hay productos que cumplen la condición
    if product_ids:
        send_expiration_notifications.delay("product", product_ids, today)

    return (f"Se notificaron {len(product_ids)} productos con expiración dentro de los proximos 4 días antes de su"
            f"vencimiento.")


@shared_task
def send_expiration_notifications(notification_type, object_ids, today=None):
    """
    Tarea programada para enviar notificaciones cuando:
    1. Alertas vencen (tipo `alert`)
    2. Productos tienen todas sus alertas expiradas y expiran pronto (tipo `product`)

    `notification_type`:
        - "alert": Notificar alertas que pasaron a estado `STATUS_EXPIRED_ID`
        - "product": Notificar productos que expiran en >= 4 días y tienen todas sus alertas expiradas
    """
    if notification_type == "alert":
        # Notificar alertas vencidas
        alerts = Alert.objects.filter(id__in=object_ids, status=STATUS_ACTIVE_ID)
        if not alerts.exists():
            return "No hay alertas para notificar"

        email_subject = "Alerta de Productos Vencidos"
        email_body = "Atención: Los siguientes productos están próximos a vencer:\n\n"
        email_body += "\n".join(
            [f"- {alert.product.name} (Vencimiento: {alert.activation_date.strftime('%d/%m/%Y')})" for alert in alerts]
        )
        email_body += "\n\n Por favor, controlá el inventario."

        # Actualizar estado de alertas a expiradas
        alerts.update(status=STATUS_EXPIRED_ID)

    elif notification_type == "product":

        # Notificar alertas vencidas
        products = Product.objects.filter(id__in=object_ids)

        if not products.exists():
            return "No hay productos para notificar"

        email_subject = "Recordatorio de Productos por Vencer"
        email_body = "Atención: Los siguientes productos están a muy poco dias próximos a vencer:\n\n"
        email_body += "\n".join(
            [f"- {product.name} (Expira en {(product.expiration_date.date() - today).days} días)" for product in products]
        )
        email_body += "\n\n Por favor, revisa los productos antes de su expiración."

    else:
        return "Tipo de notificación inválido. Debe ser 'alert' o 'product'."

    # Obtener usuarios de prueba
    test_users = ['testusernoti1@test.com', 'testusernoti2@test.com', 'testusernoti3@test.com', 'testusernoti4@test.com']
    if not test_users:
        return "No hay usuarios de prueba para notificar"

    # Enviar correo
    try:
        send_mail(
            subject=email_subject,
            message=email_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=test_users,
            fail_silently=False
        )
    except Exception as e:
        return f"Error enviando notificaciones: {str(e)}"

    return f"Notificaciones enviadas correctamente a {len(test_users)} usuarios sobre {notification_type}."


@shared_task
def simulate_notifications(start_date=None, days=7, step_minutes=1):
    """
    Simula la ejecución de Celery avanzando días rápidamente.

    start_date: Fecha inicial de simulación (por defecto, hoy)
    days: Número de días a simular
    step_minutes: Intervalo de ejecución (por defecto, cada 1 minuto)
    """

    start_date = date(2025, 2, 9)
    for i in range(days):
        simulated_date = start_date + relativedelta(days=i)
        print(f"🔄 Simulando día: {simulated_date}")

        # Ejecutar ambas tareas en secuencia con la fecha simulada
        chain(
            update_alerts.s(simulated_date),
            notify_products_before_expiration.si(simulated_date)
        ).apply_async(countdown=i * step_minutes * 60)  # Ejecuta cada X minutos

    print(f"✅ Simulación programada para {days} días en intervalos de {step_minutes} minutos.")
