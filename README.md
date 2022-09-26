# XENETA - Ratestask

An [HTTP-based API](#https://github.com/xeneta/ratestask) assignment, capable of handling the GET request. Stack is based on [FastAPI](#https://fastapi.tiangolo.com/) framework. Returns JSON format for list of the average prices for each day on a route between ort codes *origin* and *destination* and return an empty value (JSON null) for days on which there are less than 3 prices in total.

Both the *origin, destination* params accept either port codes or region slugs, making it possible to query for average prices per day between geographic groups of ports.

### Query Parameters:

* date_from
* date_to
* origin
* destination

### Implementation:

    curl "http://127.0.0.1/rates?date_from=2016-01-01&date_to=2016-01-10&origin=CNSGH&destination=north_europe_main"

    [
        {
            "day": "2016-01-01",
            "average_price": 1112
        },
        {
            "day": "2016-01-02",
            "average_price": 1112
        },
        {
            "day": "2016-01-03",
            "average_price": null
        },
        ...
    ]

# Prerequisites

[Docker](https://docs.docker.com/get-docker/ "Get Docker")

[Docker Compose](https://docs.docker.com/compose/install/ "Installation")

# Installation

Docker setup which will start a
PostgreSQL instance populated with the assignment data with running FastAPI app.

Build the image:

```bash
docker-compose build
```

Once the image is build, run the container:

```bash
docker-compose up -d
```

## Testing

Use `docker-compose exec` to run the test:

```bash
docker-compose exec web pytest .
```

# Contact

Clinton Bugtong - [@linkedin](https://linkedin.com/in/clintbugs/) - clintbugs.dev@gmail.com

Project Link: [https://github.com/github_username/repo_name](https://github.com/github_username/repo_name)
