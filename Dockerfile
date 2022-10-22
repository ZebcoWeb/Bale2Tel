FROM python:3.9.13


RUN apt-get update && \
    apt-get upgrade -y

RUN python -m pip install --upgrade pip && \
    pip install -r req.txt

CMD ["python", "run.py"]