FROM python:3.9.13


ENV BALE_TOKEN = unknown
ENV TELEGRAM_TOKEN = unknown

RUN apt-get update && \
    apt-get upgrade -y

WORKDIR /bale2tel

COPY . .

RUN python -m pip install --upgrade pip && \
    pip install -r requirements.txt

CMD ["python", "run.py"]