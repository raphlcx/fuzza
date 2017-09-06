FROM python:alpine3.6

COPY . /app/
WORKDIR /app

RUN pip install -r requirements.txt
RUN python setup.py install

ENTRYPOINT ["fuzza"]
