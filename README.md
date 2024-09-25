To enable the scheduled execution of batch orders

```
docker compose cp <batch_orders.csv> cron:/tmp/orders.csv
```

The django management command `batch_order` being used to execute orders in bulk expects the csv file at the container's path `/tmp/orders.csv`

The csv file needs to have the following columns:


> `username` - the username placing an order
`stock` - the name of the stock
`quantity` - the number of stocks to buy/sell


Under `cron` service on `docker-compose.yaml`, set the environment variable `BATCH_ORDER_COMMIT` from `false` to `true`. It is set to `false` by default to avoid orders from being created indefinitely while the `cron` service is running.

You may have to `docker compose down cron` and `docker compose up -d cron` for the new environment variable to take effect.
