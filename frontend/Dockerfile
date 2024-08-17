FROM python:3.11-slim

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR='/var/cache/pypoetry' \
    APP_PORT=8501


RUN apt-get update && apt-get install -y curl    
RUN apt-get clean autoclean && apt-get autoremove --yes && rm -rf /var/lib/{apt,dpkg,cache,log}
RUN curl -sSL https://install.python-poetry.org | python3 -

COPY poetry.lock pyproject.toml /
RUN /root/.local/bin/poetry install 

COPY ./app /app
WORKDIR /app

EXPOSE ${APP_PORT}

HEALTHCHECK CMD curl --fail http://localhost:${APP_PORT}/_stcore/health

ENTRYPOINT ["streamlit", "run", "0_Start_Here.py", "--server.port" , ${APP_PORT} , "--server.address=0.0.0.0"]
