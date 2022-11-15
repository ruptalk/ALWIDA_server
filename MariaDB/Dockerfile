FROM mariadb:10.9.3

ENV MYSQL_ROOT_PASSWORD=root
ENV MYSQL_DATABASE=alwida_db
ENV MYSQL_USER=alwida_user
ENV MYSQL_PASSWORD=alwida

COPY my.cnf /etc/mysql/my.cnf
COPY init.sql /docker-entrypoint-initdb.d
COPY test.jpeg /tmp/test.jpeg

EXPOSE 3306 

CMD ["mysqld"]
