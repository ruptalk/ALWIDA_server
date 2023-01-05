FROM mariadb:10.9.3

COPY init.sql /docker-entrypoint-initdb.d
COPY test.jpeg /tmp/test.jpeg

EXPOSE 3306 

CMD ["mysqld"]
