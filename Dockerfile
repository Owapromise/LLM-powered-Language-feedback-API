FROM python:3.11-slim

WORKDIR /application

# Install build dependencies needed for packages such as PyYAML
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libyaml-dev && \
    rm -rf /var/lib/apt/lists/*

# Ensure pip/setuptools/wheel are up to date so prebuilt wheels are used when available
RUN pip install --upgrade pip setuptools wheel

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "application.main:app", "--host", "0.0.0.0", "--port", "8000"]
