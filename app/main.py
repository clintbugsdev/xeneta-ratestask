import datetime

from fastapi import FastAPI, Query
from sqlalchemy import text

from .db import database
from .utils import is_code, get_slugs

# FastAPI
app = FastAPI(title="Xeneta - Ratestask", author="Clinton Bugtong", email="clintbugs.dev@gmail.com")


# Date format for date from and date to query parameters
YYYY_MM_DD = r"^(\d{4})-(0[1-9]|1[0-2]|[1-9])-([1-9]|0[1-9]|[1-2]\d|3[0-1])$"


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/rates")
def get_rates(
    date_from: str = Query(regex=YYYY_MM_DD), 
    date_to: str = Query(regex=YYYY_MM_DD),
    origin: str = Query(),
    destination: str = Query()
):
    # Set default origin & destination parameters as slug
    where_origin = f"prices.orig_code = '{origin}'"
    where_destination = f"prices.destcode = '{destination}'"

    # Set origin parameter as region slugs
    if not is_code(origin):
        results = get_slugs(origin)
        orig_slugs = [f"'{s.slug}'" for s in results]
        where_origin = f"orig_ports.parent_slug = ANY(ARRAY[{', '.join(orig_slugs)}])"
        

    # Set destination parameter as region slugs
    if not is_code(destination):
        results = get_slugs(destination)
        dest_slugs = [f"'{s.slug}'" for s in results]
        where_destination = f"dest_ports.parent_slug = ANY(ARRAY[{', '.join(dest_slugs)}])"
        
    # SQL to get rates per day
    sql = text(
                "SELECT " 
                    "prices.day, "
                    "ROUND(AVG(prices.price), 0) as average_price, " # Rounded value, based on the given example result
                    "COUNT(prices.price) "
                "FROM "
                    "prices "
                "LEFT JOIN "
                    "ports AS orig_ports ON orig_ports.code = prices.orig_code "
                "LEFT JOIN "
                    "ports AS dest_ports ON dest_ports.code = prices.dest_code "
                "WHERE "
                    f"{where_origin} AND "
                    f"{where_destination} AND "
                    "prices.day BETWEEN :date_from AND :date_to "
                "GROUP BY "
                    "prices.day "
                "ORDER BY "
                    "prices.day ASC"
            )
    # Execute query
    results = database.execute(
        sql, 
        date_from = date_from, 
        date_to = date_to
    ).fetchall()

    # Convert date from string to datetime object
    start_date = datetime.datetime.strptime(date_from, "%Y-%m-%d").date()
    
    # Convert date to string to datetime object
    end_date = datetime.datetime.strptime(date_to, "%Y-%m-%d").date()

    # Delta time
    delta = datetime.timedelta(days=1)

    # Getting the final output
    output = list()
    for i in range((end_date + (1 * delta) - start_date).days):
        day = start_date + (i * delta)
        price = None
        # Get average price from the original result
        for r in results:
            if day == r.day:
                price = None if r.count < 3 else r.average_price
        output.append({
            "day" : day, 
            "average_price" : price
        })
    return output
