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

# INSTALL GIT 
# RUN sudo apt-get install git-all 
# install zsh 
RUN apt-get update && apt-get install -y git-all
RUN apt install zsh -y
RUN sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
RUN git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/themes/powerlevel10k
RUN git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions


# install zsh
# RUN sh -c "$(wget -O- https://github.com/deluan/zsh-in-docker/releases/download/v1.1.5/zsh-in-docker.sh)" -- \
#     -a 'CASE_SENSITIVE="true"'

# Uses "Spaceship" theme with some customization. Uses some bundled plugins and installs some more from github
# RUN sh -c "$(wget -O- https://github.com/deluan/zsh-in-docker/releases/download/v1.1.5/zsh-in-docker.sh)" -- \
#     -t https://github.com/denysdovhan/spaceship-prompt \
#     -a 'SPACESHIP_PROMPT_ADD_NEWLINE="false"' \
#     -a 'SPACESHIP_PROMPT_SEPARATE_LINE="false"' \
#     -p git \
#     -p ssh-agent \
#     -p https://github.com/zsh-users/zsh-autosuggestions \
#     -p https://github.com/zsh-users/zsh-completions
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
# Set environment variables (replace 'your_password' with your desired password)
# ENV POSTGRES_USER postgres
# ENV POSTGRES_PASSWORD your_password
# ENV POSTGRES_DB your_database
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
# docker run -d --name postgrestest20 -v ~/docker_test:/var/lib/docker_test -e POSTGRES_PASSWORD=radek -p 5433 postgres1:2.0
