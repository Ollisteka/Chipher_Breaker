﻿Взлом шифров.
---
Версия 1.2
Автор: Жукова Ольга (zhukova.o.m@yandex.ru)
---
В данной программе будет реализована возможность взломать любой подстановочный шифр.
---

LEARNING
----
Программа позволяет посчитать частоту символов в документе, наиболее часто встречающиеся слова,а также популярные n-граммыю
----
Консольная версия

Справка по запуску:
    Windows: python learn.py --help
    Linux: python3 learn.py --help
Пример запуска: python learn.py A-Za-z input.txt
----

ENCRYPTOR
----
Программа позволяет зашифровать текст, используя указанный или сгенерированный подстановочный шифр.
----
Консольная версия

Справка по запуску:
    Windows: python encrypt.py --help
    Linux: python3 encrypt.py --help
Пример запуска: python encrypt.py -s subst.txt A-Za-z input.txt

ДЛЯ ДЕШИФРОВКИ (необходимо иметь использованную для шифровки подстановку):
    Windows: python encrypt.py -r subst.txt A-Za-z code.txt
    Linux: python3 encrypt.py -r subst.txt A-Za-z code.txt

!!! Не поддерживается Pipe, так как команды не выполняются последовательно, а во второй команде требуется подстановка, которая может быть даже не была ещё сгенерирована

----

DECRYPTOR
----
Программа позволяет расшифровать текст, закодированный с помощью подстановочного шифра.
----
Консольная версия

Справка по запуску:
    Windows: python decrypt.py --help
    Linux: python3 decrypt.py --help
Пример запуска: python decrypt.py A-Za-z stat.txt input.txt
----
Алгоритм декодирования:

К любому слову строим маску по следущему принципу: первая буква заменяется на 0, каждая следующая - на 1 больше, если
ранее в слове не встречалась, иначе - такой же номер, как и у той, одинаковой буквы (hello - 01223; abcabc-012012).
Составляем словарь со статистикой для закодированного текста, затем берем по N слов каждой длины и строим для них маски.
Используя оригинальный словарь со статистикой, также строим маски для слов.
Получили два словаря, попарно сравниваем маски из каждого.
На каждой итерации получаем возможную подстановку. Объединяем её с предыдущей, оставляя только совпадающие буквы.
Если данной маске зашифрованного слова не соответствует ни одно слово из словаря, можно не обращать на это внимания,так
как возможны 2 варианта:
    a) такие случаи редки и, когда мы построим таблицу соответствия, расшифровав другие слова, мы однозначно заменим буквы и в этом слове
    б) текст состоит из уникальных слов, которые редко употребляются и нашей статистики не хватает для дешифрации
В конце концов оставляем лишь те буквы, которые можно расшифровать однозначно, остальные заменяем на "_"

Алгоритм подбора возможных подстановок:

Посчитаем вероятность появления каждой квадрагаммы в тексте,  используя данные, полученные с помощью learn.py. Затем, чтобы
посчитать вероятность того, что закодированный текст является раскодированным - выделим все квадграммы из него и перемножим
вероятности каждой из них. Чем выше полученное число - тем более вероятно, что этот текст - раскодирован.
