use androzoo;
drop table if exists applist;
create table applist(
	sha256 char(64) not null,
	sha1 char(40),
	md5 char(32),
	dex_date text,
	apk_size text,
	pkg_name text,
	vercode text,
	vt_detection text,
	vt_scan_date text,
	dex_size text,
	markets text
);

SHOW VARIABLES LIKE "secure_file_priv";

LOAD DATA INFILE '/var/lib/mysql-files/latest.csv'
INTO TABLE androzoo.applist
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n';

ALTER TABLE androzoo.applist ADD COLUMN `id` INT AUTO_INCREMENT UNIQUE FIRST;

ALTER TABLE androzoo.applist 
ADD PRIMARY KEY (id);

SET SQL_SAFE_UPDATES = 0;
UPDATE androzoo.applist 
   SET `pkg_name` = TRIM(BOTH '"' FROM `pkg_name`);
   
alter table applist add column app_type text;

alter table applist add column app_permissions text;

alter table applist add column app_genre text;

alter table applist add column app_details text;

# For each database:
ALTER DATABASE androzoo CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;
# For each table:
ALTER TABLE androzoo.applist CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
# For each column:
ALTER TABLE androzoo.applist CHANGE app_details app_details text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

SELECT pkg_name FROM applist where markets like '%play.google.com%' and id between 1 and 5;

SELECT id,sha256,pkg_name FROM applist where markets like '%play.google.com%' and pkg_name like '%kr.ac.snjc.library%';

SELECT count(*) FROM androzoo.applist where markets like '%play.google.com%' and (app_details is null or app_details='') and id between 1 and 2000;

SELECT count(*) FROM androzoo.applist where markets like '%play.google.com%' and id between 1 and 100000;

select app_details FROM androzoo.applist where markets like '%play.google.com%' and id between 15401 and 15500;


select (SELECT count(*) as cnt FROM androzoo.applist where markets like '%play.google.com%') as total_play,
((SELECT count(*) as cnt FROM androzoo.applist where markets like '%play.google.com%') - 
(SELECT count(*) FROM androzoo.applist where markets like '%play.google.com%' and (app_details is null or app_details='')))
as total_done;