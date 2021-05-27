import boto3
import functools
import os
import requests
import json
import time

# importing module
import logging

# Creating an object
logging.getLogger().setLevel(logging.INFO)

aws_access_key_id = os.environ["aws_access_key_id"]
aws_secret_access_key = os.environ["aws_secret_access_key"]
aws_region_name = os.environ["aws_region_name"]
webhook_url = os.environ["webhook_url"]
periodic_time_interval = int(os.environ["periodic_time_interval"]) * 60


def error_handler(func=None, *, default=None):
    def inner_function_wrapper(func):
        @functools.wraps(func)
        def inner_function(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as ex:
                logging.error(f"{func.__name__}: {ex}")
                return default

        return inner_function

    if func:
        return inner_function_wrapper(func)
    else:
        return inner_function_wrapper


def get_ec2_client(region):
    return boto3.client(
        "ec2",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region,
    )


def get_ec2_resource(region):
    return boto3.resource(
        "ec2",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region,
    )


@error_handler(default=[])
def get_region_names():
    ec2 = get_ec2_client(aws_region_name)
    regions = ec2.describe_regions()
    return map(lambda r: r["RegionName"], regions["Regions"])


@error_handler
def get_ec2_instances():
    ec2_instances_dict = {}
    for region_name in get_region_names():
        ec2 = get_ec2_resource(region_name)
        instances = ec2.instances.filter(
            Filters=[{"Name": "instance-state-name", "Values": ["running"]},]
        )
        ec2_instances_dict[region_name] = len(list(instances))
    return ec2_instances_dict


@error_handler
def call_webhook(url, payload):
    headers = {
        "content-type": "application/json",
        "cache-control": "no-cache",
        "postman-token": "d73b89a7-3ebe-79e0-0fe9-2bdfce38c7dc",
    }

    response = requests.request("POST", url, data=json.dumps(payload), headers=headers)

    if response.status_code == 200:
        logging.info("Success!")
    else:
        logging.error("Failure!")


while True:
    ec2_instances_dict = get_ec2_instances()
    if ec2_instances_dict:
        call_webhook(webhook_url, ec2_instances_dict)
    time.sleep(periodic_time_interval)
