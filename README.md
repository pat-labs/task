# Task Project

## Docker Commands

### Build the Application Image

To build the Docker image for the application using the multi-stage Dockerfile:

```sh
docker build -t task-app .
```

### Run the Application Container

To run the application container:

```sh
docker run --name task-app-container --network host task-app
```

*Note: `--network host` is used here to allow the container to easily access the PostgreSQL instance running on
localhost.*

### Run PostgreSQL Container

To create and run the PostgreSQL database container required for the application:

```sh
docker run --name postgres-task \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=task \
  -p 5432:5432 \
  -d postgres:latest
```

**Description of PostgreSQL Command Flags:**

* `--name postgres-task`: Assigns the name `postgres-task` to the container for easy reference.
* `-e POSTGRES_USER=postgres`: Sets the environment variable to create a default user named `postgres`.
* `-e POSTGRES_PASSWORD=postgres`: Sets the environment variable to set the password for the default user to `postgres`.
* `-e POSTGRES_DB=task`: Sets the environment variable to create a default database named `task` upon initialization.
* `-p 5432:5432`: Maps port 5432 of the container to port 5432 on the host machine, allowing external connections.
* `-d postgres:latest`: Runs the container in detached mode (in the background) using the latest official PostgreSQL
  image.
