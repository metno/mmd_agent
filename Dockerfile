FROM python:3.8

WORKDIR /mmd_agent

COPY requirements.txt .

RUN pip install -r requirements.txt

ADD config.yaml .

COPY ./mmd_agent ./mmd_agent


# Override workdirectory, expected to have persistent storage
VOLUME mmd_agent

CMD ["python","./mmd_agent/agent.py"]

