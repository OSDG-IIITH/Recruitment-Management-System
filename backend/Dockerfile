# cache the dependencies
FROM python:3.12 AS python_cache
RUN apt-get update && apt-get install libsasl2-dev python3-dev libldap2-dev libssl-dev slapd -y

FROM python_cache AS dependencies
ENV VIRTUAL_ENV=/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
WORKDIR /cache/
COPY requirements.txt .
RUN python -m venv /venv
RUN pip install -r requirements.txt

# build and start
FROM python:3.12-slim AS build
EXPOSE 80
RUN apt-get update && apt-get install libldap-2.5.0 -y
WORKDIR /app
ENV VIRTUAL_ENV=/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
COPY --from=dependencies /venv /venv
COPY . .
ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]