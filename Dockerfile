# Use an official Python image as the base
FROM python:3.9-slim

# Set the working directory
WORKDIR /workdir
# Install Git
RUN apt-get update && apt-get install -y git && apt-get clean

# Copy requirements and project files
COPY requirements.txt ./
COPY . . 
RUN pip install langchain openai python-dotenv
RUN apt-get update && apt-get install -y git && apt-get clean
RUN apt-get update && apt-get install wget -y


# Expose the port (optional for web-based apps)
EXPOSE 8000

