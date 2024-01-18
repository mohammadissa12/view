# Use an official Python runtime as a parent image
FROM python:3.10-alpine

# Upgrade pip
RUN pip install --upgrade pip

# Copy the requirements file and install the required Python packages
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Copy the current directory contents into the container at /django-app
COPY . /django-app

# Set the working directory to /django-app
WORKDIR /django-app

# Make the entrypoint script executable
RUN chmod +x entrypoint.sh

# Define the script to be executed when the container starts
ENTRYPOINT ["sh","entrypoint.sh"]
