# dapr speed-testing

### Testing different methods of invocating dapr to measure speed

## How to run
Make sure you have the dapr/dapr cli installed, and run:
```shell
dapr run --app-id helloapp --app-port 9000 --dapr-http-port 3500 --dapr-grpc-port 3501
```

Then, build and run the python app. 
Notice that it's running with constrained memory and cpu 
to simulate a lightweight microservice without 
unlimited resources

```shell
docker build -t speedtest . &&\
docker run --network host --memory 50m --cpus "0.1" -e LOG_LEVEL=DEBUG speedtest
```

Now you can invoke the various methods. 
Each will cause 500 service invocation requests to go via dapr and hit 
another endpoint on the app.


## My results:
```shell 
# Native dapr http native client using async
curl http://localhost:9000/1
{"time_taken":16.0988712310791}

# Non-async dapr native http client
# This test varied a lot when re-running it, between 12 and 22 seconds
http://localhost:9000/2
{"time_taken":12.778820991516113}

# regular requests.get
curl http://localhost:9000/3
{"time_taken":16.49533247947693}

# regular requests session
curl http://localhost:9000/4
{"time_taken":13.089093208312988}

# httpx async get. By far the slowest in the test
curl http://localhost:9000/5
{"time_taken":90.34034895896912}

# httpx async with a single client instance
curl http://localhost:9000/6
{"time_taken":13.15303659439087}

# Dapr's native grpc client, using a non-async method
curl http://localhost:9000/7
{"time_taken":5.243842840194702}

# Dapr's native grpc-client, wrapped in asyncify so it can be used in async methods
curl http://localhost:9000/8
{"time_taken":9.169137716293335}
```

Some conclusions:
- GRPC is by far the faster. For async-only apps, wrapping the grpc call in async is still faster than other options
- httpx is extremely slow when using an async context manager per invocation
- otherwise the results are comparable