FROM  redis/redis-stack:latest

# Create application directory
RUN mkdir /chatbot-db

# Copy application files to container
ADD . /chatbot-db

# Set working directory
WORKDIR /chatbot-db

# Install application dependencies
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    pip3 install -r requirements.txt

# Expose application port
EXPOSE 6973 5000 8001

# Start application
CMD ["python3", "app.py"]
