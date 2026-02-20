FROM python:3.12-bookworm
LABEL maintainer="z3pp1x"

ENV PYTHONUNBUFFERED=1
ENV PATH="/py/bin:$PATH"

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./backend /backend
WORKDIR /backend
EXPOSE 8000

ARG DEV=false
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apt-get update && \
    apt-get install -y --no-install-recommends postgresql-client && \
    apt-get install -y --no-install-recommends \
        build-essential libpq-dev && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ "$DEV" = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    apt-get remove --purge -y build-essential libpq-dev &&\
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    rm -rf /tmp && \
    adduser \
        --disabled-password \
        --no-create-home \
        z3pp1x && \
    chown -R z3pp1x /backend

USER z3pp1x

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]