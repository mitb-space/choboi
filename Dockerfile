FROM python:3.8-alpine

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

WORKDIR /usr/src/app

COPY requirements ./requirements
RUN pip install --no-cache-dir -r requirements/base.txt

COPY . .

CMD [ "python", "./choboi.py" ]

