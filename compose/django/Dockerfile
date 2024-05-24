FROM docker.io/python:3.12.3-slim-bookworm as python

# Python build stage
FROM python as python-build-stage

# Install build dependencies
RUN apt-get update && apt-get install --no-install-recommends -y \
    # dependencies for building Python packages
    build-essential \
    # psycopg2 dependencies
    libpq-dev

# Create Python wheels
COPY ./requirements.txt .
RUN pip wheel --wheel-dir /usr/src/app/wheels -r requirements.txt

# Python run stage
FROM python as python-run-stage

ARG APP_HOME=/app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR ${APP_HOME}

# Install devcontainer dependencies and utils
RUN apt-get update && apt-get install --no-install-recommends -y \
    sudo git bash-completion nano ssh

# Create devcontainer user and add it to sudoers
RUN groupadd --gid 1000 dev-user \
    && useradd --uid 1000 --gid dev-user --shell /bin/bash --create-home dev-user \
    && echo dev-user ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/dev-user \
    && chmod 0440 /etc/sudoers.d/dev-user

RUN apt-get update && apt-get install --no-install-recommends -y \
    # psycopg dependencies
    libpq-dev \
    # cleaning up unused files
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*

# All absolute dir copies ignore workdir instruction. All relative dir copies are wrt to the workdir instruction
# copy python dependency wheels from python-build-stage
COPY --from=python-build-stage /usr/src/app/wheels  /wheels/

# use wheels to install python dependencies
RUN pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* \
    && rm -rf /wheels/

COPY ./compose/django/entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r$//g' /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY ./compose/django/start.sh /start.sh
RUN sed -i 's/\r$//g' /start.sh
RUN chmod +x /start.sh

COPY . ${APP_HOME}

ENTRYPOINT ["/entrypoint.sh"]
