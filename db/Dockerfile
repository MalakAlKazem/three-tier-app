# Use the official PostgreSQL image
FROM postgres:16

# Environment variables for PostgreSQL
ENV POSTGRES_DB=appdb
ENV POSTGRES_USER=dbuser
ENV POSTGRES_PASSWORD=password123

# Copy the initialization SQL script
# PostgreSQL will automatically run any .sql files in /docker-entrypoint-initdb.d/
COPY init.sql /docker-entrypoint-initdb.d/

# Expose PostgreSQL port (documentation purposes)
EXPOSE 5432