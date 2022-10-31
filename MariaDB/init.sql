alter database alwida_db default character set utf8mb4;
set names utf8mb4;

CREATE TABLE `user_table` (
	`id`	VARCHAR(20)	NOT NULL,
	`pw`	VARCHAR(20)	NOT NULL,
	`name`	VARCHAR(20)	NOT NULL,
	`phone`	VARCHAR(11)	NOT NULL,
	`car_num`	VARCHAR(20)	NOT NULL,
	`check_num`	VARCHAR(5)	NOT NULL,
	`info_agree`	BOOLEAN	NOT NULL,
	`info_gps`	BOOLEAN	NOT NULL
);

CREATE TABLE `admin_table` (
	`uid`	VARCHAR(36)	NOT NULL,
	`id`	VARCHAR(20) UNIQUE	NOT NULL,
	`pw`	VARCHAR(20)	NOT NULL,
	`tn`	VARCHAR(30)	NOT NULL,
	`name`	VARCHAR(20)	NOT NULL,
	`phone`	VARCHAR(11)	NOT NULL,
	`enroll`	BOOLEAN	NULL
);

CREATE TABLE `terminal_table` (
	`tn`	VARCHAR(30)	NOT NULL,
	`name`	VARCHAR(50)	NOT NULL,
	`location`	VARCHAR(30)	NOT NULL,
	`car_amount`	INT	NOT NULL,
	`easy`	INT	NOT NULL	DEFAULT 0,
	`normal`	INT	NOT NULL	DEFAULT 0,
	`difficalt`	INT	NOT NULL	DEFAULT 0
);

CREATE TABLE `receipt_table` (
	`container_num`	VARCHAR(30)	NOT NULL,
	`id`	VARCHAR(20)	NOT NULL,
	`publish`	BOOLEAN	NOT NULL,
	`publish_datetime`	DATETIME	NULL
);

CREATE TABLE `container_table` (
	`container_num`	VARCHAR(30)	NOT NULL,
	`id`	VARCHAR(20)	NOT NULL,
	`tn`	VARCHAR(30)	NOT NULL,
	`scale`	VARCHAR(30)	NOT NULL,
	`fm`	VARCHAR(30)	NOT NULL,
	`position`	VARCHAR(30)	NULL,
	`contain_last_time`	DATETIME	NOT NULL,
	`in_out`	BOOLEAN	NOT NULL
);

CREATE TABLE `cash_table` (
	`id`	VARCHAR(20)	NOT NULL,
	`uid`	VARCHAR(36)	NOT NULL,
	`publish_pay`	VARCHAR(20)	NOT NULL,
	`pay_datetime`	DATETIME	NULL
);

CREATE TABLE `reservation_table` (
	`id`	VARCHAR(20)	NOT NULL,
	`container_num`	VARCHAR(30)	NOT NULL,
	`tn`	VARCHAR(30)	NOT NULL,
	`request_time`	DATETIME	NOT NULL,
	`accept_time`	DATETIME	NULL,
	`response_publish`	BOOLEAN	NOT NULL,
	`suggestion`	DATETIME	NULL
);

ALTER TABLE `user_table` ADD CONSTRAINT `PK_USER_TABLE` PRIMARY KEY (
	`id`
);

ALTER TABLE `admin_table` ADD CONSTRAINT `PK_ADMIN_TABLE` PRIMARY KEY (
	`uid`
);

ALTER TABLE `terminal_table` ADD CONSTRAINT `PK_TERMINAL_TABLE` PRIMARY KEY (
	`tn`
);

ALTER TABLE `receipt_table` ADD CONSTRAINT `PK_RECEIPT_TABLE` PRIMARY KEY (
	`container_num`
);

ALTER TABLE `container_table` ADD CONSTRAINT `PK_CONTAINER_TABLE` PRIMARY KEY (
	`container_num`
);

ALTER TABLE `cash_table` ADD CONSTRAINT `PK_CASH_TABLE` PRIMARY KEY (
	`id`
);

ALTER TABLE `reservation_table` ADD CONSTRAINT `PK_RESERVATION_TABLE` PRIMARY KEY (
	`id`
);

ALTER TABLE `admin_table` ADD CONSTRAINT `FK_terminal_table_TO_admin_table_1` FOREIGN KEY (
	`tn`
)
REFERENCES `terminal_table` (
	`tn`
);

ALTER TABLE `receipt_table` ADD CONSTRAINT `FK_container_table_TO_receipt_table_1` FOREIGN KEY (
	`container_num`
)
REFERENCES `container_table` (
	`container_num`
);

ALTER TABLE `receipt_table` ADD CONSTRAINT `FK_user_table_TO_receipt_table_1` FOREIGN KEY (
	`id`
)
REFERENCES `user_table` (
	`id`
);

ALTER TABLE `container_table` ADD CONSTRAINT `FK_user_table_TO_container_table_1` FOREIGN KEY (
	`id`
)
REFERENCES `user_table` (
	`id`
);

ALTER TABLE `container_table` ADD CONSTRAINT `FK_terminal_table_TO_container_table_1` FOREIGN KEY (
	`tn`
)
REFERENCES `terminal_table` (
	`tn`
);

ALTER TABLE `cash_table` ADD CONSTRAINT `FK_user_table_TO_cash_table_1` FOREIGN KEY (
	`id`
)
REFERENCES `user_table` (
	`id`
);

ALTER TABLE `cash_table` ADD CONSTRAINT `FK_admin_table_TO_cash_table_1` FOREIGN KEY (
	`uid`
)
REFERENCES `admin_table` (
	`uid`
);

ALTER TABLE `reservation_table` ADD CONSTRAINT `FK_user_table_TO_reservation_table_1` FOREIGN KEY (
	`id`
)
REFERENCES `user_table` (
	`id`
);

ALTER TABLE `reservation_table` ADD CONSTRAINT `FK_container_table_TO_reservation_table_1` FOREIGN KEY (
	`container_num`
)
REFERENCES `container_table` (
	`container_num`
);

ALTER TABLE `reservation_table` ADD CONSTRAINT `FK_terminal_table_TO_reservation_table_1` FOREIGN KEY (
	`tn`
)
REFERENCES `terminal_table` (
	`tn`
);

INSERT INTO terminal_table VALUES('부산 터미널1','터미널1','부산',0,0,0,0);
INSERT INTO terminal_table VALUES('부산 터미널2','터미널2','부산',0,0,0,0);
INSERT INTO terminal_table VALUES('서울 터미널1','터미널1','서울',0,0,0,0);

INSERT INTO admin_table VALUES (UUID(), 'admin1','admin1','부산 터미널1','admin1','01011111111',NULL);
INSERT INTO admin_table VALUES (UUID(), 'admin2','admin2','부산 터미널2','admin2','01022222222',NULL);
INSERT INTO admin_table VALUES (UUID(), 'admin3','admin3','서울 터미널1','admin3','01033333333',NULL);


INSERT INTO user_table VALUES ('user1','user1','user1','01099999999','1111','AAAA', 1, 1);
INSERT INTO user_table VALUES ('user2','user2','user2','01088888888','2222','AAAA', 1, 1);
INSERT INTO user_table VALUES ('user3','user3','user3','01077777777','3333','AAAA', 1, 1);
INSERT INTO user_table VALUES ('user4','user4','user4','01066666666','4444','AAAA', 1, 1);
INSERT INTO user_table VALUES ('user5','user5','user5','01055555555','5555','AAAA', 1, 1);
INSERT INTO user_table VALUES ('user6','user6','user6','01055555555','5555','AAAA', 1, 1);
INSERT INTO user_table VALUES ('user7','user7','user7','01055555555','5555','AAAA', 1, 1);
INSERT INTO user_table VALUES ('user8','user8','user8','01055555555','5555','AAAA', 1, 1);
INSERT INTO user_table VALUES ('user9','user9','user9','01055555555','5555','AAAA', 1, 1);
INSERT INTO user_table VALUES ('user10','user10','user10','01055555555','5555','AAAA', 1, 1);
INSERT INTO user_table VALUES ('user11','user11','user11','01055555555','5555','AAAA', 1, 1);
INSERT INTO user_table VALUES ('user12','user12','user12','01055555555','5555','AAAA', 1, 1);
INSERT INTO user_table VALUES ('user13','user13','user13','01055555555','5555','AAAA', 1, 1);
INSERT INTO user_table VALUES ('user14','user14','user14','01055555555','5555','AAAA', 1, 1);

INSERT INTO container_table VALUES ('1111','user1','부산 터미널1','규격1','F','장치위치1',NOW(),1);
INSERT INTO reservation_table VALUES ('user1', '1111', '부산 터미널1',NOW(), NULL, 0, NULL);
INSERT INTO container_table VALUES ('2222','user2','부산 터미널1','규격2','F','장치위치2',NOW(),1);
INSERT INTO reservation_table VALUES ('user2', '2222', '부산 터미널1',NOW(), NULL, 0, NULL);
INSERT INTO container_table VALUES ('3333','user3','부산 터미널1','규격3','F','장치위치3',NOW(),1);
INSERT INTO reservation_table VALUES ('user3', '3333', '부산 터미널1',NOW(), NULL, 0, NULL);
INSERT INTO container_table VALUES ('4444','user4','부산 터미널1','규격4','F','장치위치4',NOW(),1);
INSERT INTO reservation_table VALUES ('user4', '4444', '부산 터미널1',NOW(), NULL, 0, NULL);
INSERT INTO container_table VALUES ('5555','user5','부산 터미널2','규격5','F','장치위치5',NOW(),1);
INSERT INTO reservation_table VALUES ('user5', '5555', '부산 터미널2',NOW(), NULL, 0, NULL);

INSERT INTO container_table VALUES ('6666','user6','부산 터미널1','규격5','F','장치위치5',NOW(),1);
INSERT INTO reservation_table VALUES ('user6', '6666', '부산 터미널1',"2022-11-01 06:00:00", "2022-11-01 06:00:00", 1, NULL);
INSERT INTO container_table VALUES ('7777','user7','부산 터미널1','규격5','F','장치위치5',NOW(),1);
INSERT INTO reservation_table VALUES ('user7', '7777', '부산 터미널1',"2022-11-01 06:05:00", "2022-11-01 06:05:00", 1, NULL);
INSERT INTO container_table VALUES ('8888','user8','부산 터미널1','규격5','F','장치위치5',NOW(),1);
INSERT INTO reservation_table VALUES ('user8', '8888', '부산 터미널1',"2022-11-01 06:29:00", "2022-11-01 06:29:00", 1, NULL);
INSERT INTO container_table VALUES ('9999','user9','부산 터미널1','규격5','F','장치위치5',NOW(),1);
INSERT INTO reservation_table VALUES ('user9', '9999', '부산 터미널1',"2022-11-01 06:30:00", "2022-11-01 06:30:00", 1, NULL);
INSERT INTO container_table VALUES ('10101010','user10','부산 터미널1','규격5','F','장치위치5',NOW(),1);
INSERT INTO reservation_table VALUES ('user10', '10101010', '부산 터미널1',"2022-11-01 06:35:00", "2022-11-01 06:35:00", 1, NULL);
INSERT INTO container_table VALUES ('11111111','user11','부산 터미널1','규격5','F','장치위치5',NOW(),1);
INSERT INTO reservation_table VALUES ('user11', '11111111', '부산 터미널1',"2022-11-01 07:19:00", "2022-11-01 07:19:00", 1, NULL);
INSERT INTO container_table VALUES ('12121212','user12','부산 터미널1','규격5','F','장치위치5',NOW(),1);
INSERT INTO reservation_table VALUES ('user12', '12121212', '부산 터미널1',"2022-11-01 07:00:00", "2022-11-01 07:00:00", 1, NULL);
INSERT INTO container_table VALUES ('13131313','user13','부산 터미널1','규격5','F','장치위치5',NOW(),1);
INSERT INTO reservation_table VALUES ('user13', '13131313', '부산 터미널1',"2022-11-01 07:15:00", "2022-11-01 07:15:00", 1, NULL);
INSERT INTO container_table VALUES ('14141414','user14','부산 터미널1','규격5','F','장치위치5',NOW(),1);
INSERT INTO reservation_table VALUES ('user14', '14141414', '부산 터미널1',"2022-11-01 07:29:00", "2022-11-01 07:29:00", 1, NULL);