# Docker Data Pump service.
A python service to push the count of running EC2 instances in a list of regions periodically to a web hook in a Docker container.

**This application is written with Python 3.6.**

## Set up environment variables

Create a file named '.env' on the root folder with following Key-Value pairs:

```sh
aws_access_key_id=XXXXXXX
aws_secret_access_key=XXXXXXX
aws_region_name=XXXXXX
webhook_url=https://webhook.site/xyz
periodic_time_interval=30 (time in seconds)
```

## Build and Run

It is best to first install Docker on the system.
Then run the following commands:

```sh
# To build docker image.
docker build -t data_pump_service .

# To run docker container.
docker run --env-file=.env -t data_pump_service

```
