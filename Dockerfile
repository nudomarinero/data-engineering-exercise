FROM python:3.9-slim-bullseye

# Required for the Python tests
RUN apt-get update && \
    apt-get install -y \
    curl \
    make \
    sudo \
    && rm -rf /var/lib/apt/lists/*

RUN useradd --create-home --home-dir /home/dataeng dataeng && \
    echo "dataeng ALL=(root) NOPASSWD:ALL" > /etc/sudoers.d/dataeng && \
    chmod 0440 /etc/sudoers.d/dataeng && \
    mkdir /home/dataeng/app && \
    chown dataeng:dataeng /home/dataeng/app

USER dataeng
WORKDIR /home/dataeng/app

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python - && \
    export PATH="/home/dataeng/.poetry/bin:${PATH}" && \
    poetry config virtualenvs.in-project true && \
    poetry config virtualenvs.create true
ENV PATH="/home/dataeng/.poetry/bin:${PATH}"

#COPY --chown=dataeng:dataeng . .
COPY --chown=tango:tango README.md process.bash ./
COPY --chown=tango:tango pyproject.toml poetry.lock* ./
COPY --chown=tango:tango src ./src

# Install the dependencies and the package
# RUN poetry install --no-root --no-dev
RUN poetry install
ENV PYTHONUNBUFFERED=0
ENV PATH="/home/dataeng/.local/bin:${PATH}"
