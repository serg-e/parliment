
# Use the Python3.7.1 image
FROM python:3.7.1-stretch

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Install the dependencies
RUN pip install -r requirements.txt

# run the command to start uWSGI CMD ["uwsgi", "app.ini"]
