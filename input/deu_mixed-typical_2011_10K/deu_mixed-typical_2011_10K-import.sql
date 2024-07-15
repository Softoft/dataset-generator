CREATE DATABASE `deu_mixed-typical_2011_10K`;

USE deu_mixed-typical_2011_10K;

CREATE TABLE `words` (
  `w_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `word` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `freq` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`w_id`),
  KEY `word` (`word`),
  KEY `w_id` (`w_id`)
) ENGINE=MyISAM AUTO_INCREMENT=20493 DEFAULT CHARSET=utf8;

CREATE TABLE `sentences` (
  `s_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `sentence` text,
  KEY `s_id` (`s_id`)
) ENGINE=MyISAM AUTO_INCREMENT=10001 DEFAULT CHARSET=utf8;

CREATE TABLE `co_s` (
  `w1_id` int(10) unsigned NOT NULL DEFAULT '0',
  `w2_id` int(10) unsigned NOT NULL DEFAULT '0',
  `freq` int(8) unsigned DEFAULT NULL,
  `sig` float DEFAULT NULL,
  PRIMARY KEY (`w1_id`,`w2_id`),
  KEY `w1_sig` (`w1_id`,`sig`),
  KEY `w2_sig` (`w2_id`,`sig`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

CREATE TABLE `co_n` (
  `w1_id` int(10) unsigned NOT NULL DEFAULT '0',
  `w2_id` int(10) unsigned NOT NULL DEFAULT '0',
  `freq` int(8) unsigned DEFAULT NULL,
  `sig` float DEFAULT NULL,
  PRIMARY KEY (`w1_id`,`w2_id`),
  KEY `w1_sig` (`w1_id`,`sig`),
  KEY `w2_sig` (`w2_id`,`sig`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

CREATE TABLE `inv_w` (
  `w_id` int(10) unsigned NOT NULL DEFAULT '0',
  `s_id` int(10) unsigned NOT NULL DEFAULT '0',
  `pos` mediumint(2) unsigned NOT NULL DEFAULT '0',
  KEY `w_id` (`w_id`),
  KEY `s_id` (`s_id`),
  KEY `w_s` (`w_id`,`s_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

CREATE TABLE `inv_so` (
  `so_id` int(10) unsigned NOT NULL DEFAULT '0',
  `s_id` int(10) unsigned NOT NULL DEFAULT '0',
  KEY `s_id` (`s_id`),
  KEY `so_id` (`so_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

CREATE TABLE `sources` (
  `so_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `source` varchar(255) DEFAULT NULL,
  `date` date DEFAULT NULL,
  KEY `so_id` (`so_id`),
  KEY `date` (`date`)
) ENGINE=MyISAM AUTO_INCREMENT=8992 DEFAULT CHARSET=utf8;

ALTER TABLE `words` DISABLE KEYS;
ALTER TABLE `sentences` DISABLE KEYS;
ALTER TABLE `co_s` DISABLE KEYS;
ALTER TABLE `co_n` DISABLE KEYS;
ALTER TABLE `inv_w` DISABLE KEYS;
ALTER TABLE `inv_so` DISABLE KEYS;
ALTER TABLE `sources` DISABLE KEYS;

LOAD DATA LOCAL INFILE 'deu_mixed-typical_2011_10K-words.txt' INTO TABLE words;
LOAD DATA LOCAL INFILE 'deu_mixed-typical_2011_10K-sentences.txt' INTO TABLE sentences;
LOAD DATA LOCAL INFILE 'deu_mixed-typical_2011_10K-co_s.txt' INTO TABLE co_s;
LOAD DATA LOCAL INFILE 'deu_mixed-typical_2011_10K-co_n.txt' INTO TABLE co_n;
LOAD DATA LOCAL INFILE 'deu_mixed-typical_2011_10K-inv_w.txt' INTO TABLE inv_w;
LOAD DATA LOCAL INFILE 'deu_mixed-typical_2011_10K-inv_so.txt' INTO TABLE inv_so;
LOAD DATA LOCAL INFILE 'deu_mixed-typical_2011_10K-sources.txt' INTO TABLE sources;

ALTER TABLE `words` ENABLE KEYS;
ALTER TABLE `sentences` ENABLE KEYS;
ALTER TABLE `co_s` ENABLE KEYS;
ALTER TABLE `co_n` ENABLE KEYS;
ALTER TABLE `inv_w` ENABLE KEYS;
ALTER TABLE `inv_so` ENABLE KEYS;
ALTER TABLE `sources` ENABLE KEYS;