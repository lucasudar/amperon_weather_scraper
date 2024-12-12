# Amperon Data Engineering Take Home Assigment

Build a small system that scrapes the Tomorrow IO API <https://docs.tomorrow.io/reference/welcome> for forecasts and
recent weather history for a set of geographic locations. You can use the Free API plan. Limit the list of geolocations
at these 10 locations:

|   lat   |   lon    |
|:-------:|:--------:|
| 25.8600 | -97.4200 |
| 25.9000 | -97.5200 |
| 25.9000 | -97.4800 |
| 25.9000 | -97.4400 |
| 25.9000 | -97.4000 |
| 25.9200 | -97.3800 |
| 25.9400 | -97.5400 |
| 25.9400 | -97.5200 |
| 25.9400 | -97.4800 |
| 25.9400 | -97.4400 |

The forecasts should be scraped hourly for each location on the list, and they should be available to query in a SQL
database at the end.

Design the system to answer the following questions using SQL:

* What's the latest temperature for each geolocation? What's the latest wind speed?
* Show an hourly time series of temperature (or any other available weather variable) from a day ago to 5 days in the
  future for a selected location.

## Considerations

* The choice of technologies, libraries, frameworks, and SQL databases is up to you, and please document the rationale
  behind your choices in README.
* For this example, you don't need to use any cloud services. Every service should be defined as a docker container and
  be runnable locally (we've provided a baseline compose file, but you can change it to fit your needs).
* You should use Python as the primary language for the solution.
* When in doubt - document your uncertainty in the README, along with your choice, and move on.
* We would rather see the best practices in software and data engineering than a complicated or even complete solution.

## Result

* Submit a public GitHub repository with the working code, or submit a private repository with the following users added as contributors:
  * `jward-amp`
  * `kmamykin`
  * `mike-sanderson-amp`.
* The system must be started using a docker-compose file in that repo.
* There must be a Jupyter notebook to visualize the results. The visual design of the visualization is not important.
* Add a README file with any instructions on how to run the system and the reasoning for choosing any particular
  tech.

## Timing

There is no time limit on this assignment to respect existing work and personal commitments. Our expectation is
somewhere within a week to have something you'd be comfortable submitting to us.

## Running the baseline infrastructure

We have provided some baseline infrastructure to help you get started. You should feel free to change any part of the
setup if it helps you have a better solution.

Here are some commands to get started:

Build and start the containers

```shell
$ docker compose up --build
```

The postgres instance is available with the following settings:

```shell
PGHOST=localhost
PGPORT=5432
PGDATABASE=tomorrow
PGUSER=postgres
PGPASSWORD=postgres
```

You can place table definitions in [./scripts/init-db.sql](./scripts/init-db.sql). This script is executed when the
postgres container starts.

Navigate to [localhost:8888](http://localhost:8888) to access the jupyter notebook server.

Lastly, cleanup your system with

```shell
$ docker compose down --volumes
```

## Feedback request

Please provide any feedback you may have on this take home assignment as part of the final submission README. We are 
continually trying to improve both the experience of our candidates and the signal that we receive from this assignment.