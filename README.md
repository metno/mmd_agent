Tests can be run by:

```bash
python -m pytest -vv --cov=mmd_agent --cov-report=term --cov-report=xml

```

## Build
```
docker build -t mmd-agent

```
## Run
```
docker run -it --network="host" mmd-agent:latest /bin/bash
cd go-mms
./mms s --production-hub nats://localhost:4222 --cmd /app/mmd_agent/agent.py 
```