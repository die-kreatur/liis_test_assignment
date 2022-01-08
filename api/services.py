from django.db.models import Q
from .models import Booking


def bookings_for_time_period(date_from, date_to):
    """Функция возвращает существующие в заданный промежуток времени бронирования.
    Возможно 4 варианта:
    - дата начала бронирования попадает в выбранный промежуток времени;
    - дата окончания бронирования попадает в выбранный промежуток времени;
    - выбранный промежуток времени содержит обе даты;
    - период бронирования содержит выбранный промежуток времени.
    В соответсвии с этими условиями составлен запрос query для поиска по БД"""

    query = (
                Q(date_from__range=[date_from, date_to]) \
                | Q(date_to__range=[date_from, date_to])
            ) | (
                Q(date_from__lte=date_from) \
                & Q(date_to__gte=date_to)
            )

    return Booking.objects.filter(query)
