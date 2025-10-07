# Note on the code

Due to lack of time, a simple algorithm was used even though it does not work for some cases.
The biggest problem is that it will use as much as possible the cheapest source without surpassing the load, but will not look if the remaining load can be fulfilled by another plant without exceeding it.

The structure is kept pretty simple, waiting for more features to be implemented to have a clearer view on how the code should look like.


# Instructions to run the code

First build the docker image :

```
docker build -t powerplant-app .
```
You can then run a container :
```
docker run -it -p 8888:8888 powerplant-app
```
