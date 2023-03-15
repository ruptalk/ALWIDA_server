FROM mariadb:10.9.3

COPY init.sql /docker-entrypoint-initdb.d

EXPOSE 3306 

CMD ["mysqld"]
