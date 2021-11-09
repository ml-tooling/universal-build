FROM python:3.8-alpine

# Install python template lib from distribution
# hadolint ignore=DL3010
COPY ./resources/python-lib.tar.gz /python-lib.tar.gz
# hadolint ignore=DL3013
RUN pip install --no-cache-dir "/python-lib.tar.gz"

EXPOSE 8080

ENTRYPOINT ["python-lib", "start-api-server","--port","8080"]
