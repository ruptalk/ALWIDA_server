alter database alwida_db default character set utf8mb4;
set names utf8mb4;

CREATE TABLE `user_table` (
	`id`	VARCHAR(20)	NOT NULL,
	`pw`	VARCHAR(20)	NOT NULL,
	`name`	VARCHAR(20)	NOT NULL,
	`phone`	VARCHAR(11)	NOT NULL,
	`tn`	VARCHAR(30)	NOT NULL,
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
	`container_num`	VARCHAR(30)	NOT NULL,
	`publish_pay`	BOOLEAN	NOT NULL,
	`pay_datetime`	DATETIME	NULL
);

CREATE TABLE `reservation_table` (
	`id`	VARCHAR(20)	NOT NULL,
	`container_num`	VARCHAR(30)	NOT NULL,
	`tn`	VARCHAR(30)	NOT NULL,
	`request_time`	DATETIME	NOT NULL,
	`accept_time`	DATETIME	NULL,
	`suggestion`	VARCHAR(20)	NULL
);

CREATE TABLE `check_table` (
	`id`	VARCHAR(20)	NOT NULL,
	`request_time`	DATETIME	NOT NULL,
	`img`	LONGBLOB	NOT NULL,
	`result`	INT	NOT NULL
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

ALTER TABLE `check_table` ADD CONSTRAINT `PK_CHECK_TABLE` PRIMARY KEY (
	`id`
);

ALTER TABLE `user_table` ADD CONSTRAINT `FK_terminal_table_TO_user_table_1` FOREIGN KEY (
	`tn`
)
REFERENCES `terminal_table` (
	`tn`
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

ALTER TABLE `cash_table` ADD CONSTRAINT `FK_container_table_TO_cash_table_1` FOREIGN KEY (
	`container_num`
)
REFERENCES `container_table` (
	`container_num`
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

ALTER TABLE `check_table` ADD CONSTRAINT `FK_user_table_TO_check_table_1` FOREIGN KEY (
	`id`
)
REFERENCES `user_table` (
	`id`
);

-- insert terminal
INSERT INTO terminal_table VALUES ('PNIT','국제신항','부산신항',0,0,0,0);
INSERT INTO terminal_table VALUES ('PNC','부산신항','부산신항',0,0,0,0);
INSERT INTO terminal_table VALUES ('HJNC','한진신항','부산신항',0,0,0,0);
INSERT INTO terminal_table VALUES ('HNPT','현대신항','부산신항',0,0,0,0);
INSERT INTO terminal_table VALUES ('BNCT','고려신항','부산신항',0,0,0,0);
INSERT INTO terminal_table VALUES ('BCT','부산 컨테이너 터미널','부산신항',0,0,0,0);

INSERT INTO terminal_table VALUES ('PECT','신선대','부산북항',0,0,0,0);
INSERT INTO terminal_table VALUES ('BIT','감만부두','부산북항',0,0,0,0);
INSERT INTO terminal_table VALUES ('DPCT','동부','부산북항',0,0,0,0);
INSERT INTO terminal_table VALUES ('INTERGIS','7부두','부산북항',0,0,0,0);
INSERT INTO terminal_table VALUES ('Hutchison','5부두','부산북항',0,0,0,0);

INSERT INTO terminal_table VALUES ('PSA','인천 컨테이너 터미널','인천항',0,0,0,0);
INSERT INTO terminal_table VALUES ('E1 컨테이너 터미널','E1 컨테이너 터미널','인천항',0,0,0,0);
INSERT INTO terminal_table VALUES ('인천신항','선광신컨테이너 터미널','인천항',0,0,0,0);
INSERT INTO terminal_table VALUES ('HJIT','한진 인천 컨테이너 터미널','인천항',0,0,0,0);

INSERT INTO terminal_table VALUES ('정일 울산 컨테이너 터미널','정일 울산 컨테이너 터미널','울산항',0,0,0,0);

INSERT INTO terminal_table VALUES ('PICT','포항 열일 신항만','포항',0,0,0,0);

INSERT INTO terminal_table VALUES ('허치슨포트 광양 컨테이너 터미널','허치슨포트 광양 컨테이너 터미널','광양',0,0,0,0);
INSERT INTO terminal_table VALUES ('CJ 대한통운','CJ 대한통운','광양',0,0,0,0);
INSERT INTO terminal_table VALUES ('SM 상선 광양터미널','SM 상선 광양터미널','광양',0,0,0,0);

INSERT INTO terminal_table VALUES ('군산 컨테이너 터미널','군산 컨테이너 터미널','군산항',0,0,0,0);

INSERT INTO terminal_table VALUES ('평택항 신컨테이너 터미널','평택항 신컨테이너 터미널','평택항',0,0,0,0);

INSERT INTO terminal_table VALUES ('의왕 ICD 제1터미널','의왕 ICD 제1터미널','의왕 ICD',0,0,0,0);
INSERT INTO terminal_table VALUES ('의왕 ICD 제2터미널','의왕 ICD 제2터미널','의왕 ICD',0,0,0,0);

INSERT INTO admin_table VALUES (UUID(), 'admin1','admin1','PNIT','admin1','01011111111',NULL);
INSERT INTO admin_table VALUES (UUID(), 'admin2','admin2','PNC','admin2','01022222222',NULL);
INSERT INTO admin_table VALUES (UUID(), 'admin3','admin3','HJNC','admin3','01033333333',NULL);
-- end insert terminal

INSERT INTO user_table VALUES ('user1','user1','user1','01099999999','PNIT','1111','AAAA', 1, 1);
INSERT INTO user_table VALUES ('user2','user2','user2','01088888888','PNIT','2222','AAAA', 1, 1);
INSERT INTO user_table VALUES ('user3','user3','user3','01077777777','PNIT','3333','AAAA', 1, 1);
INSERT INTO user_table VALUES ('user4','user4','user4','01066666666','PNIT','4444','AAAA', 1, 1);
INSERT INTO user_table VALUES ('user5','user5','user5','01055555555','PNIT','5555','AAAA', 1, 1);
INSERT INTO user_table VALUES ('user6','user6','user6','01055555555','PNC','5555','AAAA', 1, 1);
INSERT INTO user_table VALUES ('user7','user7','user7','01055555555','PNC','5555','AAAA', 1, 1);
INSERT INTO user_table VALUES ('user8','user8','user8','01055555555','PNC','5555','AAAA', 1, 1);
INSERT INTO user_table VALUES ('user9','user9','user9','01055555555','PNC','5555','AAAA', 1, 1);
INSERT INTO user_table VALUES ('user10','user10','user10','01055555555','PNC','5555','AAAA', 1, 1);
INSERT INTO user_table VALUES ('user11','user11','user11','01055555555','HJNC','5555','AAAA', 1, 1);
INSERT INTO user_table VALUES ('user12','user12','user12','01055555555','HJNC','5555','AAAA', 1, 1);
INSERT INTO user_table VALUES ('user13','user13','user13','01055555555','HJNC','5555','AAAA', 1, 1);
INSERT INTO user_table VALUES ('user14','user14','user14','01055555555','HJNC','5555','AAAA', 1, 1);

INSERT INTO container_table VALUES ('1111','user1','PNIT','규격1','F','장치위치1',NOW(),1);
INSERT INTO reservation_table VALUES ('user1', '1111', 'PNIT',NOW(), NULL, NULL);
INSERT INTO container_table VALUES ('2222','user2','PNIT','규격2','F','장치위치2',NOW(),1);
INSERT INTO reservation_table VALUES ('user2', '2222', 'PNIT',NOW(), NULL, NULL);
INSERT INTO container_table VALUES ('3333','user3','PNIT','규격3','F','장치위치3',NOW(),1);
INSERT INTO reservation_table VALUES ('user3', '3333', 'PNIT',NOW(), NULL, NULL);
INSERT INTO container_table VALUES ('4444','user4','PNIT','규격4','F','장치위치4',NOW(),1);
INSERT INTO reservation_table VALUES ('user4', '4444', 'PNIT',NOW(), NULL, NULL);
INSERT INTO container_table VALUES ('5555','user5','PNIT','규격5','F','장치위치5',NOW(),1);
INSERT INTO reservation_table VALUES ('user5', '5555', 'PNIT',NOW(), NULL, NULL);

INSERT INTO container_table VALUES ('6666','user6','PNIT','규격5','F','장치위치5',NOW(),1);
INSERT INTO reservation_table VALUES ('user6', '6666', 'PNIT',"2022-11-07 06:00:00", "2022-11-07 06:00:00", NULL);
INSERT INTO container_table VALUES ('7777','user7','PNIT','규격5','F','장치위치5',NOW(),1);
INSERT INTO reservation_table VALUES ('user7', '7777', 'PNIT',"2022-11-07 06:05:00", "2022-11-07 06:05:00", NULL);
INSERT INTO container_table VALUES ('8888','user8','PNIT','규격5','F','장치위치5',NOW(),1);
INSERT INTO reservation_table VALUES ('user8', '8888', 'PNIT',"2022-11-07 06:29:00", "2022-11-07 06:29:00", NULL);
INSERT INTO container_table VALUES ('9999','user9','PNIT','규격5','F','장치위치5',NOW(),1);
INSERT INTO reservation_table VALUES ('user9', '9999', 'PNIT',"2022-11-07 06:30:00", "2022-11-07 06:30:00", NULL);
INSERT INTO container_table VALUES ('10101010','user10','PNIT','규격5','F','장치위치5',NOW(),1);
INSERT INTO reservation_table VALUES ('user10', '10101010', 'PNIT',"2022-11-07 06:35:00", "2022-11-07 06:35:00", NULL);
INSERT INTO container_table VALUES ('11111111','user11','PNIT','규격5','F','장치위치5',NOW(),1);
INSERT INTO reservation_table VALUES ('user11', '11111111', 'PNIT',"2022-11-07 07:19:00", "2022-11-07 07:19:00", NULL);
INSERT INTO container_table VALUES ('12121212','user12','PNIT','규격5','F','장치위치5',NOW(),1);
INSERT INTO reservation_table VALUES ('user12', '12121212', 'PNIT',"2022-11-07 07:00:00", "2022-11-07 07:00:00", NULL);
INSERT INTO container_table VALUES ('13131313','user13','PNIT','규격5','F','장치위치5',NOW(),1);
INSERT INTO reservation_table VALUES ('user13', '13131313', 'PNIT',"2022-11-07 07:15:00", "2022-11-07 07:15:00", NULL);
INSERT INTO container_table VALUES ('14141414','user14','PNIT','규격5','F','장치위치5',NOW(),1);
INSERT INTO reservation_table VALUES ('user14', '14141414', 'PNIT',"2022-11-07 07:29:00", "2022-11-07 07:29:00", NULL);

INSERT INTO receipt_table VALUES ('1111','user1',0,NULL);
INSERT INTO receipt_table VALUES ('2222','user2',0,NULL);
INSERT INTO receipt_table VALUES ('3333','user3',0,NULL);
INSERT INTO receipt_table VALUES ('4444','user4',0,NULL);
INSERT INTO receipt_table VALUES ('5555','user5',0,NULL);
INSERT INTO receipt_table VALUES ('6666','user6',1,NOW());
INSERT INTO receipt_table VALUES ('7777','user7',1,NOW());
INSERT INTO receipt_table VALUES ('8888','user8',1,NOW());
INSERT INTO receipt_table VALUES ('9999','user9',1,NOW());
INSERT INTO receipt_table VALUES ('10101010','user10',1,NOW());

INSERT INTO cash_table VALUES ('user1','1111',0,NULL);
INSERT INTO cash_table VALUES ('user2','2222',1,NOW());
INSERT INTO cash_table VALUES ('user3','3333',0,NULL);
INSERT INTO cash_table VALUES ('user4','4444',1,NOW());
INSERT INTO cash_table VALUES ('user5','5555',1,NOW());
INSERT INTO cash_table VALUES ('user6','6666',0,NULL);

INSERT INTO check_table VALUES('user1',NOW(),"AAAA",0);
INSERT INTO check_table VALUES('user2',NOW(),"AAAA",0);
INSERT INTO check_table VALUES('user3',NOW(),"AAAA",0);
INSERT INTO check_table VALUES('user4',NOW(),"AAAA",1);
INSERT INTO check_table VALUES('user5',NOW(),"AAAA",2);
INSERT INTO check_table VALUES('user6',NOW(),"AAAA",0);
INSERT INTO check_table VALUES('user7',NOW(),"AAAA",3);
INSERT INTO check_table VALUES('user8',NOW(),"AAAA",4);