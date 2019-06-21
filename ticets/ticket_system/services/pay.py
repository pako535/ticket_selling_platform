from collections import namedtuple
from ticket_system.models import Reservation, States


class CardError(Exception):
    pass


class PaymentError(Exception):
    pass


class CurrencyError(Exception):
    pass


class ReservationError(Exception):
    pass


PaymentResult = namedtuple('PaymentResult', ('amount', 'currency'))


"""
    PaymentServices = PaymentGateway
    
"""


class PaymentServices:
    supported_currencies = ('EUR',)
    reservation = None

    def get_reservation(self, id):
        self.reservation = Reservation.objects.filter(id=id).first()
        if not self.reservation:
            raise ReservationError("Bad id reservation given")

    def check_correctness_amount(self, amount):
        if float(amount) == self.reservation.ticket.price:
            return True
        return False

    def charge(self, amount, token, currency='EUR'):
        if token == 'card_error':
            raise CardError("Your card has been declined")
        elif token == 'payment_error':
            raise PaymentError("Something went wrong with your transaction")
        elif currency not in self.supported_currencies:
            raise CurrencyError(f"Currency {currency} not supported")
        elif self.reservation.state == States.CANCELED.value \
                or self.reservation.state == States.PAID.value:
            return "The reservation has expired or the ticket has already been paid"
        else:
            if self.check_correctness_amount(amount):
                self.reservation.state = States.PAID.value
                self.reservation.save()
                return PaymentResult(amount, currency)
            else:
                return "Invalid amount"
