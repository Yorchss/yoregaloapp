FROM python:3.10-slim

# System dependencies for Chromium and headless support
RUN apt-get update && apt-get install -y \
    wget curl unzip gnupg2 ca-certificates \
    chromium chromium-driver \
    libglib2.0-0 libnss3 libgconf-2-4 libx11-xcb1 libxcomposite1 \
    libxcursor1 libxdamage1 libxi6 libxtst6 libatk1.0-0 libatk-bridge2.0-0 \
    libgtk-3-0 libxrandr2 libasound2 libxshmfence-dev libgbm-dev \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables for Flask
ENV FLASK_APP=consume.py
ENV FLASK_RUN_HOST=0.0.0.0    

# Set the working directory inside the container
WORKDIR /app

# Copy project files into the container
COPY . /app

# Install dependencies
COPY requirements.txt .
RUN pip install undetected-chromedriver flask requests undetected-chromedriver selenium webdriver-manager setuptools
RUN pip3 install undetected-chromedriver flask requests undetected-chromedriver selenium webdriver-manager setuptools
RUN pip install --no-cache-dir -r requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt
# Expose Flask's default port
EXPOSE 5000

# Run the Flask application
CMD ["python", "consume.py"]