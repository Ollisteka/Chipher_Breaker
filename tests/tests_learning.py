#!/usr/bin/env python3
import os
import tempfile
import unittest
import logic.learner as l

OUTPUT_FILE = "output.txt"
ENCODING = "utf-8"

LETTERS = "letters"
WORDS = "words"
NGRAMMS = "ngramms"


class MyTestCase(unittest.TestCase):
    maxDiff = None

    def setUp(self):
        self.first_file = make_tmp(
            b"a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a "
            b"a a a a a a a a a a a a a a a "
            b"a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a "
            b"a a a a a a a a a a a a a a a "
            b"a a a a a a b b b b b b b b b b b b b b b b b b b b b b b b b b "
            b"b b b b b b b b b b b b b b b "
            b"b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b b "
            b"b b b b b b b b b b b b b b b "
            b"b b b b b b b b b b b b c c c c c c c c c c c c c c c c c c c c "
            b"c c c c c c c c c c c c c c c "
            b"c c c c c c c c c c c c c c c c c c c c c c c c c c c c c c c c "
            b"c c c c c c c c c c c c c c c "
            b"c c c c c c c c c c c c c c c c c c d d d d d d d d d d d d d d "
            b"d d d d d d d d d d d d d d d "
            b"d d d d d d d d d d d d d d d d d d d d d d d d d d d d d d d d "
            b"d d d d d d d d d d d d d d d "
            b"d d d d d d d d d d d d d d d d d d d d d d d d e e e e e e e e "
            b"e e e e e e e e e e e e e e e "
            b"e e e e e e e e e e e e e e e e e e e e e e e e e e e e e e e e "
            b"e e e e e e e e e e e e e e e "
            b"e e e e e e e e e e e e e e e e e e e e e e e e e e e e e e")
        self.second_file = make_tmp(
            b"z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z "
            b"z z z z z z z z z z z z z z z "
            b"z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z "
            b"z z z z z z z z z z z z z z z "
            b"z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z "
            b"z z z z z z z z z z z z z z z "
            b"z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z "
            b"z z z z z z z z z z z z z z z "
            b"z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z "
            b"z z z z z z z z z z z z z z z "
            b"z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z "
            b"z z z z z z z z z z z z z z z "
            b"z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z "
            b"z z z z z z z z z z z z z z z "
            b"z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z "
            b"z z z z z z z z z z z z z z z "
            b"z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z "
            b"z z z z z z z z z z z z z z z "
            b"z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z "
            b"z z z z z z z z z z z z z z z "
            b"z z z z z z z z z z z z z z z z z z z z z z z z z z z z z z")
        self.ngr_file = make_tmp(b"aaa abab")
        self.big_en_file = make_big_en_file()
        self.big_rus_file = make_tmp("""

        В ноябре месяце 1805 года князь Василий должен был ехать на ревизию в
        четыре губернии. Он устроил для себя это назначение с тем, чтобы
        побывать заодно в своих расстроенных имениях, и захватив с собой
        (в месте расположения его полка) сына Анатоля, с ним вместе заехать
        к князю Николаю Андреевичу Болконскому с тем, чтоб женить сына на
        дочери этого богатого старика. Но прежде отъезда и этих новых дел,
        князю Василью нужно было решить дела с Пьером, который, правда,
        последнее время проводил целые дни дома, т. е. у князя Василья, у
        которого он жил, был смешон, взволнован и глуп (как должен быть
        влюбленный) в присутствии Элен, но всё еще не делал предложения.

        «Tout ca est bel et bon, mais il faut que ca finisse», [Всё это
        хорошо, но надо это кончить,] – сказал себе раз утром князь Василий
        со вздохом грусти, сознавая, что Пьер, стольким обязанный ему (ну,
        да Христос с ним!), не совсем хорошо поступает в этом деле.
        «Молодость… легкомыслие… ну, да Бог с ним, – подумал князь Василий, с
        удовольствием чувствуя свою доброту: – mais il faut, que ca finisse.
        После завтра Лёлины именины, я позову кое-кого, и ежели он не поймет,
        что он должен сделать, то уже это будет мое дело. Да, мое дело.
        Я – отец!»

        Пьер полтора месяца после вечера Анны Павловны и последовавшей за ним
        бессонной, взволнованной ночи, в которую он решил, что женитьба на
        Элен была бы несчастие, и что ему нужно избегать ее и уехать, Пьер
        после этого решения не переезжал от князя Василья и с ужасом
        чувствовал, что каждый день он больше и больше в глазах людей
        связывается с нею, что он не может никак возвратиться к своему
        прежнему взгляду на нее, что он не может и оторваться от нее, что
        это будет ужасно, но что он должен будет связать с нею свою судьбу.
        Может быть, он и мог бы воздержаться, но не проходило дня, чтобы у
        князя Василья (у которого редко бывал прием) не было бы вечера, на
        котором должен был быть Пьер, ежели он не хотел расстроить общее
        удовольствие и обмануть ожидания всех. Князь Василий в те редкие
        минуты, когда бывал дома, проходя мимо Пьера, дергал его за руку вниз,
         рассеянно подставлял ему для поцелуя выбритую, морщинистую щеку и
         говорил или «до завтра», или «к обеду, а то я тебя не увижу», или
         «я для тебя остаюсь» и т. п. Но несмотря на то, что, когда князь
         Василий оставался для Пьера (как он это говорил), он не говорил с
         ним двух слов, Пьер не чувствовал себя в силах обмануть его ожидания.
          Он каждый день говорил себе всё одно и одно: «Надо же, наконец,
           понять ее и дать себе отчет: кто она? Ошибался ли я прежде или
           теперь ошибаюсь? Нет, она не глупа; нет, она прекрасная девушка!
           – говорил он сам себе иногда. – Никогда ни в чем она не ошибается,
           никогда она ничего не сказала глупого. Она мало говорит, но то,
           что она скажет, всегда просто и ясно. Так она не глупа. Никогда она
            не смущалась и не смущается. Так она не дурная женщина!» Часто ему
             случалось с нею начинать рассуждать, думать вслух, и всякий раз
        она отвечала ему на это либо коротким, но кстати сказанным
        замечанием, показывавшим, что ее это не интересует, либо молчаливой
        улыбкой и взглядом, которые ощутительнее всего показывали Пьеру ее
        превосходство. Она была права, признавая все рассуждения вздором в
        сравнении с этой улыбкой.

        Она обращалась к нему всегда с радостной, доверчивой, к нему одному
        относившейся улыбкой, в которой было что-то значительней того, что
        было в общей улыбке, украшавшей всегда ее лицо. Пьер знал, что все
        ждут только того, чтобы он, наконец, сказал одно слово, переступил
        через известную черту, и он знал, что он рано или поздно переступит
        через нее; но какой-то непонятный ужас охватывал его при одной мысли
        об этом страшном шаге. Тысячу раз в продолжение этого полутора месяца,
        во время которого он чувствовал себя всё дальше и дальше втягиваемым в
        ту страшившую его пропасть, Пьер говорил себе: «Да что ж это? Нужна
        решимость! Разве нет у меня ее?»

        Он хотел решиться, но с ужасом чувствовал, что не было у него в этом
        случае той решимости, которую он знал в себе и которая действительно
        была в нем. Пьер принадлежал к числу тех людей, которые сильны только
        тогда, когда они чувствуют себя вполне чистыми. А с того дня, как им
        владело то чувство желания, которое он испытал над табакеркой у Анны
        Павловны, несознанное чувство виноватости этого стремления
        парализировало его решимость.

        В день именин Элен у князя Василья ужинало маленькое общество людей
        самых близких, как говорила княгиня, родные и друзья. Всем этим родным
        и друзьям дано было чувствовать, что в этот день должна решиться участь
         именинницы.

        Гости сидели за ужином. Княгиня Курагина, массивная, когда-то
        красивая, представительная женщина сидела на хозяйском месте. По обеим
        сторонам ее сидели почетнейшие гости – старый генерал, его жена, Анна
        Павловна Шерер; в конце стола сидели менее пожилые и почетные гости, и
        там же сидели домашние, Пьер и Элен, – рядом. Князь Василий не ужинал:
        он похаживал вокруг стола, в веселом расположении духа, подсаживаясь то
         к тому, то к другому из гостей. Каждому он говорил небрежное и
         приятное слово, исключая Пьера и Элен, которых присутствия он не
         замечал, казалось. Князь Василий оживлял всех. Ярко горели восковые
         свечи, блестели серебро и хрусталь посуды, наряды дам и золото и
         серебро эполет; вокруг стола сновали слуги в красных кафтанах;
         слышались звуки ножей, стаканов, тарелок и звуки оживленного говора
         нескольких разговоров вокруг этого стола. Слышно было, как старый
         камергер в одном конце уверял старушку-баронессу в своей пламенной
         любви к ней и ее смех; с другой – рассказ о неуспехе какой-то Марьи
         Викторовны. У середины стола князь Василий сосредоточил вокруг себя
         слушателей. Он рассказывал дамам, с шутливой улыбкой на губах,
         последнее – в среду – заседание государственного совета, на котором
         был получен и читался Сергеем Кузьмичем Вязмитиновым, новым
         петербургским военным генерал-губернатором, знаменитый тогда
         рескрипт государя Александра Павловича из армии, в котором государь,
         обращаясь к Сергею Кузьмичу, говорил, что со всех сторон получает он
         заявления о преданности народа, и что заявление Петербурга особенно
         приятно ему, что он гордится честью быть главою такой нации и
         постарается быть ее достойным. Рескрипт этот начинался словами:
         Сергей Кузьмич! Со всех сторон доходят до меня слухи и т. д.

        – Так-таки и не пошло дальше, чем «Сергей Кузьмич»? – спрашивала одна
         дама.

        – Да, да, ни на волос, – отвечал смеясь князь Василий. – Сергей
         Кузьмич… со всех сторон. Со всех сторон, Сергей Кузьмич… Бедный
         Вязмитинов никак не мог пойти далее. Несколько раз он принимался
         снова за письмо, но только что скажет Сергей … всхлипывания…
         Ку…зьми…ч — слезы… и со всех сторон заглушаются рыданиями, и дальше
          он не мог. И опять платок, и опять «Сергей Кузьмич, со всех сторон»,
           и слезы… так что уже попросили прочесть другого.

        – Кузьмич… со всех сторон… и слезы… – повторил кто-то смеясь.

        – Не будьте злы, – погрозив пальцем, с другого конца стола, проговорила
         Анна Павловна, – c'est un si brave et excellent homme notre bon
         Viasmitinoff… [Это такой прекрасный человек, наш добрый Вязмитинов…]

        Все очень смеялись. На верхнем почетном конце стола все были, казалось,
         веселы и под влиянием самых различных оживленных настроений; только
         Пьер и Элен молча сидели рядом почти на нижнем конце стола; на лицах
         обоих сдерживалась сияющая улыбка, не зависящая от Сергея Кузьмича, –
         улыбка стыдливости перед своими чувствами. Что бы ни говорили и как
         бы ни смеялись и шутили другие, как бы аппетитно ни кушали и рейнвейн,
          и соте, и мороженое, как бы ни избегали взглядом эту чету, как бы ни
          казались равнодушны, невнимательны к ней, чувствовалось почему-то,
          по изредка бросаемым на них взглядам, что и анекдот о Сергее
        Кузьмиче, и смех, и кушанье – всё было притворно, а все силы внимания
         всего этого общества были обращены только на эту пару – Пьера и Элен.
        Князь Василий представлял всхлипыванья Сергея Кузьмича и в это
        время обегал взглядом дочь; и в то время как он смеялся, выражение его
        лица говорило: «Так, так, всё хорошо идет; нынче всё решится». Анна
        Павловна грозила ему за notre bon Viasmitinoff, а в глазах ее, которые
        мельком блеснули в этот момент на Пьера, князь Василий читал
        поздравление с будущим зятем и счастием дочери. Старая княгиня,
        предлагая с грустным вздохом вина своей соседке и сердито взглянув
        на дочь, этим вздохом как будто говорила: «да, теперь нам с вами
        ничего больше не осталось, как пить сладкое вино, моя милая; теперь
        время этой молодежи быть так дерзко вызывающе-счастливой». «И что за
        глупость всё то, что я рассказываю, как будто это меня интересует, –
        думал дипломат, взглядывая на счастливые лица любовников – вот это
        счастие!»

        Среди тех ничтожно-мелких, искусственных интересов, которые связывали
        это общество, попало простое чувство стремления красивых и здоровых
        молодых мужчины и женщины друг к другу. И это человеческое чувство
        подавило всё и парило над всем их искусственным лепетом. Шутки были
        невеселы, новости неинтересны, оживление – очевидно поддельно. Не
        только они, но лакеи, служившие за столом, казалось, чувствовали то
        же и забывали порядки службы, заглядываясь на красавицу Элен с ее
        сияющим лицом и на красное, толстое, счастливое и беспокойное лицо
        Пьера. Казалось, и огни свечей сосредоточены были только на этих
        двух счастливых лицах.

        Пьер чувствовал, что он был центром всего, и это положение и радовало
        и стесняло его. Он находился в состоянии человека, углубленного в
        какое-нибудь занятие. Он ничего ясно не видел, не понимал и не слыхал.
         Только изредка, неожиданно, мелькали в его душе отрывочные мысли и
         впечатления из действительности.

        «Так уж всё кончено! – думал он. – И как это всё сделалось? Так быстро!
         Теперь я знаю, что не для нее одной, не для себя одного, но и для
         всех это должно неизбежно свершиться. Они все так ждут этого, так
         уверены, что это будет, что я не могу, не могу обмануть их. Но как
         это будет? Не знаю; а будет, непременно будет!» думал Пьер,
         взглядывая на эти плечи, блестевшие подле самых глаз его.

        То вдруг ему становилось стыдно чего-то. Ему неловко было, что он один
        занимает внимание всех, что он счастливец в глазах других, что он с
        своим некрасивым лицом какой-то Парис, обладающий Еленой. «Но, верно,
        это всегда так бывает и так надо, – утешал он себя. – И, впрочем, что
        же я сделал для этого? Когда это началось? Из Москвы я поехал вместе
        с князем Васильем. Тут еще ничего не было. Потом, отчего же мне было
        у него не остановиться? Потом я играл с ней в карты и поднял ее
        ридикюль, ездил с ней кататься. Когда же это началось, когда это
        всё сделалось? И вот он сидит подле нее женихом; слышит, видит,
        чувствует ее близость, ее дыхание, ее движения, ее красоту. То вдруг
         ему кажется, что это не она, а он сам так необыкновенно красив, что
          оттого-то и смотрят так на него, и он, счастливый общим удивлением,
           выпрямляет грудь, поднимает голову и радуется своему счастью.
           Вдруг какой-то голос, чей-то знакомый голос, слышится и говорит
           ему что-то другой раз. Но Пьер так занят, что не понимает того,
           что говорят ему. – Я спрашиваю у тебя, когда ты получил письмо
        от Болконского, – повторяет третий раз князь Василий. –
        Как ты рассеян, мой милый.

        Князь Василий улыбается, и Пьер видит, что все, все улыбаются на него
        и на Элен. «Ну, что ж, коли вы все знаете», говорил сам себе Пьер. «Ну,
         что ж? это правда», и он сам улыбался своей кроткой, детской улыбкой,
          и Элен улыбается.

        – Когда же ты получил? Из Ольмюца? – повторяет князь Василий, которому
         будто нужно это знать для решения спора.

        «И можно ли говорить и думать о таких пустяках?» думает Пьер.

        – Да, из Ольмюца, – отвечает он со вздохом.

        От ужина Пьер повел свою даму за другими в гостиную. Гости стали
        разъезжаться и некоторые уезжали, не простившись с Элен. Как будто
        не желая отрывать ее от ее серьезного занятия, некоторые подходили
         на минуту и скорее отходили, запрещая ей провожать себя. Дипломат
          грустно молчал, выходя из гостиной. Ему представлялась вся тщета
           его дипломатической карьеры в сравнении с счастьем Пьера. Старый
           генерал сердито проворчал на свою жену, когда она спросила его о
            состоянии его ноги. «Эка, старая дура, – подумал он. – Вот Елена
            Васильевна так та и в 50 лет красавица будет».

        – Кажется, что я могу вас поздравить, – прошептала Анна Павловна
        княгине и крепко поцеловала ее. – Ежели бы не мигрень, я бы осталась.

        Княгиня ничего не отвечала; ее мучила зависть к счастью своей дочери.

        Пьер во время проводов гостей долго оставался один с Элен в маленькой
         гостиной, где они сели. Он часто и прежде, в последние полтора месяца,
          оставался один с Элен, но никогда не говорил ей о любви. Теперь он
          чувствовал, что это было необходимо, но он никак не мог
          решиться на этот последний шаг. Ему было стыдно;
          ему казалось, что тут, подле Элен, он занимает чье-то чужое место.
          Не для тебя это счастье, – говорил ему какой-то внутренний голос.
          – Это счастье для тех, у кого нет того, что есть у тебя. Но надо было
           сказать что-нибудь, и он заговорил. Он спросил у нее, довольна ли
            она нынешним вечером? Она, как и всегда, с простотой своей
        отвечала, что нынешние именины были для нее одними из самых приятных.

        Кое-кто из ближайших родных еще оставались. Они сидели в
        большой гостиной. Князь Василий ленивыми шагами подошел к Пьеру.
        Пьер встал и сказал, что уже поздно. Князь Василий
        строго-вопросительно посмотрел на него, как будто то, что он сказал,
         было так странно, что нельзя было и расслышать. Но вслед за тем
          выражение строгости изменилось, и князь Василий дернул Пьера
           вниз за руку, посадил его и ласково улыбнулся.

        – Ну, что, Леля? – обратился он тотчас же к дочери с тем
        небрежным тоном привычной нежности, который усвоивается родителями,
         с детства ласкающими своих детей, но который князем Василием был
          только угадан посредством подражания другим родителям.

        И он опять обратился к Пьеру.

        – Сергей Кузьмич, со всех сторон, – проговорил он, расстегивая
        верхнюю пуговицу жилета.

        Пьер улыбнулся, но по его улыбке видно было, что он понимал,
         что не анекдот Сергея Кузьмича интересовал в это время князя Василия;
          и князь Василий понял, что Пьер понимал это. Князь Василий вдруг
           пробурлил что-то и вышел. Пьеру показалось, что даже князь Василий
            был смущен. Вид смущенья этого старого светского человека тронул
            Пьера; он оглянулся на Элен – и она, казалось, была смущена и
            взглядом говорила: «что ж, вы сами виноваты».

        «Надо неизбежно перешагнуть, но не могу, я не могу», думал
         Пьер, и заговорил опять о постороннем, о Сергее Кузьмиче, спрашивая,
          в чем состоял этот анекдот, так как он его не расслышал. Элен
          с улыбкой отвечала, что она тоже не знает.

        Когда князь Василий вошел в гостиную, княгиня тихо говорила
         с пожилой дамой о Пьере.

        – Конечно, c'est un parti tres brillant, mais le bonheur, ma chere…
         – Les Marieiages se font dans les cieux, [Конечно, это очень
         блестящая партия, но счастье, моя милая… – Браки совершаются на
          небесах,] – отвечала пожилая дама.

        Князь Василий, как бы не слушая дам, прошел в дальний угол и сел на
        диван. Он закрыл глаза и как будто дремал. Голова его было упала,
         и он очнулся.

        – Aline, – сказал он жене, – allez voir ce qu'ils font. [Алина,

        посмотри, что они делают.]

        Княгиня подошла к двери, прошлась мимо нее с значительным, равнодушным
        видом и заглянула в гостиную. Пьер и Элен так же сидели и
        разговаривали.

        – Всё то же, – отвечала она мужу.

        Князь Василий нахмурился, сморщил рот на сторону, щеки его запрыгали с
         свойственным ему неприятным, грубым выражением; он, встряхнувшись,
         встал, закинул назад голову и решительными шагами, мимо дам, прошел
         в маленькую гостиную. Он скорыми шагами, радостно подошел к Пьеру.
         Лицо князя было так необыкновенно-торжественно, что Пьер испуганно
          встал, увидав его.

        – Слава Богу! – сказал он. – Жена мне всё сказала! – Он обнял одной
        рукой Пьера, другой – дочь. – Друг мой Леля! Я очень, очень рад. –
        Голос его задрожал. – Я любил твоего отца… и она будет тебе хорошая
         жена… Бог да благословит вас!…

        Он обнял дочь, потом опять Пьера и поцеловал его дурно пахучим ртом.
        Слезы, действительно, омочили его щеки.

        – Княгиня, иди же сюда, – прокричал он.

        Княгиня вышла и заплакала тоже. Пожилая дама тоже утиралась платком.
         Пьера целовали, и он несколько раз целовал руку прекрасной Элен.
          Через несколько времени их опять оставили одних.

        «Всё это так должно было быть и не могло быть иначе, – думал Пьер,
         – поэтому нечего спрашивать, хорошо ли это или дурно? Хорошо,
          потому что определенно, и нет прежнего мучительного сомнения».
          Пьер молча держал руку своей невесты и смотрел на ее поднимающуюся
          и опускающуюся прекрасную грудь.

        – Элен! – сказал он вслух и остановился.

        «Что-то такое особенное говорят в этих случаях», думал он, но никак не
         мог вспомнить, что такое именно говорят в этих случаях. Он взглянул
          в ее лицо. Она придвинулась к нему ближе. Лицо ее зарумянилось.

        – Ах, снимите эти… как эти… – она указывала на очки.

        Пьер снял очки, и глаза его сверх той общей странности глаз людей,
         снявших очки, глаза его смотрели испуганно-вопросительно. Он хотел
          нагнуться над ее рукой и поцеловать ее; но она быстрым и грубым
          движеньем головы пeрехватила его губы и свела их с своими. Лицо
    ее поразило Пьера своим изменившимся, неприятно-растерянным выражением.

        «Теперь уж поздно, всё кончено; да и я люблю ее», подумал Пьер.

        – Je vous aime! [Я вас люблю!] – сказал он, вспомнив то, что нужно
         было говорить в этих случаях; но слова эти прозвучали так бедно,
          что ему стало стыдно за себя.

        Через полтора месяца он был обвенчан и поселился, как говорили,
         счастливым обладателем красавицы-жены и миллионов, в большом
         петербургском заново отделанном доме графов Безухих.


        """.encode(ENCODING))
        self.alph_en = "A-Za-z"
        self.alph_rus = "А-Яа-яЁё"
        self.count_first = {
            LETTERS: {
                "a": 100,
                "b": 100,
                "c": 100,
                "d": 100,
                "e": 100},
            WORDS: {
                "a": 100,
                "b": 100,
                "c": 100,
                "d": 100,
                "e": 100},
            NGRAMMS: {}}
        self.frequency_first = {
            LETTERS: {
                "a": 0.2,
                "b": 0.2,
                "c": 0.2,
                "d": 0.2,
                "e": 0.2},
            WORDS: {
                "a": 0.2,
                "b": 0.2,
                "c": 0.2,
                "d": 0.2,
                "e": 0.2}}
        self.count_updated = {
            LETTERS: {
                "a": 100,
                "b": 100,
                "c": 100,
                "d": 100,
                "e": 100,
                "z": 500},
            WORDS: {
                "a": 100,
                "b": 100,
                "c": 100,
                "d": 100,
                "e": 100,
                "z": 500},
            NGRAMMS: {}}
        self.frequency_updated = {
            LETTERS: {
                "a": 0.1,
                "b": 0.1,
                "c": 0.1,
                "d": 0.1,
                "e": 0.1,
                "z": 0.5},
            WORDS: {
                "a": 0.1,
                "b": 0.1,
                "c": 0.1,
                "d": 0.1,
                "e": 0.1,
                "z": 0.5}}

    def tearDown(self):
        for file in [
                self.first_file,
                self.second_file,
                self.ngr_file,
                self.big_en_file,
                self.big_rus_file]:
            file.close()
            os.unlink(file.name)
        try:
            delete_file(OUTPUT_FILE)
        except FileNotFoundError:
            pass

    def test_file_to_update_in_wrong_lang(self):
        rus_text_info = l.TextInfo(self.alph_rus, ENCODING, self.big_rus_file)
        rus_count_info = rus_text_info.find_info(100)
        l.write_json_in_file(
            OUTPUT_FILE,
            rus_count_info.make_count_dict(),
            ENCODING)

        en_text_info = l.TextInfo(self.alph_en, ENCODING, self.first_file)
        en_count_info = en_text_info.find_info(100)
        en_count_info.update_count_info(
            OUTPUT_FILE, en_text_info.alph, 100, ENCODING)
        self.assertDictEqual(self.count_first, en_count_info.make_count_dict())

    def test_file_to_update_is_missing(self):
        text_info = l.TextInfo(self.alph_en, ENCODING, self.first_file)
        count_info = text_info.find_info(100)
        count_info.update_count_info(
            "this_file_does_not_exist",
            text_info.alph,
            100,
            ENCODING)
        self.assertDictEqual(self.count_first, count_info.make_count_dict())

    def test_change_top_words(self):
        text_info = l.TextInfo(self.alph_en, ENCODING, self.first_file)
        count_info = text_info.find_info(10)
        l.write_json_in_file(
            OUTPUT_FILE,
            count_info.make_count_dict(),
            ENCODING)

        new_text_info = l.TextInfo(self.alph_en, ENCODING, self.second_file)
        new_count_info = new_text_info.find_info(10)
        new_count_info.update_count_info(
            OUTPUT_FILE, new_text_info.alph, 3, ENCODING)

        self.assertEqual(3, len(new_count_info.words))

    def test_default_top_words(self):
        text_info = l.TextInfo(self.alph_en, ENCODING, self.big_en_file)
        count_info = text_info.find_info(None)
        self.assertEqual(100, len(count_info.words))

    def test_top_words(self):
        text_info = l.TextInfo(self.alph_en, ENCODING, self.first_file)
        count_info = text_info.find_info(3)
        self.assertEqual(3, len(count_info.words))

    def test_count_first(self):
        text_info = l.TextInfo(self.alph_en, ENCODING, self.first_file)
        count_info = text_info.find_info(100)
        count = count_info.make_count_dict()
        self.assertDictEqual(count, self.count_first)

    def test_count_frequency(self):
        text_info = l.TextInfo(self.alph_en, ENCODING, self.first_file)
        count_info = text_info.find_info(100)
        frequency = count_info.make_frequency_dict()
        self.assertDictEqual(frequency, self.frequency_first)

    def test_count_updated(self):
        text_info = l.TextInfo(self.alph_en, ENCODING, self.first_file)
        count_info = text_info.find_info(100)
        l.write_json_in_file(
            OUTPUT_FILE,
            count_info.make_count_dict(),
            ENCODING)

        new_text_info = l.TextInfo(self.alph_en, ENCODING, self.second_file)
        new_count_info = new_text_info.find_info(100)
        new_count_info.update_count_info(
            OUTPUT_FILE, new_text_info.alph, 100, ENCODING)
        updated_dict = new_count_info.make_count_dict()
        self.assertDictEqual(updated_dict, self.count_updated)

    def test__frequency_updated(self):
        text_info = l.TextInfo(self.alph_en, ENCODING, self.first_file)
        count_info = text_info.find_info(100)
        l.write_json_in_file(
            OUTPUT_FILE,
            count_info.make_count_dict(),
            ENCODING)

        new_text_info = l.TextInfo(self.alph_en, ENCODING, self.second_file)
        new_count_info = new_text_info.find_info(100)
        new_count_info.update_count_info(
            OUTPUT_FILE, new_text_info.alph, 100, ENCODING)
        frequency = new_count_info.make_frequency_dict()
        self.assertDictEqual(frequency, self.frequency_updated)

    def test_ngramms(self):
        text_info = l.TextInfo(self.alph_en, ENCODING, self.ngr_file)
        count_info = text_info.find_info(100)
        ngramms = count_info.make_ngramms_dict()
        must_be = {"2": {"aa": 2, "ab": 2, "ba": 1},
                   "3": {"aaa": 1, "aba": 1, "bab": 1},
                   "4": {"abab": 1}}
        self.assertDictEqual(must_be, ngramms)


def delete_file(filename):
    """
    Delete file from current directory
    :param filename:
    :return:
    """
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), filename)
    os.remove(path)


def make_tmp(text):
    """
    Make a temp file from a given text.
    :param text:
    :return:
    """
    tmp = tempfile.NamedTemporaryFile(delete=False)
    tmp.write(text)
    return tmp


def make_big_en_file():
    """
    Generate temp file with Harry Potter text
    :return:
    """
    return make_tmp(""" Harry Potter and the Sorcerer's Stone



For Jessica, who loves stories,
For Anne, who loved them too;
And for Di, who heard this one first.





1. THE BOY WHO LIVED


Mr. and Mrs. Dursley, of number four, Privet Drive, were proud to say that
 they were perfectly normal, thank you very much. They were the last people
  you'd expect to be involved in anything strange or mysterious, because they
   just didn't hold with such nonsense.
Mr. Dursley was the director of a firm called Grunnings, which made drills.
 He was a big, beefy man with hardly any neck, although he did have a very
  large mustache. Mrs. Dursley was thin and blonde and had nearly twice the
usual amount of neck, which came in very useful as she spent so much of her
 time craning over garden fences, spying on the neighbors. The Dursleys had
  a small son called Dudley and in their opinion there was no finer boy
  anywhere.
The Dursleys had everything they wanted, but they also had a secret, and their
 greatest fear was that somebody would discover it. They didn't think they
could bear it if anyone found out about the Potters. Mrs. Potter was Mrs.
Dursley's sister, but they hadn't met for several years; in fact,
Mrs. Dursley pretended she didn't have a sister, because her sister and
her good for nothing husband were as unDursleyish as it was possible
to be. The Dursleys shuddered to think what the neighbors would say if the
Potters arrived in the street. The Dursleys knew that the Potters had a small
son, too, but they had never even seen him. This boy was another good reason
for keeping the Potters away; they didn't want Dudley mixing with a child like
that.
When Mr. and Mrs. Dursley woke up on the dull, gray Tuesday our story starts,
 there was nothing about the cloudy sky outside to suggest that strange
and mysterious things would soon be happening all over the country.
Mr. Dursley hummed as he picked out his most boring tie for work, and Mrs.
Dursley gossiped away happily as she wrestled a screaming Dudley into his
high chair.
None of them noticed a large, tawny owl flutter past the window.
At half past eight, Mr. Dursley picked up his briefcase, pecked Mrs. Dursley
 on the cheek, and tried to kiss Dudley good bye but missed, because Dudley
 was now having a tantrum and throwing his cereal at the walls.
“Little tyke,” chortled Mr. Dursley as he left the house. He got into his car
 and backed out of number four's drive.
It was on the corner of the street that he noticed the first sign of something
 peculiar—a cat reading a map. For a second, Mr. Dursley didn't realize what
 he had seen—then he jerked his head around to look again. There was a tabby
 cat standing on the corner of Privet Drive, but there wasn't a map in sight.
 What could he have been thinking of? It must have been a trick of the light.
 Mr. Dursley blinked and stared at the cat. It stared back. As Mr. Dursley
 drove around the corner and up the road, he watched the cat in his mirror.
 It was now reading the sign that said Privet Drive—no, looking at the sign;
 cats couldn't read maps or signs. Mr. Dursley gave himself a little shake and
 put the cat out of his mind. As he drove toward town he thought of nothing
 except a large order of drills he was hoping to get that day.
But on the edge of town, drills were driven out of his mind by something else.
 As he sat in the usual morning traffic jam, he couldn't help noticing that
 there seemed to be a lot of strangely dressed people about. People in cloaks.
Mr. Dursley couldn't bear people who dressed in funny clothes—the getups you
saw on young people! He supposed this was some stupid new fashion. He drummed
his fingers on the steering wheel and his eyes fell on a huddle of these
weirdos standing quite close by. They were whispering excitedly together.
Mr. Dursley was enraged to see that a couple of them weren't young at all; why,
that man had to be older than he was, and wearing an emerald green cloak! The
nerve of him! But then it struck Mr. Dursley that this was probably some silly
stunt—these people were obviously collecting for something… yes, that would
be it. The traffic moved on and a few minutes later, Mr. Dursley arrived in the
 Grunnings parking lot, his mind back on drills.
Mr. Dursley always sat with his back to the window in his office on the ninth
floor. If he hadn't, he might have found it harder to concentrate on drills
that morning. He didn't see the owls swooping past in broad daylight, though
people down in the street did; they pointed and gazed open-mouthed as owl after
owl sped overhead. Most of them had never seen an owl even at nighttime.
Mr. Dursley, however, had a perfectly normal, owl free morning. He yelled at
five different people. He made several important telephone calls and shouted a
bit more. He was in a very good mood until lunchtime, when he thought he'd
stretch his legs and walk across the road to buy himself a bun from the bakery.
He'd forgotten all about the people in cloaks until he passed a group of them
next to the baker's. He eyed them angrily as he passed. He didn't know why,
but they made him uneasy. This bunch were whispering excitedly, too, and he
 couldn't see a single collecting tin. It was on his way back past them,
 clutching a large doughnut in a bag, that he caught a few words of what
 they were saying.
“The Potters, that's right, that's what I heard—”
“—yes, their son, Harry—”
Mr. Dursley stopped dead. Fear flooded him. He looked back at the whisperers
 as if he wanted to say something to them, but thought better of it.
He dashed back across the road, hurried up to his office, snapped at his
 secretary not to disturb him, seized his telephone, and had almost finished
dialing his home number when he changed his mind. He put the receiver back
down and stroked his mustache, thinking… no, he was being stupid. Potter wasn't
 such an unusual name. He was sure there were lots of people called Potter who
 had a son called Harry. Come to think of it, he wasn't even sure his nephew
 was called Harry. He'd never even seen the boy. It might have been Harvey. Or
 Harold. There was no point in worrying Mrs. Dursley; she always got so upset
 at any mention of her sister. He didn't blame her—if he'd had a sister like
 that… but all the same, those people in cloaks…
He found it a lot harder to concentrate on drills that afternoon and when he
 left the building at five o'clock, he was still so worried that he walked
 straight into someone just outside the door.
“Sorry,” he grunted, as the tiny old man stumbled and almost fell. It was a
 few seconds before Mr. Dursley realized that the man was wearing a violet
  cloak. He didn't seem at all upset at being almost knocked to the ground.
On the contrary, his face split into a wide smile and he said in a squeaky
voice that made passersby stare, “Don't be sorry, my dear sir, for nothing
could upset me today! Rejoice, for You-Know-Who has gone at last! Even Muggles
like yourself should be celebrating, this happy, happy day!”
And the old man hugged Mr. Dursley around the middle and walked off.
Mr. Dursley stood rooted to the spot. He had been hugged by a complete
stranger. He also thought he had been called a Muggle, whatever that was.
He was rattled. He hurried to his car and set off for home, hoping he was
imagining things, which he had never hoped before, because he didn't approve
of imagination.
As he pulled into the driveway of number four, the first thing he saw—and it
didn't improve his mood—was the tabby cat he'd spotted that morning. It was now
 sitting on his garden wall. He was sure it was the same one; it had the same
 markings around its eyes.
“Shoo!” said Mr. Dursley loudly.
The cat didn't move. It just gave him a stern look. Was this normal cat
behavior? Mr. Dursley wondered. Trying to pull himself together, he let himself
into the house. He was still determined not to mention anything to his wife.
Mrs. Dursley had had a nice, normal day. She told him over dinner all about
Mrs. Next Door's problems with her daughter and how Dudley had learned a new
word (“Won't!”). Mr. Dursley tried to act normally. When Dudley had been put
to bed, he went into the living room in time to catch the last report on the
 evening news:
“And finally, bird watchers everywhere have reported that the nation's owls
have been behaving very unusually today. Although owls normally hunt at night
and are hardly ever seen in daylight, there have been hundreds of sightings of
these birds flying in every direction since sunrise. Experts are unable to
explain why the owls have suddenly changed their sleeping pattern.”
The newscaster allowed himself a grin. “Most mysterious. And now, over to Jim
McGuffin with the weather. Going to be any more showers of owls tonight, Jim?”
“Well, Ted,” said the weatherman, “I don't know about that, but it's not only
the owls that have been acting oddly today. Viewers as far apart as Kent,
Yorkshire, and Dundee have been phoning in to tell me that instead of the
rain I promised yesterday, they've had a downpour of shooting stars! Perhaps
people have been celebrating Bonfire Night early—it's not until next week,
folks! But I can promise a wet night tonight.”
Mr. Dursley sat frozen in his armchair. Shooting stars all over Britain? Owls
flying by daylight? Mysterious people in cloaks all over the place? And a
whisper, a whisper about the Potters…
Mrs. Dursley came into the living room carrying two cups of tea. It was no
good. He'd have to say something to her. He cleared his throat nervously.
“Er—Petunia, dear—you haven't heard from your sister lately, have you?”
As he had expected, Mrs. Dursley looked shocked and angry. After all, they
normally pretended she didn't have a sister.
“No,” she said sharply. “Why?”
“Funny stuff on the news,” Mr. Dursley mumbled. “Owls… shooting stars… and
 there were a lot of funny looking people in town today…”
“So?” snapped Mrs. Dursley.
“Well, I just thought… maybe… it was something to do with… you know… her
 crowd.”
Mrs. Dursley sipped her tea through pursed lips. Mr. Dursley wondered whether
 he dared tell her he'd heard the name “Potter.” He decided he didn't dare.
  Instead he said, as casually as he could, “Their son—he'd be about Dudley's
   age now, wouldn't he?”
“I suppose so,” said Mrs. Dursley stiffly.
“What's his name again? Howard, isn't it?”
“Harry. Nasty, common name, if you ask me.“""".encode(ENCODING))


if __name__ == '__main__':
    unittest.main()
