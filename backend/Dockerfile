FROM python:3.12-slim AS builder

WORKDIR /app

COPY pyproject.toml requirements.txt ./
RUN pip wheel --no-cache-dir --no-deps --wheel-dir wheels -r requirements.txt

COPY src src
RUN pip wheel --no-cache-dir --no-deps --wheel-dir wheels .


FROM python:3.12-slim AS runner_stage

COPY --from=builder /app/wheels /wheels
RUN pip install --no-cache /wheels/* && rm -rf /wheels

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

COPY healthcheck-script.sh /usr/local/bin/

RUN chmod +x /usr/local/bin/healthcheck-script.sh

HEALTHCHECK CMD /usr/local/bin/healthcheck-script.sh

CMD ["uvicorn", "mysite.main:app", "--host", "0.0.0.0", "--port", "80"]