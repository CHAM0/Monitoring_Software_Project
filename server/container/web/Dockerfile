# Use an official Python runtime as a parent image
FROM arangodb

# Copy the current directory contents into the container at /app
#COPY requirements.txt /app/requirements.txt

# Set the working directory to /app
WORKDIR /app

#RUN pip install -r requirements.txt

#COPY . /app

# launch python script
#cmd ["python", "app.py"]

# Expose listen port
EXPOSE 8529

# Expose our data, logs and configuration volumes
#VOLUME ["/data", "/var/log/arangodb", "/etc/arangodb"]