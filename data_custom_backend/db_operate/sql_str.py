# -*- coding: utf-8 -*-
"""
-------------------------------------------------
File Name： sql_str
Description :
Author : 'li'
date： 2020/10/20
-------------------------------------------------
Change Activity:
2020/10/20:
-------------------------------------------------
"""
from config.database_config import DB_NAME

QUERY_TABLE_NAME = """select table_name,table_comment from information_schema.tables
 where table_schema='%s';""".replace('%s', DB_NAME)
DROP_TABLE = """DROP TABLE `$table_name` ;"""

ALERT_TABLE_NAME = """alter table `%old_name` rename to `%new_name`; """

CREATE_TABLE = """create table `%TABLE_NAME` (
 unique_id int not null auto_increment primary key,%COLUMNS_INFO)
  COMMENT='%table_comment' ;"""

QUERY_COLUMN_INFO = """SELECT column_name, data_type, column_comment  FROM information_schema.columns 
WHERE table_name = '%table_name' ORDER BY ORDINAL_POSITION; """
ADD_COLUMN = """ALTER  TABLE `%table_name` add  column  
                `%column_name`  %data_type   COMMENT '%new_comment' ; """
DELETE_COLUMN = """alter table `%table_name` drop column `%column_name`; """
ADD_DATA = """INSERT INTO `%table_name` ( %fields )   VALUES  ( %values);"""
UPDATE_DATA = """UPDATE  `%table_name` SET %update_content where `unique_id` ='$unique_id';"""

ALTER_TABLE_COMMENT = """alter table `%TABLE_NAME` comment '%TABLE_COMMENT'; """
