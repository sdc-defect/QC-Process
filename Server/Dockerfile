FROM python:3.7.13-slim-bullseye

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && apt-get upgrade -y
RUN apt-get install libgl1-mesa-glx libglib2.0-0 -y

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY app .
EXPOSE 8080
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]