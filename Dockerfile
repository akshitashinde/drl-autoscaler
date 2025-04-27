FROM python:3.10-slim

WORKDIR /app

COPY app.py /app/
COPY drl_scaler.zip /app/

RUN pip install flask stable-baselines3[extra] numpy

EXPOSE 5000

CMD ["python3", "app.py"]
