FROM python:3.12-slim AS assets
WORKDIR /app
# JavaScript is buildless; syntax is checked by scripts/build.py before packaging.
COPY web /app/dist

FROM python:3.12-slim
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 RELAYFY_ENV=production RELAYFY_DB_PATH=/data/relayfy.sqlite
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && useradd --uid 10001 --create-home relayfy && mkdir /data && chown relayfy:relayfy /data
COPY service ./service
COPY --from=assets /app/dist ./dist
COPY gunicorn.conf.py ./
USER relayfy
VOLUME ["/data"]
EXPOSE 8000
CMD ["gunicorn", "--config", "gunicorn.conf.py", "service.wsgi:application"]
