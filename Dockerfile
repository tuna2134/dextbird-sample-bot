FROM python:3-slim AS builder

WORKDIR /builder

RUN pip3 install poetry

COPY pyproject.toml .
COPY poetry.lock .
RUN poetry export -f requirements.txt --output requirements.txt

FROM python:3

WORKDIR /app

COPY --from=builder /builder/requirements.txt .
RUN pip3 install -r requirements.txt

COPY ./src/ .

CMD ["python3", "main.py"]
