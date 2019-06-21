from ticket_system.models import Reservation, States

"""
    Globbal function to update reservation states
"""


def update_reservation_states():
    for reservation in Reservation.objects.filter(state=States.RESERVED.value):
        reservation.update_reservation()
