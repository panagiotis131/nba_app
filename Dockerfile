FROM python

WORKDIR /code

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY nba.py .

CMD ["python", "./nba.py"]
