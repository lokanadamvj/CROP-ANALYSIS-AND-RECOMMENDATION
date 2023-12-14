# parent base image
FROM python:3.8-slim

# set work directory
WORKDIR /src/app

# copy requirements.txt
COPY ./requirements.txt /src/app/requirements.txt

# install system dependencies
RUN apt-get update \
    # && apt-get -y install gcc make \
    && rm -rf /var/lib/apt/lists/* \
    &&  pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# copy project
COPY . .

# set app port
EXPOSE 8080

ENTRYPOINT [ "python" ] 

# Run app.py when the container launches
CMD [ "app.py","run","--host","0.0.0.0","--port","8080"]