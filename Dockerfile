# dockerfile
FROM python:3.10-slim

COPY . /aton_test_task
COPY requirements.txt /aton_test_task/requirements.txt

RUN pip install -r /aton_test_task/requirements.txt

WORKDIR /aton_test_task

EXPOSE 5000

CMD ["python", "-u", "main.py"]
