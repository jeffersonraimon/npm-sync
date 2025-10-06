FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py api.py sync.py utils.py config.example.yml ./
# If you mount a config.yml at runtime, it will be used instead of the example.
CMD ["python", "main.py"]
