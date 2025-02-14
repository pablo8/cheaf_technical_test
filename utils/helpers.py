# Importación de librerias de python
from datetime import datetime

# Importación de terceros
import pytz
from dateutil.relativedelta import relativedelta


def convert_str_to_datetime(s):
    """
       Convierte una cadena de texto en un objeto datetime con zona horaria UTC.

       Parámetros:
       ----------
       s : str
           Fecha y hora en formato de cadena. Ejemplos:
           - "31/12/2020 12:40"  (Formato completo con año de 4 dígitos)
           - "31/12/20 12:40"    (Formato con año de 2 dígitos)

       Retorna:
       -------
       datetime | None
           - Un objeto datetime en UTC si la conversión es exitosa.
           - None si el formato de la cadena no coincide con ninguno de los esperados.
       """
    date_formats = ["%d/%m/%Y %H:%M", "%d/%m/%y %H:%M"]
    for fmt in date_formats:
        try:
            # Convertir la cadena a datetime (naive) y agregar zona horaria UTC
            return datetime.strptime(s, fmt).astimezone(pytz.UTC)
        except ValueError:
            continue
    return None


def calculate_activation_dates(expiration_date):
    """
       Calcula las fechas de activación de alertas en base a la fecha de expiración.

       Parámetros:
       ----------
       expiration_date : datetime
           Fecha de expiración del producto.

       Retorna:
       -------
       tuple[datetime, datetime] | tuple[None, None]
           - Primera alerta: 10 días antes de la expiración.
           - Segunda alerta: 5 días antes de la expiración.
           - Si ocurre un error, retorna (None, None).
       """
    try:
        return expiration_date - relativedelta(days=10), expiration_date - relativedelta(days=5)
    except Exception as e:
        print(f"Error en calculate_activation_dates: {e}")
        return None, None


def output_date_format(_datetime):
    """
        Convierte un objeto datetime a formato de cadena 'dd/mm/yyyy HH:MM'.

        Parámetros:
        ----------
        _datetime : datetime
            Objeto datetime que se desea formatear.

        Retorna:
        -------
        str | None
            - Fecha formateada como 'dd/mm/yyyy HH:MM'.
            - Retorna None si hay un error en el formato.
        """
    try:
        return datetime.strftime(_datetime, '%d/%m/%Y %H:%M')
    except Exception as e:
        print(f"Error en output_date_format: {e}")
        return None


def get_start_end_dates(range_dates):
    """
       Convierte una cadena con dos fechas separadas por coma en objetos datetime.date.

       Parámetros:
       ----------
       range_dates : str
           Cadena con dos fechas separadas por una coma, en formato 'YYYY-MM-DD,YYYY-MM-DD'.

       Retorna:
       -------
       tuple[date, date] | tuple[None, None]
           - La primera fecha como fecha de inicio.
           - La segunda fecha como fecha de fin.
           - Retorna (None, None) si el formato es inválido.
       """
    try:
        date_list = range_dates.split(',')
        date_start = datetime.strptime(date_list[0], "%Y-%m-%d").date()
        date_end = datetime.strptime(date_list[1], "%Y-%m-%d").date()
        return date_start, date_end
    except (ValueError, IndexError) as e:
        print(f"Error en get_start_end_dates: {e}")
        return None, None



