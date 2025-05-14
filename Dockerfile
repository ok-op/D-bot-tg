FROM python:3.10-slim

WORKDIR /app

COPY . .
COPY stream.tar /app/stream.tar

RUN pip install -r requirements.txt

EXPOSE 3000

CMD ["python", "bot.py"]
