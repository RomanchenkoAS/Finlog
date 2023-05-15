FROM python:3.10

WORKDIR /app

COPY . .

RUN apt-get update
RUN apt-get install -y python3-dev
RUN apt-get clean

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

EXPOSE 8000

CMD ["python3", "manage.py", "runserver", "8000"]