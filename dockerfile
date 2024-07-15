# Use an official Python runtime as a parent image
FROM python:3.9-slim as base

# Install PostgreSQL client tools
RUN apt-get update && apt-get install -y postgresql-client

# Set the working directory in the container
WORKDIR /insaitbackend

# Copy the current directory contents into the container at /insaitbackend
COPY . /insaitbackend

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV FLASK_APP=app.py

# Run app.py when the container launches
CMD ["flask", "run", "--host=0.0.0.0"]

# Test stage
FROM base as test

# Set the working directory for the test stage
WORKDIR /insaitbackend

# Copy only the necessary files from the base stage
COPY --from=base /insaitbackend /insaitbackend

# Run tests
CMD ["pytest"]
