# incoporate the python version for the programme
FROM python:3.9-slim-buster

# install system dependencies
RUN apt-get update && apt-get install -y \
    python3-pip python3-dev \
    build-essential libssl-dev libffi-dev python3-setuptools \
    netcat
    
# setting the working directory
WORKDIR /app

# copy the requirements 
COPY ./requirements.txt .
COPY ./requirements_google.txt .

# # expose the port that flask will run on
EXPOSE 3303

# Set the FLASK_APP and FLASK_ENV environment variables
ENV FLASK_APP=src/server.py

# install the requirements
RUN pip3 install -r requirements.txt
RUN pip3 install -r requirements_google.txt

# Copy the program files to docker app directory
COPY . .




# CMD ["flask", "run", "--host", "0.0.0.0"]