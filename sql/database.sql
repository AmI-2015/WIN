-- phpMyAdmin SQL Dump
-- version 4.1.12
-- http://www.phpmyadmin.net
--
-- Host: localhost:8889
-- Generation Time: Mag 18, 2015 alle 18:34
-- Versione del server: 5.5.34-log
-- PHP Version: 5.5.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

--
-- Database: `win`
--

-- --------------------------------------------------------

--
-- Struttura della tabella `distance`
--

DROP TABLE IF EXISTS `distance`;
CREATE TABLE `distance` (
  `restroom` int(11) NOT NULL,
  `place` int(11) NOT NULL,
  `priority` int(11) NOT NULL,
  PRIMARY KEY (`restroom`,`place`),
  KEY `place` (`place`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Struttura della tabella `restroom`
--
-- lo 0 in status indica bagno aperto
-- wc_count indica il numero di toilet in quel bagno

DROP TABLE IF EXISTS `restroom`;
CREATE TABLE `restroom` (
  `id` int(11) NOT NULL,
  `people_count` int(11) NOT NULL DEFAULT 0,
  `wc_count` int(11) NOT NULL,
  `gender` char(2) NOT NULL,
  `status` int(11) DEFAULT 0,  
  `wc_closed_count` int(11) DEFAULT 0,
  `lat` double NOT NULL,
  `long` double NOT NULL,
  `waiting_time` char(5) NOT NULL DEFAULT '00:00'
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Struttura della tabella `place`
--

DROP TABLE IF EXISTS `place`;
CREATE TABLE `place` (
  `id` int(11) NOT NULL,
  `name` varchar(32) NOT NULL,
  `typeit` varchar(32) NOT NULL,
  `type` varchar(32) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Limiti per le tabelle scaricate
--

--
-- Limiti per la tabella `restroom`
--
ALTER TABLE `restroom`
  ADD CONSTRAINT `restroom_ibfk_1` FOREIGN KEY (`id`) REFERENCES `place` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Limiti per la tabella `distance`
--
ALTER TABLE `distance`
  ADD CONSTRAINT `distance_ibfk_2` FOREIGN KEY (`place`) REFERENCES `place` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `distance_ibfk_1` FOREIGN KEY (`restroom`) REFERENCES `restroom` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;
