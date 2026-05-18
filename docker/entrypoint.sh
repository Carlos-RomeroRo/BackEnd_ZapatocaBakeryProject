#!/bin/sh
set -e

echo "Esperando PostgreSQL..."
python - <<'PY'
import os
import sys
import time

from sqlalchemy import create_engine, text

url = os.environ.get("DATABASE_URL")
if not url:
    print("DATABASE_URL no definida", file=sys.stderr)
    sys.exit(1)

engine = create_engine(url)
for attempt in range(60):
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("PostgreSQL listo.")
        break
    except Exception:
        if attempt == 59:
            print("Timeout: no se pudo conectar a PostgreSQL.", file=sys.stderr)
            sys.exit(1)
        time.sleep(1)
PY

exec uvicorn app.main:app --host 0.0.0.0 --port "${PORT:-8000}"
