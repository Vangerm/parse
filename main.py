import regard

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
        inp = input('Какой раздел?\n').lower()
        if inp == 'все':
            regard.discharge_categories(categories_name=categories_name)
            regard.load_categories()
        elif inp in categories_name:
            category_href = regard.open_json_file()[inp]
            regard.discharge_category(category_name=inp, category_href=category_href)