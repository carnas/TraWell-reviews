FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /reviews
COPY requirements.txt /reviews/
RUN pip install -r requirements.txt
COPY . ./reviews