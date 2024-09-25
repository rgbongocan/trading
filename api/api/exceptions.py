from django.core.exceptions import ValidationError


class NotEnoughShares(ValidationError):
    pass
