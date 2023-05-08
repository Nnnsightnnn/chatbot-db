FROM redislabs/redis-stack:latest

# Copy application files to container
COPY chatbot-db /chatbot-db

# Set working directory
WORKDIR /chatbot-db

# Install application dependencies
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    pip3 install -r requirements.txt

# Expose application port
EXPOSE 6973 5000

# Start application
CMD ["python3", "app.py"]
