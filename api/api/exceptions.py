from django.core.exceptions import ValidationError
from django.db.transaction import TransactionManagementError


class NotEnoughShares(ValidationError):
    pass


class BatchOrdersNotCommitted(TransactionManagementError):
    pass
