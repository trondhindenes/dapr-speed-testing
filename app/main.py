import time

import httpx
import requests
from dapr.clients import DaprClient, DaprGrpcClient
from fastapi import FastAPI
from loguru import logger
from asyncer import asyncify

from app.httpx_wrapper import http_get

app_id = "helloapp"
total_loops = 500

app = FastAPI(
    title="hello",
    version="0.0.1"
)

d = DaprClient(address="127.0.0:3500")
d_grpc = DaprGrpcClient(address="127.0.0.0:3501")


def do_the_stuff():
    return True


@app.get("/pling")
async def get_pling():
    return {"status": "ok"}


@app.get("/1")
async def send_messages_to_dapr_async():
    start = time.time()
    counter = 0
    while counter < total_loops:
        logger.debug(f"invoking d.invoke_method_async for counter {counter}")
        result = await d.invoke_method_async(
            app_id=app_id,
            method_name="pling",
            data="what",
            http_verb="GET"
        )
        counter += 1
    end = time.time()
    time_taken = (end - start)
    logger.debug(f"time taken: {time_taken}")
    return {"time_taken": time_taken}


@app.get("/2")
def send_messages_to_dapr():
    start = time.time()
    counter = 0
    while counter < total_loops:
        logger.debug(f"invoking d.invoke_method for counter {counter}")
        result = d.invoke_method(
            app_id=app_id,
            method_name="pling",
            data="what",
            http_verb="GET"
        )
        counter += 1
    end = time.time()
    time_taken = (end - start)
    logger.debug(f"time taken: {time_taken}")
    return {"time_taken": time_taken}


@app.get("/3")
def send_messages_to_dapr_with_requests():
    start = time.time()
    counter = 0
    while counter < total_loops:
        logger.debug(f"invoking requests.get for counter {counter}")
        result = requests.get(f"http://localhost:3500/v1.0/invoke/{app_id}/method/pling/what")
        counter += 1
    end = time.time()
    time_taken = (end - start)
    logger.debug(f"time taken: {time_taken}")
    return {"time_taken": time_taken}


@app.get("/4")
def send_messages_to_dapr_with_requests_session():
    start = time.time()
    counter = 0
    session = requests.session()
    while counter < total_loops:
        logger.debug(f"invoking session.get for counter {counter}")
        result = session.get(f"http://localhost:3500/v1.0/invoke/{app_id}/method/pling/what")
        counter += 1
    end = time.time()
    time_taken = (end - start)
    logger.debug(f"time taken: {time_taken}")
    return {"time_taken": time_taken}


@app.get("/5")
async def send_messages_to_dapr_with_httpx():
    start = time.time()
    counter = 0
    session = requests.session()
    while counter < total_loops:
        logger.debug(f"invoking client.get for counter {counter}")
        async with httpx.AsyncClient() as client:
            r = await client.get(f"http://localhost:3500/v1.0/invoke/{app_id}/method/pling/what")
        counter += 1
    end = time.time()
    time_taken = (end - start)
    logger.debug(f"time taken: {time_taken}")
    return {"time_taken": time_taken}


@app.get("/6")
async def send_messages_to_dapr_with_httpx_session():
    start = time.time()
    counter = 0
    session = requests.session()
    while counter < total_loops:
        logger.debug(f"invoking http_get for counter {counter}")
        r = await http_get(f"http://localhost:3500/v1.0/invoke/{app_id}/method/pling/what")
        counter += 1
    end = time.time()
    time_taken = (end - start)
    logger.debug(f"time taken: {time_taken}")
    return {"time_taken": time_taken}


@app.get("/7")
def send_messages_to_dapr_grpc():
    start = time.time()
    counter = 0
    while counter < total_loops:
        logger.debug(f"invoking d_grpc.invoke_method for counter {counter}")
        result = d_grpc.invoke_method(
            app_id=app_id,
            method_name="pling",
            data="what",
            http_verb="GET"
        )
        counter += 1
    end = time.time()
    time_taken = (end - start)
    logger.debug(f"time taken: {time_taken}")
    return {"time_taken": time_taken}


@app.get("/8")
async def send_messages_to_dapr_grpc_async_wrapped():
    start = time.time()
    counter = 0
    while counter < total_loops:
        logger.debug(f"invoking d_grpc.invoke_method (async-wrapped) for counter {counter}")
        result = await asyncify(d_grpc.invoke_method)(
            app_id=app_id,
            method_name="pling",
            data="what",
            http_verb="GET"
        )
        counter += 1
    end = time.time()
    time_taken = (end - start)
    logger.debug(f"time taken: {time_taken}")
    return {"time_taken": time_taken}
