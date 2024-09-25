### Batch ordering

For batch ordering, the following columns are expected in the csv file

> `stock` - valid name of stock
`quantity` - number of stocks to buy/sell
`username` - (for cron only) valid username placing an order

To avoid unwanted repetition, the batch orders are executed all or nothing. Upon encountering an error, it is up to the user to double-check the validity of column names and row values.

#### Through file upload

The `/batch-order/` endpoint takes a csv file upload and orders are placed in behalf of the user logged in.

#### Through a scheduled job (cron)

The django management command `batch_order` is invoked periodically to execute orders in bulk, which can be placed in behalf of more than one user.

This cron consumes `/tmp/orders.csv`. To ensure the file exists in the container

```
docker compose cp <filename>.csv cron:/tmp/orders.csv
```

By default, orders placed by the cron are not committed to avoid orders from being created indefinitely. To enable commits, explicitly set `BATCH_ORDER_COMMIT` from `false` to
```
cron:
    ...
    environment:
      - BATCH_ORDER_COMMIT=true
```

You may have to `docker compose down cron && docker compose up -d cron` and for the new environment variable to take effect.
