FROM python:3.8

WORKDIR /app

COPY *requirements.txt .

RUN pip install -r requirements.txt -r test_requirements.txt

COPY . .

CMD [ "pytest" ]