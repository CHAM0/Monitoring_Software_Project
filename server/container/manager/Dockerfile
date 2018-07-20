# Use an official Python runtime as a parent image
FROM python:2.7-slim

# Copy the current directory contents into the container at /app
COPY requirements.txt /app/requirements.txt

# Set the working directory to /app
WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

# launch python script
#cmd ["python", "check.py"]

# launch python script
cmd ["python", "check.py"]
