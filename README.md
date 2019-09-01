## Application architecture

The application is composed of 4 components, API gateway, API products and API categories are the backend components and the frontend component is the Angular app.

![Application architecture](https://i.imgur.com/zuEq3v6.png)

## Microservices architecture
- The backend is composed of 3 components:
  - API gateway: The entry point of all communications with the backend services.
  - API products: The service that manages products.
  - API categories: The service that manages categories.

- The used pattern is `database per service`([https://microservices.io/patterns/data/database-per-service.html](https://microservices.io/patterns/data/database-per-service.html)). The API products and the API categories, each one has its own database.

- The API gateway is the single entry point for all clients. Also, it implements the `API composition`([https://microservices.io/patterns/data/api-composition.html](https://microservices.io/patterns/data/api-composition.html)) to query data from products and categories APIs.

- The communication between the API gateway and the services are based on an authenticated REST API.

## API authentication

- The communication between the web application(Angular) and the API gateway and the communication between the API gateway and the services are based on an authenticated REST API.
- The authentication is based on a key which should be passed in the header of the HTTP request:
```sh
X-API-Key: <api_key>
```
- The API key is shared between all the components:
  - The key is stored in these files
```sh
- backend/.envs/key.env
- frontend/src/environments/environment.ts
- frontend/src/environments/environment.prod.ts
```

## Development and testing environments

  - Ubuntu 17.04
  - Docker Compose (1.24.1, build 4667896b)
  - Docker  (1.13.1, build 092cba3)
  - MongoDB docker image (mongo)
  - Python docker image (python:3.7-alpine)
  - Node docker image (node:10-alpine)
  - Angular 8


## How to run the application

Make sure that docker-compose and docker are installed on your system. Clone the repository and then change directory to the cloned repository.

- Start the API gateway, products and categories:

```sh
docker-compose up gateway products categories
```

```sh
api-gateway        |  * Serving Flask app "api.py"
api-gateway        |  * Environment: production
api-gateway        |    WARNING: This is a development server. Do not use it in a production deployment.
api-gateway        |    Use a production WSGI server instead.
api-gateway        |  * Debug mode: off
api-gateway        |  * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
api-categories     |  * Serving Flask app "api.py"
api-categories     |  * Environment: production
api-categories     |    WARNING: This is a development server. Do not use it in a production deployment.
api-categories     |    Use a production WSGI server instead.
api-categories     |  * Debug mode: off
api-categories     |  * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
api-products       |  * Serving Flask app "api.py"
api-products       |  * Environment: production
api-products       |    WARNING: This is a development server. Do not use it in a production deployment.
api-products       |    Use a production WSGI server instead.
api-products       |  * Debug mode: off
api-products       |  * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
```

- Run the Angular web application:

```sh
docker-compose up webapp
```

You can access the web application from your browser by this URL [http://localhost:8000](http://localhost:8000).

## How to run the tests

- API gateway tests:
  - The tests are located in `backend/gateway/tests/`

```sh
docker-compose up gateway-test
```

```sh
api-gateway-test   | .........................
api-gateway-test   | ----------------------------------------------------------------------
api-gateway-test   | Ran 25 tests in 0.322s
api-gateway-test   |
api-gateway-test   | OK
api-gateway-test   | Name                Stmts   Miss  Cover   Missing
api-gateway-test   | -------------------------------------------------
api-gateway-test   | __init__.py             0      0   100%
api-gateway-test   | api.py                125      2    98%   78, 147
api-gateway-test   | tests/__init__.py       0      0   100%
api-gateway-test   | tests/test_api.py     142      0   100%
api-gateway-test   | -------------------------------------------------
api-gateway-test   | TOTAL                 267      2    99%
api-gateway-test exited with code 0
```

- API products tests:
  - The tests are located in `backend/products/tests/`

```sh
docker-compose up products-test
```

```sh
api-products-test  | .......................
api-products-test  | ----------------------------------------------------------------------
api-products-test  | Ran 23 tests in 0.348s
api-products-test  |
api-products-test  | OK
api-products-test  | Name                   Stmts   Miss  Cover   Missing
api-products-test  | ----------------------------------------------------
api-products-test  | __init__.py                0      0   100%
api-products-test  | api.py                    78      2    97%   63, 85
api-products-test  | models.py                 12      0   100%
api-products-test  | tests/__init__.py          0      0   100%
api-products-test  | tests/test_api.py        115      0   100%
api-products-test  | tests/test_models.py      30      0   100%
api-products-test  | ----------------------------------------------------
api-products-test  | TOTAL                    235      2    99%
api-products-test exited with code 0
```

- API categories tests:
  - The tests are located in `backend/categories/tests/`

```sh
docker-compose up categories-test
```

```sh
api-categories-test | ...............
api-categories-test | ----------------------------------------------------------------------
api-categories-test | Ran 15 tests in 0.251s
api-categories-test |
api-categories-test | OK
api-categories-test | Name                   Stmts   Miss  Cover   Missing
api-categories-test | ----------------------------------------------------
api-categories-test | __init__.py                0      0   100%
api-categories-test | api.py                    63      0   100%
api-categories-test | models.py                 10      0   100%
api-categories-test | tests/__init__.py          0      0   100%
api-categories-test | tests/test_api.py         71      0   100%
api-categories-test | tests/test_models.py      19      0   100%
api-categories-test | ----------------------------------------------------
api-categories-test | TOTAL                    163      0   100%
api-categories-test exited with code 0
```

- Angular app tests:
  - The tests are located in `frontend/src/app/`

```sh
docker-compose up webapp-test
```

```sh
webapp-test        | TOTAL: 38 SUCCESS
webapp-test        | TOTAL: 38 SUCCESS
webapp-test        | TOTAL: 38 SUCCESS
webapp-test        |
webapp-test        | =============================== Coverage summary ===============================
webapp-test        | Statements   : 92.66% ( 101/109 )
webapp-test        | Branches     : 100% ( 0/0 )
webapp-test        | Functions    : 86.21% ( 50/58 )
webapp-test        | Lines        : 93.55% ( 87/93 )
webapp-test        | ================================================================================
webapp-test exited with code 0
```

## TODO
- Improve the API authentication. Use a better solution like JWT based authentication.
- Add and display error messages in the Angular web application. So, the user will see the error message when something went wrong.
