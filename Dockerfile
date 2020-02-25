FROM python:3.8-alpine

WORKDIR /usr/src/app

COPY requirements ./requirements
RUN pip install --no-cache-dir -r requirements/base.txt

COPY . .

CMD [ "python", "./choboi.py" ]

