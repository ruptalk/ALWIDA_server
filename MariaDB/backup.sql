alter database alwida_db default character set utf8mb4;
set names utf8mb4;

CREATE TABLE admin_account(
    userid VARCHAR(20) NOT NULL,
    userpw VARCHAR(20) NOT NULL,
    destination VARCHAR(40) NOT NULL,
    PRIMARY KEY(userid)
);

INSERT INTO admin_account VALUES ('admin1','admin1','부산 국제 터미널');

CREATE TABLE working_time(
    id INT(10) NOT NULL AUTO_INCREMENT,
    destination VARCHAR(40) NOT NULL,
    request_time DATETIME NOT NULL,
    accept_time DATETIME,
    admin_check BOOLEAN NOT NULL,
    PRIMARY KEY(id)
);

INSERT INTO working_time VALUES (NULL,'부산 국제 터미널',NOW(), NULL, FALSE);
INSERT INTO working_time VALUES (NULL,'서울 국제 터미널',NOW(), NULL, FALSE);
INSERT INTO working_time VALUES (NULL,'부산 국제 터미널',NOW(), NULL, FALSE);
INSERT INTO working_time VALUES (NULL,'서울 국제 터미널',NOW(), NULL, FALSE);
INSERT INTO working_time VALUES (NULL,'서울 국제 터미널',NOW(), NULL, FALSE);
INSERT INTO working_time VALUES (NULL,'부산 국제 터미널',NOW(), NULL, FALSE);