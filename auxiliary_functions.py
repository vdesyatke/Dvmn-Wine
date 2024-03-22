def decline_years(years):
    """Функция принимает число лет и возвращает строку вида
     'число лет' с правильным склонением"""

    if years > 10 and str(years)[-2:] in ('11', '12', '13', '14'):
        return f'{years} лет'
    elif str(years)[-1:] == '1':
        return f'{years} год'
    elif str(years)[-1:] in ('2', '3', '4'):
        return f'{years} года'
    else:
        return f'{years} лет'
