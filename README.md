# postgresimages
simple image of 
- docker run -d --name NAME -e POSTGRES_PASSWORD=password
- docker run -d --name NAME -e POSTGRES_PASSWORD=password  -p 5432 NAME:1.0
- docker run -d --name NAME -v -e POSTGRES_PASSWORD=password  -p 5432 NAME:1.0
- docker run -d --name postgrestest1 -v ~/docker_volume:/docker_volume -e POSTGRES_PASSWORD=radek -p 5432 postgreszshexcel:1.0
- docker exec -it NAME sh
service postgresql start
su - postgres -c "psql"
\l 
\d 
\dt
# Change the password
ALTER USER name WITH PASSWORD 'xyz';

