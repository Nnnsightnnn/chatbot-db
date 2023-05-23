FROM python:3.11.3

# Create application directory
WORKDIR /chatbot-db

# Copy application files to container
COPY . .

# Install application dependencies
RUN apt-get update && \
    apt-get install -y python3-pip && \
    pip3 install --no-cache-dir -r requirements.txt && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Start application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app", "python3", "app.py"]