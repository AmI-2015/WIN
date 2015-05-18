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
-- Struttura della tabella `bagno`
--

DROP TABLE IF EXISTS `bagno`;
CREATE TABLE `bagno` (
  `id` int(11) NOT NULL,
  `numeroPersone` int(11) NOT NULL,
  `numeroGabinetti` int(11) NOT NULL,
  `stato` int(11) DEFAULT NULL,
  `gabinettiChiusi` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Struttura della tabella `distanza`
--

DROP TABLE IF EXISTS `distanza`;
CREATE TABLE `distanza` (
  `bagno` int(11) NOT NULL,
  `posto` int(11) NOT NULL,
  `priorita` int(11) NOT NULL,
  PRIMARY KEY (`bagno`,`posto`),
  KEY `posto` (`posto`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Struttura della tabella `posto`
--

DROP TABLE IF EXISTS `posto`;
CREATE TABLE `posto` (
  `id` int(11) NOT NULL,
  `nome` varchar(32) NOT NULL,
  `tipo` varchar(32) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Limiti per le tabelle scaricate
--

--
-- Limiti per la tabella `bagno`
--
ALTER TABLE `bagno`
  ADD CONSTRAINT `bagno_ibfk_1` FOREIGN KEY (`id`) REFERENCES `posto` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Limiti per la tabella `distanza`
--
ALTER TABLE `distanza`
  ADD CONSTRAINT `distanza_ibfk_2` FOREIGN KEY (`posto`) REFERENCES `posto` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `distanza_ibfk_1` FOREIGN KEY (`bagno`) REFERENCES `bagno` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;
