FROM redis/redis-stack:7.0.6-RC8

# Create application directory
RUN mkdir /chatbot-db

# Copy application files to container
COPY . /chatbot-db

# Set working directory
WORKDIR /chatbot-db

# Install application dependencies
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    pip3 install -r requirements.txt

# Start application
CMD redis-server & python3 app.py
