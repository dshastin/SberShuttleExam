FROM redhat/ubi8-minimal:latest

WORKDIR /opt/app

RUN microdnf install shadow-utils  \
    && microdnf install findutils \
    && microdnf install procps \
    && microdnf install python3.11 python3.11-setuptools python3.11-devel binutils clang

RUN groupadd -r web && useradd -d /opt/app -r -g web web && chown web:web -R /opt/app

RUN python3 -m ensurepip --upgrade \
    && python3 -m venv venv

ENV PYTHONFAULTHANDLER=1\
    PYTHONBUFFERED=1 \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VIRTUALENVS_PATH=/opt/app/venv

COPY src/requirements.txt ./

RUN python3 -m pip install -r requirements.txt

COPY ./src/ entrypoint.sh ./

USER web

ENTRYPOINT ["/bin/sh", "entrypoint.sh"]
