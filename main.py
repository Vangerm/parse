import regard.parser as regard

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


while True:
    inp = input('Что выгружаем?\n')
    if inp == 'break':
        break
    elif inp == 'regard':
        # regard.discharge_categories(categories_name=categories_name)
        regard.load_categories()
