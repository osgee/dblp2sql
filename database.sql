DROP DATABASE `dblp`;
CREATE DATABASE `dblp`;
USE `dblp`;

CREATE TABLE `author`(
    `authorid` INT PRIMARY KEY AUTO_INCREMENT  NOT NULL,
    `author` VARCHAR (50) UNIQUE NOT NULL
    )DEFAULT CHARSET=`utf8` AUTO_INCREMENT=1;

CREATE TABLE `journal`(
    `journalid` INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    `journal` VARCHAR (50) UNIQUE NOT NULL
    )DEFAULT CHARSET=`utf8` AUTO_INCREMENT=1;


CREATE TABLE `article`(
    `articleid` INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    `arttype` INT ,
    `key` VARCHAR (200) UNIQUE NOT NULL,
    `mdate` TIMESTAMP,
    `publtype` VARCHAR (50) DEFAULT null NULL ,
    `reviewid` VARCHAR (50) DEFAULT null NULL ,
    `rating` VARCHAR (50) DEFAULT null NULL ,
    `editer` VARCHAR (50) DEFAULT null NULL ,
    `title` VARCHAR (200) ,
    `booktitle` VARCHAR (100) DEFAULT null NULL ,
    `pagestart` INT NULL ,
    `pageend` INT DEFAULT null NULL ,
    `year` INT DEFAULT null NULL ,
    `address` VARCHAR (200) DEFAULT null NULL ,
    `volume` INT DEFAULT null NULL ,
    `number` INT DEFAULT null NULL ,
    `month` INT DEFAULT null NULL ,
    `url` VARCHAR (200) DEFAULT null NULL ,
    `ee` VARCHAR (200) DEFAULT null NULL ,
    `publisher` VARCHAR (100) DEFAULT null NULL ,
    `journalid` INT
    ) DEFAULT CHARSET=`utf8` AUTO_INCREMENT=1;


CREATE TABLE `author_article`(
    `aaid` INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    `authorid` INT,
    `articleid` INT
    )DEFAULT CHARSET=`utf8` AUTO_INCREMENT=1;

alter table `article` add constraint `c_article_journal_FK` foreign key (`journalid`)  references `journal` (`journalid`);
alter table `author_article` add constraint `c_author_article_article_FK` foreign key (`articleid`) references `article` (`articleid`);
alter table `author_article` add constraint `c_author_article_author_FK` foreign key (`authorid`) references `author` (`authorid`);
