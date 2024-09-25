### About

This is a REST API written with Django that implements _simplified_ stock trading. The following holds true in the scope of this project:

- A user can buy an unlimited quantity of stock
- A user can only sell stock that they have
- A negative order quantity means the user intends to sell
- Orders are executed immediately. There are no concepts of limit and stop orders.

### Getting started

```
docker compose up -d
```
to get your environment up and running. There are three running services:

> `api` - Django web server
`db` - Postgres database
`cron` - Periodically consumes a batch order file (see below)

```
docker compose exec -it api ./manage.py migrate`
```
to initialize your database

```
docker compose exec -it api python manage.py createsuperuser --username su --email su@gmail.com
```
to create an admin user. You can modify the credentials but make sure to edit the corresponding values in `notsosecrets.env`

With this, you can create user/s by logging in as an admin on http://localhost:8000/admin/auth/user/

Go back to http://localhost:8000 to login as your created user and use the endpoints.

_Hint: You can only create new stocks as an admin user._

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

### Testing

To run all tests
```
docker compose exec -it api ./manage.py test
```

Test are split simply into two files: for models and for views
