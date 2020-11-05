FROM postgres

ENV POSTGRES_DB=developeum
ENV POSTGRES_USER=db_user
ENV POSTGRES_PASSWORD=ch4ng3_m3_plz

COPY schema/schema.sql /docker-entrypoint-initdb.d/
