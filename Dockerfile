FROM python:3.11
ENV PYTHONBUFFERED 1

WORKDIR /usr/src/app
RUN mkdir -p /usr/src/app

COPY requirements.txt .
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

COPY . /usr/src/app

CMD ["python", "src/main.py"]
