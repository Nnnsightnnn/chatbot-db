FROM redis-stack-server

WORKDIR /chatbot-db

RUN pip install -r requirements.txt

CMD ["python", "app.py"]