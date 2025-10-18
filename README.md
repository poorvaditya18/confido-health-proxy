# CONFIDO-EHR-PROXY

description: responsible to connect with various data source with plug-in/plug-out pattern (currently supports: EPIC)

NOTE: please refer `design-doc.txt`

# Setup ENVs:

EPIC_BASE_URL=
AUTH_SERVICE_URL=
REDIS_PORT=
REDIS_HOST=
REDIS_PASSWORD=
DB_USER=
DB_PASSWORD=
DB_PORT=
DB_NAME=

# dependency:

- `CONFIDO-EHR-PROXY` depends on `CONFIDO-AUTH` for token generation.

# for setting up REDIS and Postgres -

pull the latest docker image of Redis and Postgres (v14) with correctly mention PORT number same as in envs.

# start server:

change directory to src : `cd src/`
start the server using `uvicorn main:app --reload --host 0.0.0.0 --port 8001`

# API :

- Get: /appointments :
  `curl --location 'localhost:8001/api/v1/appointments' --header`

- Get: /patients :
  `curl --location 'localhost:8001/api/v1/appointments' --header`

- Post: /ingest :
  `curl --location --request POST 'localhost:8001/api/v1/ingest' --header 'x-source-type: EPIC'`
