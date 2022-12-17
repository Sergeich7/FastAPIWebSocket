FROM python:3.10-alpine
LABEL maintainer="Vitaly Belashov pl3@yandex.ru"
WORKDIR /app
RUN pip install --upgrade pip
COPY . /app/
RUN pip install -r requirements.txt
EXPOSE 8000
ENV PYTHONUNBUFFERED 1
CMD ["uvicorn", "run:app", "--host", "0.0.0.0"]
