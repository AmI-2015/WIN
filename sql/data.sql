DELETE FROM `place` WHERE `id` >= 1 AND `id` <= 4;
INSERT INTO `place` (`id`, `name`, `type`) VALUES
(1, 'Classroom 12', 'classroom'),
(2, 'Studyroom nord', 'studyroom'),
(3, 'Restroom nord', 'restroom'),
(4, 'Restroom east', 'restroom');
