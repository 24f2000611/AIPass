ARG PYTHON_VERSION=3.12
FROM python:${PYTHON_VERSION}-slim

LABEL maintainer="AIPass <aipass.system@gmail.com>"
LABEL description="Reproducible test environment for Trinity Pattern"

WORKDIR /app
COPY pyproject.toml setup.py ./
RUN pip install --no-cache-dir -e . && pip install --no-cache-dir pytest ruff coverage
COPY . .
CMD ["pytest", "-v", "--tb=short"]
