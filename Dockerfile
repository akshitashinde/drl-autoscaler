FROM python:3.10-slim

WORKDIR /app

# Copy app and model zip only
COPY app.py /app/
COPY drl_scaler.zip /app/

# Install dependencies
RUN pip install --no-cache-dir flask stable-baselines3[extra] numpy

EXPOSE 5000

CMD ["python3", "app.py"]
