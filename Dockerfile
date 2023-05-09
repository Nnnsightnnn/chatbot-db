FROM  redis/redis-stack:latest

# Create application directory
RUN mkdir /chatbot-db

# Copy application files to container
ADD . /chatbot-db

# Create RediSearch directory
RUN mkdir /RediSearch

# Add files from RediSearch to directory
RUN git clone --recursive https://github.com/RediSearch/RediSearch.git

# Navigate to RediSearch
RUN cd RediSearch

# Installation
RUN make setup
RUN make build

RUN make run

# Goto Main Directory
RUN cd ..

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
