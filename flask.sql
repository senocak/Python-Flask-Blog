-- phpMyAdmin SQL Dump
-- version 4.8.3
-- https://www.phpmyadmin.net/
--
-- Anamakine: 127.0.0.1
-- Üretim Zamanı: 10 Oca 2019, 08:32:38
-- Sunucu sürümü: 10.1.37-MariaDB
-- PHP Sürümü: 7.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Veritabanı: `flask`
--

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `articles`
--

CREATE TABLE `articles` (
  `id` int(11) NOT NULL,
  `title` text NOT NULL,
  `url` varchar(100) NOT NULL,
  `author` varchar(100) NOT NULL,
  `content` text NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Tablo döküm verisi `articles`
--

INSERT INTO `articles` (`id`, `title`, `url`, `author`, `content`, `created_at`) VALUES
(5, 'Lorem Ipsum1', 'lorem_ipsum1', 'asenocak', '<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ullamcorper sit amet risus nullam. Sagittis nisl rhoncus mattis rhoncus urna. Ultricies lacus sed turpis tincidunt id aliquet risus. Sit amet massa vitae tortor condimentum lacinia. Libero justo laoreet sit amet. Porttitor rhoncus dolor purus non enim praesent elementum facilisis leo. Consectetur libero id faucibus nisl tincidunt eget. Non pulvinar neque laoreet suspendisse interdum consectetur libero id. Vehicula ipsum a arcu cursus vitae congue mauris. Fermentum posuere urna nec tincidunt praesent. Vel fringilla est ullamcorper eget nulla facilisi etiam dignissim diam.</p>\r\n\r\n<p>Gravida arcu ac tortor dignissim convallis. Magna fringilla urna porttitor rhoncus dolor purus non enim praesent. Dignissim enim sit amet venenatis urna. Lacus suspendisse faucibus interdum posuere lorem ipsum. Et odio pellentesque diam volutpat commodo sed egestas egestas fringilla. At volutpat diam ut venenatis tellus in metus. Nisl vel pretium lectus quam id leo in vitae turpis. Leo integer malesuada nunc vel risus commodo viverra maecenas. Urna molestie at elementum eu facilisis sed odio morbi. Ultrices mi tempus imperdiet nulla malesuada pellentesque elit eget gravida. Purus ut faucibus pulvinar elementum integer enim neque volutpat. Posuere ac ut consequat semper viverra nam libero justo laoreet. Enim eu turpis egestas pretium aenean pharetra magna. Pharetra vel turpis nunc eget lorem dolor sed. Lorem mollis aliquam ut porttitor leo a.</p>\r\n', '2019-01-10 07:24:08');

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `username` varchar(100) NOT NULL,
  `password` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Tablo döküm verisi `users`
--

INSERT INTO `users` (`id`, `name`, `email`, `username`, `password`) VALUES
(1, 'Anil Senocak', 'anil@bilgimedya.com.tr', 'asenocak', '7d18268dd1755cd6a2b9a7f9ef32f189');

--
-- Dökümü yapılmış tablolar için indeksler
--

--
-- Tablo için indeksler `articles`
--
ALTER TABLE `articles`
  ADD PRIMARY KEY (`id`);

--
-- Tablo için indeksler `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- Dökümü yapılmış tablolar için AUTO_INCREMENT değeri
--

--
-- Tablo için AUTO_INCREMENT değeri `articles`
--
ALTER TABLE `articles`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- Tablo için AUTO_INCREMENT değeri `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
