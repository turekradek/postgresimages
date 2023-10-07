# Use Ubuntu 22.04 as a parent image
FROM ubuntu:22.04

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
ADD . /app

# Set environment variables to avoid timezone prompt
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Warsaw

# install tools
RUN apt-get update && \
    apt-get install -y jq net-tools
# Install Python, pip, sudo, vim, and dependencies for psycopg2-binary
RUN apt-get update && \
    apt-get install -y python3.11 python3-pip sudo vim libpq-dev python3-dev build-essential

# Install PostgreSQL
RUN apt-get install -y postgresql postgresql-contrib

# Set PostgreSQL to accept connections with md5 password
RUN echo "local all postgres md5" >> /etc/postgresql/14/main/pg_hba.conf

# Setup the environment variable for PostgreSQL password
ENV POSTGRES_PASSWORD=password

# Update pip
RUN pip install --upgrade pip

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME World

# Run a PostgreSQL command file:
COPY init.sql /docker-entrypoint-initdb.d/

# Start PostgreSQL and initialize database
RUN service postgresql start && su - postgres -c "psql -f /docker-entrypoint-initdb.d/init.sql"

# Keep the container running
CMD ["tail", "-f", "/dev/null"]

# su - postgres -c "psql"
# \l
# \d 
# \d table
# ALTER USER postgres WITH PASSWORD 'xyz'
