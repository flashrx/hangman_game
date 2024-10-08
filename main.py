from random import choice
from time import sleep, time


def pause() -> None:
    continue_or_quit = input('Нажми любую клавишу для продолжения, либо [q], чтобы выйти из игры... ')
    if continue_or_quit == 'q':
        exit()


def print_titles(title_num: int) -> None:
    if title_num < 6:
        title = ['ДОБРО ПОЖАЛОВАТЬ В ИГРУ УГАДАЙКА СЛОВ!', 'ЗАПУСК ИГРЫ', 'ПРАВИЛА', 'СТАТИСТИКА', 'НАСТРОЙКИ',
                 'РАЗРАБОТЧИКИ', ''][title_num]
        print(title)
        sleep(0.5)
        print('∼' * len(title))
        sleep(0.5)


def developers() -> None:
    print('Учебный проект курса "Поколение Python: курс для начинающих".\nПрограммист: Никонов А.\n')
    pause()


def rules() -> None:
    print('''1. Программа загадывает случайное слово, а игрок должен его угадать за 7 попыток. Изначально все буквы 
слова неизвестны. Также рисуется виселица с петлёй. 
2. Игрок предлагает букву, которая может входить в это слово. Если такая буква есть в слове, то программа подставляет 
её столько раз, сколько она встречается в слове. Если такой буквы нет, то отнимается одна попытка, а к виселице 
добавляется очередная часть тела висельника. Игрок продолжает отгадывать буквы до тех пор, пока не отгадает слово, либо 
не исчерпает все попытки. 
3. За одну попытку можно назвать либо одну букву, либо слово целиком. Пытаться угадывать по несколько букв за раз 
нельзя - это будет зачтено как попытка угадать целое слово, соответственно попытка будет потеряна впустую.
''')
    pause()


def statistics() -> None:
    try:
        print(f'⎔ Победы:     {wins_count} ({wins_count / total_games * 100}%)')
        print(f'⎔ Поражения:  {loses_count} ({loses_count / total_games * 100}%)')
        print(f'⎔ Время:      {round(total_time / 60, 1)} минут')
        print(f'⎔ Слова:      {stat_dict}')
        print()
    except ZeroDivisionError:
        print('Статистика недоступна, так как не было сыграно ни одной игры.\n')
    pause()


def settings():
    global options
    while 'НАСТРОЙКИ':
        choose_setting = input('[1] Длина загадываемых слов\n[2] Символ скрытых букв\n[3] Главное меню\n')
        if choose_setting == '1':
            while 'РЕГУЛИРУЕМ ДЛИНУ СЛОВА':
                try:
                    min_l, max_l = map(int, input('Укажи минимальную и максимальную длину загадываемых слов (два '
                                                  'целых числа через пробел): ').split())
                    if min_l > 1 and max_l > 1:
                        options['min_l'] = min_l
                        options['max_l'] = max_l
                        break
                    print('Минимальная и максимальная длина слова должна быть больше 1 символа.')
                except ValueError:
                    print('Некорректный ввод. Это точно два целых числа через пробел?')
        elif choose_setting == '2':
            mask_symbol = input('Укажи символ, обозначающий неразгаданные буквы в слове: ')
            while 'ВЫБИРАЕМ СИМВОЛ ДЛЯ СКРЫТЫХ БУКВ':
                if len(mask_symbol) == 1 and not mask_symbol.isalnum() and not mask_symbol.isspace():
                    options['mask_symbol'] = mask_symbol
                    break
                mask_symbol = input('Символ не должен быть буквой, цифрой, пустой строкой или пробелом: ')
        elif choose_setting == '3':
            return 'quit'


def display_hangman(hidden_word: str, tries: int) -> str:
    stages = [
        '''
┏━━━━━━┓    ☁～～～～☁～～～～☀～～～～☁～～～～☁
┃      ╿    ⎔ Загаданное слово: {}
┃     ℺
┃   ╭╴╶╮
┃     Ų
┃   <╯ ╰>   ⎔ Осталось попыток: {}
┻═══════════════════════════════════════════
        ''',
        '''
┏━━━━━━┓    ☁～～～～☁～～～～☀～～～～☁～～～～☁
┃      ╿    ⎔ Загаданное слово: {}
┃     ℺
┃   ╭╴╶╮
┃     Ų
┃   <╯      ⎔ Осталось попыток: {}
┻═══════════════════════════════════════════
        ''',
        '''
┏━━━━━━┓    ☁～～～～☁～～～～☀～～～～☁～～～～☁
┃      ╿    ⎔ Загаданное слово: {}
┃     ℺
┃   ╭╴╶╮
┃     Ų
┃           ⎔ Осталось попыток: {}
┻═══════════════════════════════════════════
        ''',
        '''
┏━━━━━━┓    ☁～～～～☁～～～～☀～～～～☁～～～～☁
┃      ╿    ⎔ Загаданное слово: {}
┃     ℺
┃   ╭╴╶╮
┃     
┃           ⎔ Осталось попыток: {}
┻═══════════════════════════════════════════
        ''',
        '''
┏━━━━━━┓    ☁～～～～☁～～～～☀～～～～☁～～～～☁
┃      ╿    ⎔ Загаданное слово: {}
┃     ℺
┃   ╭╴
┃     
┃           ⎔ Осталось попыток: {}
┻═══════════════════════════════════════════
        ''',
        '''
┏━━━━━━┓    ☁～～～～☁～～～～☀～～～～☁～～～～☁
┃      ╿    ⎔ Загаданное слово: {}
┃     ℺
┃     
┃     
┃           ⎔ Осталось попыток: {}
┻═══════════════════════════════════════════
        ''',
        '''
┏━━━━━━┓    ☁～～～～☁～～～～☀～～～～☁～～～～☁
┃      ╿    ⎔ Загаданное слово: {}
┃     ℺    
┃   
┃     
┃           ⎔ Осталось попыток: {}
┻═══════════════════════════════════════════
        ''',
        '''
┏━━━━━━┓    ☁～～～～☁～～～～☀～～～～☁～～～～☁
┃      ╿    ⎔ Загаданное слово: {}
┃           
┃           
┃           
┃           ⎔ Осталось попыток: {}
┻═══════════════════════════════════════════
        '''
    ]
    return stages[tries].format(hidden_word, tries)


def is_valid(attempt: str) -> str:
    phrases = [
        '"Не понимать", - всплеснул руками знаток языков Ху Ли Ган, китаец по батюшке. "Ну и, Ху Ли?" - прищурился '
        'каратель, ожидая ответа то ли от китайца, то ли от тебя...',
        '"Ба! Иностранец?" - выпучил глаза сутулый дед в кафтане "ВерьСанчо" и перекрестился. Толпа зароптала, а '
        'палач, хрустнув шеей, злобно оглянулся на тебя...']
    while not set(attempt).issubset('АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'):
        print(choice(phrases))
        attempt = input('Кажется, с ними шутки плохи, надо играть по правилам: ').upper()
    return attempt


def get_word(min_l: int, max_l: int) -> str:
    try:
        with open("words.txt", encoding='utf-8') as file:
            words = [word.rstrip() for word in file.readlines() if min_l + 1 <= len(word) <= max_l + 1]
            return choice(words).upper()
    except IndexError:
        exit(f'В файле "words.txt" не найдено ни одного слова длиной от {min_l} до {max_l} символов!')
    except FileNotFoundError:
        exit('Файл "words.txt" не найден в каталоге программы.')


def play() -> None:
    word = get_word(options.get('min_l', 2), options.get('max_l', 25))
    attempts_dict, attempts_counter, tries_left, result = {}, 0, 7, False
    hidden_word = options.get('mask_symbol', '*') * len(word)
    print('''Агрессивная толпа окружила эшафот. Дожёвывая последние краюхи хлеба и изрыгая нецензурную брань беззубыми 
ртами, люди требовали жестоких зрелищ. Ты приходишь в сознание от мерзкого, леденящего душу ощущения сдавленности 
и обречённости - похоже, петлю уже накинули. Сквозь неуёмный гул, словно разрезая пространство, прозвучал вопрос о 
твоём последнем желании перед казнью. Мысли судорожно перемешивались в кучу от нахлынувшего ужаса, но впрочем, 
думать было некогда. "Сыграй в УГАДАЙКУ!" - неожиданно выкрикнул странно одетый незнакомец, неявно выделяющийся 
из окружающей серой массы, - от него будто веяло аурой света и надежды. Палач усмехнулся, а толпа притихла...
''')
    pause()
    s_time = time()
    while 'ИГРАЕМ В УГАДАЙКУ':
        print(display_hangman(word if result else hidden_word, tries_left))
        if result:
            break
        attempt = is_valid(input('"Назови букву или слово целиком" - прошипела фигура в маске, подтягивая верёвку. '
                                 'Петля сдавливает горло всё сильнее, медлить нельзя: ').upper())
        while attempt in attempts_dict:
            print(f'"Было, тупица!" - загудели буйные головы в толпе, выкрикивая предыдущие попытки: {attempts_dict}')
            attempt = is_valid(input('Кажется, пора собраться с мыслями и назвать что-то другое: ').upper())
        attempts_counter += 1
        attempts_dict[attempt] = attempts_counter
        if len(attempt) == 1:
            hidden_word = ''.join(c if c in attempts_dict else options.get('mask_symbol', '*') for c in word)
        if attempt not in word and attempt != word:
            tries_left -= 1
        if attempt == word or hidden_word == word:
            result = 'win'
        elif not tries_left:
            result = 'lose'
    timer = round(time() - s_time)
    if result == 'lose':
        global loses_count
        loses_count += 1
        print('Потрачено!')
        sleep(2)
        print(f'Разъярённая толпа в течение {timer} сек. припомнила все твои попытки: {attempts_dict}')
        sleep(2)
        print(f'Палач покачал головой и угрюмо вздёрнул болтающееся в петле тело, бормоча под нос лишь слово '
              f'{word}...\n')
    elif result == 'win':
        global wins_count
        wins_count += 1
        print('Угадано!')
        sleep(2)
        print(f'Ангел-хранитель в течение {timer} сек. благословил все твои попытки: {attempts_dict}')
        sleep(2)
        print(f'Верёвка неожиданно рвётся! Ты ловко скидываешь с шеи петлю и со всех ног бросаешься наутёк, сдавленно '
              f'прохрипев лишь слово {word}...\n')
    global total_games, stat_dict, total_time
    stat_dict[word] = ('Потрачено!', 'Угадано!')[result == 'win']
    total_games += 1
    total_time += timer
    pause()


options = {'min_l': 2, 'max_l': 25, 'mask_symbol': '▢'}
stat_dict, total_games, wins_count, loses_count, total_time = {}, 0, 0, 0, 0
while 'ГЛАВНОЕ МЕНЮ':
    menu = ('', 'play', 'rules', 'statistics', 'settings', 'developers', 'exit')
    print_titles(0)
    answer = input('[1] Новая игра\n[2] Правила\n[3] Статистика\n[4] Настройки\n[5] Разработчики\n''[6] Выход\n')
    if answer in ('1', '2', '3', '4', '5', '6'):
        print_titles(int(answer))
        eval(menu[int(answer)] + '()')
    else:
        print('Некорректный ввод. Возвращаемся в главное меню.\n')
