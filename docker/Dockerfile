FROM python:3.9-slim

RUN echo "Asia/Manila" > /etc/timezone
    
RUN apt-get update
RUN rm -rf /var/lib/apt/lists/*

# set work directory
WORKDIR /home

COPY requirements.txt .
RUN pip install -r requirements.txt

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

EXPOSE 5000

CMD ["python"]