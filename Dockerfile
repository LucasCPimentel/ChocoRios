# Use the official Python image as the base image
FROM python:3.8

# Set the working directory in the container
WORKDIR /app

# Copy the application files into the working directory
COPY . /app

# Install the application dependencies
RUN pip install -r requirements.txt

# Defina as variáveis de ambiente necessárias para o Flask
ENV FLASK_APP=ChocoRios.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=8000

EXPOSE 8000

# Define the entry point for the container
CMD ["flask", "run"]
