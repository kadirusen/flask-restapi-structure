FROM python:3.8.2
WORKDIR /code
COPY . .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 5000
CMD ["python", "main.py", "run"]
