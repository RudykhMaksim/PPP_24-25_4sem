CREATE TABLE teachers (
    tab_number INT PRIMARY KEY,
    surname VARCHAR(50) NOT NULL,
    position VARCHAR(50),
    department VARCHAR(50),
    experience INT
);

CREATE TABLE disciplines (
    code_discipline VARCHAR(50) PRIMARY KEY,
    name_discipline VARCHAR(100) NOT NULL,
    direction VARCHAR(50)
);

CREATE TABLE load_distribution (
    tab_number INT,
    code_discipline VARCHAR(20),
    group_code VARCHAR(20),
    semester INT,
    hours INT,
    PRIMARY KEY (tab_number, code_discipline, group_code, semester),
    FOREIGN KEY (tab_number) REFERENCES teachers(tab_number),
    FOREIGN KEY (code_discipline) REFERENCES disciplines(code_discipline)
);

INSERT INTO teachers (tab_number, surname, position, department, experience) VALUES
(11, 'Ганкина', 'Доцент', 'ЭВМ', 8),
(12, 'Чичиков', 'Доцент', 'ЭВМ', 19),
(13, 'Иванов', 'Доцент', 'ЭВМ', 35),
(14, 'Орлов', NULL, 'ИФП', 12),
(15, 'Туркин', 'Доцент', 'САПР ВС', 21),
(16, 'Чебышев', 'Профессор', 'ИФП', 15),
(17, 'Цаплина', NULL, 'ВМ', 9),
(18, 'Павлушин', 'Доцент', 'САПР ВС', 2),
(19, 'Чечеткин', 'Доцент', 'САПР ВС', 5),
(20, 'Соловьев', 'Ассистент', 'САПР ВС', NULL);

INSERT INTO disciplines (code_discipline, name_discipline, direction) VALUES
(1,'Информатика', NULL),
(2,'ЭиЭ', 'Техническое'),
(3,'ИиКГ', NULL),
(4,'История', NULL),
(5,'Философия', 'Гуманитарное'),
(6,'Математический анализ', 'Математическое'),
(7,'Технологии программирования', 'Техническое'),
(8,'ПУ ЭВМ', 'Техническое'),
(9,'Операционные системы', 'Техническое'),
(10,'Базы данных', 'Техническое');

INSERT INTO load_distribution (tab_number, code_discipline, group_code, semester, hours) VALUES
(11, 7, '641', 5, 32),
(11, 10, '641', 5, 68),
(12, 9, '640', 5, 68),
(13, 1, '840', 1, 68),
(13, 1, '841', 1, 68),
(14, 4, '840', 1, 68),
(14, 4, '841', 1, 68),
(15, 3, '643', 5, 68),
(16, 5, '740', 4, 68),
(16, 5, '748', 4, 68),
(17, 6, '840', 1, 51),
(17, 6, '840', 2, 51),
(17, 6, '841', 1, 51),
(17, 6, '841', 2, 51),
(18, 2, '640', 5, 51),
(18, 2, '641', 5, 51),
(18, 2, '648', 5, 51),
(19, 3, '640', 5, 68),
(19, 3, '641', 5, 68),
(19, 8, '640', 5, 32);

drop table teachers cascade;
drop table disciplines cascade;
drop table load_distribution cascade;