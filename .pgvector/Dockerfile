# Use the pgvector image as the base
FROM ankane/pgvector

# Set environment variables
ENV POSTGRES_DB=vectordb
ENV POSTGRES_USER=testuser
ENV POSTGRES_PASSWORD=testpwd
ENV POSTGRES_HOST_AUTH_METHOD=trust

# Copy initialization SQL script
COPY init.sql /docker-entrypoint-initdb.d/init.sql

# Expose the PostgreSQL port
EXPOSE 5432
