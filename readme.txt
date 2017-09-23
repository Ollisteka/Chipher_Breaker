Взлом шифров.
---
Версия 1.0
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
Пример запуска: python decrypt.py A-Za-z input.txt
----