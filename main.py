from parser.parser import Parser

categories_name = (
    'процессоры',
    'материнские платы',
    'видеокарты',
    'оперативная память',
    'блоки питания',
    'корпуса',
    'жёсткие диски',
    'накопители ssd',
    'системы охлаждения',
    'системы охлаждения процессора',
    'ssd накопители'
    )

if __name__ == '__main__':
    parser = Parser()

    url = "https://www.pc4you.ru/"

    parser.discharge_categories(url, "section", categories_name=categories_name)
