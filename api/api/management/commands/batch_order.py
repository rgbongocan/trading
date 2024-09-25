import logging

import pandas as pd
from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import transaction

from api.exceptions import BatchOrdersNotCommitted
from api.models import Order, Stock

EXPECTED_COLUMNS = {"username", "stock", "quantity"}


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        logging.info("Executing batch order")
        filepath = settings.BATCH_ORDER_PATH
        try:
            df_orders = pd.read_csv(filepath)
            df_orders.head()
            assert set(df_orders.columns) == EXPECTED_COLUMNS
            # all orders need to go through, or none at all
            with transaction.atomic():
                for idx, row in df_orders.iterrows():
                    user = User.objects.get(username=row["username"])
                    stock = Stock.objects.get(name=row["stock"])
                    order = Order(user=user, stock=stock, amount=row["quantity"])
                    # we opt for individual object creation instead
                    # of bulk_create to trigger validations
                    order.save()
                logging.info(f"{len(df_orders.index)} orders successfully executed")
                if not settings.BATCH_ORDER_COMMIT:
                    raise BatchOrdersNotCommitted()
        except FileNotFoundError:
            logging.error(f"{filepath} does not exist")
        except BatchOrdersNotCommitted:
            logging.error(
                "Batch orders are not set to be committed. Check django settings."
            )
        except Exception as e:
            logging.error("Exception encountered, rolling back any orders made")
            raise e
