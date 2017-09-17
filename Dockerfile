FROM python:alpine3.6

WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY . /app/
RUN python setup.py install

ENTRYPOINT ["fuzza"]
