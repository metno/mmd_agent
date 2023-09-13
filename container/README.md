## Build
```
docker build -t mmd-agent

```
## Run
```
docker run mmd-agent:latest 

s --queue-name product-events --production-hub < production hub url > --cmd < path/to/python/script > --cred-file < path/to/cred/file >
```