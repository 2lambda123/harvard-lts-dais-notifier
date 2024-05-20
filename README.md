# dais-notifier

A microservice that reads messages from a queue and sends out an email


## Local setup
    
1. Make a copy of the env-template.txt to .env and modify the user and password variables.

2. Start the container
    
```
docker-compose -f docker-compose-local.yml up -d --build --force-recreate
```

3. Local Healthcheck: http://localhost:10587/readiness

## Testing
Note, testing uses its own queues so they will not interfere with the queues used by the actual program.

1. Start the container up as described in the <b>Local Setup</b> instructions.

2. Exec into the container:

```
docker exec -it notifier bash
```

3. Run the tests

```
pytest
```

## Invoking the task manually

- Clone this repo from github 

- Create the .env from the env-template.txt and replace with proper values (use LPE Shared-DAIS for passwords)

- Start up docker  

`docker-compose -f docker-compose-local.yml up --build -d --force-recreate`

- Exec into the docker container

`docker exec -it notifier bash`

- Run invoke task python script

`python3 scripts/invoke-task.py`

- An email should be sent to dts@hu.onmicrosoft.com
