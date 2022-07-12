FROM python:3.9.7
WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
RUN pip install uvicorn[standard]
RUN pip install -r /app/requirements.txt

COPY . /app
EXPOSE 8080
CMD ["uvicorn", "api:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8080"]