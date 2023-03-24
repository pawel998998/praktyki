-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 23, 2023 at 10:28 AM
-- Server version: 10.4.27-MariaDB
-- PHP Version: 8.2.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `dziennik`
--

-- --------------------------------------------------------

--
-- Table structure for table `logowanie`
--

CREATE TABLE `logowanie` (
  `id` int(10) NOT NULL,
  `firstname` varchar(255) NOT NULL,
  `lastname` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `logowanie`
--

INSERT INTO `logowanie` (`id`, `firstname`, `lastname`, `email`, `password`) VALUES
(27, 'Paweł', 'Dłubała', 'pawel998998998@gmail.com', '123123'),
(28, 'Paweł', 'Dłubała', 'pawel998998998gmail.com', '123123'),
(29, 'Paweł', 'Dłubała', 'pawel998998998@gmail.co', '123123');

-- --------------------------------------------------------

--
-- Table structure for table `oceny`
--

CREATE TABLE `oceny` (
  `id` int(11) NOT NULL,
  `id_ucznia` int(11) NOT NULL,
  `id_przedmiot` int(11) NOT NULL,
  `ocena` int(11) NOT NULL,
  `typ` varchar(255) NOT NULL,
  `data` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `plan_lekcji`
--

CREATE TABLE `plan_lekcji` (
  `id` int(11) NOT NULL,
  `godziny_od` varchar(10) NOT NULL,
  `godziny_do` varchar(10) NOT NULL,
  `poniedziałek` varchar(255) NOT NULL,
  `wtorek` varchar(255) NOT NULL,
  `sroda` varchar(255) NOT NULL,
  `czwartek` varchar(255) NOT NULL,
  `piatek` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `plan_lekcji`
--

INSERT INTO `plan_lekcji` (`id`, `godziny_od`, `godziny_do`, `poniedziałek`, `wtorek`, `sroda`, `czwartek`, `piatek`) VALUES
(9123, '8:00', '8:45', 'Matematyka', 'Matematyka', 'WF', 'Niemiecki', 'Matematyka'),
(9124, '8:50', '9:35', 'WF', 'Angielski', 'Matematyka', 'Rosyjski', 'Informatyka'),
(9125, '9:45', '10:30', 'Fizyka', 'WF', 'Informatyka', 'Matematyka', 'Niemiecki'),
(9126, '10:35', '11:20', 'Informatyka', 'Biologia', 'Niemiecki', 'Angielski', 'Fizyka'),
(9127, '11:40', '12:25', 'Angielski', 'Fizyka', 'Religa', 'Biologia', 'WF'),
(9128, '12:30', '13:15', 'Rosyjski', 'Religa', 'Angielski', 'WF', 'Biologia'),
(9129, '13:25', '14:10', 'Biologia', 'Niemiecki', 'Rosyjski', 'Fizyka', 'Religa'),
(9130, '14:15', '15:00', 'Niemiecki', 'Informatyka', 'Biologia', 'Religa', 'Angielski'),
(9131, '15:05', '15:50', 'Religa', 'Rosyjski', 'Fizyka', 'Informatyka', 'Rosyjski');

-- --------------------------------------------------------

--
-- Table structure for table `przedmiot`
--

CREATE TABLE `przedmiot` (
  `id` int(11) NOT NULL,
  `nazwa` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `przedmiot`
--

INSERT INTO `przedmiot` (`id`, `nazwa`) VALUES
(1, 'Matematyka'),
(2, 'Angielski'),
(3, 'Informatyka'),
(4, 'Biologia'),
(5, 'Fizyka'),
(6, 'WF'),
(7, 'Religa'),
(8, 'Rosyjski'),
(9, 'Niemiecki');

-- --------------------------------------------------------

--
-- Table structure for table `uczen`
--

CREATE TABLE `uczen` (
  `id` int(11) NOT NULL,
  `imie` varchar(100) NOT NULL,
  `nazwisko` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `uczen`
--

INSERT INTO `uczen` (`id`, `imie`, `nazwisko`) VALUES
(2, 'Pawel', 'D');

-- --------------------------------------------------------

--
-- Table structure for table `zadania`
--

CREATE TABLE `zadania` (
  `id` int(11) NOT NULL,
  `zadanie` varchar(255) NOT NULL,
  `opis` varchar(255) NOT NULL,
  `przedmiot` varchar(255) NOT NULL,
  `data` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `zadania`
--

INSERT INTO `zadania` (`id`, `zadanie`, `opis`, `przedmiot`, `data`) VALUES
(2, 'karkowka2', 'strona 422', 'wf2', '2023-03-09');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `logowanie`
--
ALTER TABLE `logowanie`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `oceny`
--
ALTER TABLE `oceny`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_przedmiot` (`id_przedmiot`),
  ADD KEY `oceny_ibfk_2` (`id_ucznia`);

--
-- Indexes for table `plan_lekcji`
--
ALTER TABLE `plan_lekcji`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `przedmiot`
--
ALTER TABLE `przedmiot`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `uczen`
--
ALTER TABLE `uczen`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `zadania`
--
ALTER TABLE `zadania`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `logowanie`
--
ALTER TABLE `logowanie`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=30;

--
-- AUTO_INCREMENT for table `oceny`
--
ALTER TABLE `oceny`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `plan_lekcji`
--
ALTER TABLE `plan_lekcji`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9132;

--
-- AUTO_INCREMENT for table `przedmiot`
--
ALTER TABLE `przedmiot`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `uczen`
--
ALTER TABLE `uczen`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `zadania`
--
ALTER TABLE `zadania`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `oceny`
--
ALTER TABLE `oceny`
  ADD CONSTRAINT `oceny_ibfk_1` FOREIGN KEY (`id_przedmiot`) REFERENCES `przedmiot` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `oceny_ibfk_2` FOREIGN KEY (`id_ucznia`) REFERENCES `uczen` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
