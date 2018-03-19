ru_months_in = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
                'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']


def printable_russian_date(date):
    return str(date.day) + ' ' + ru_months_in[date.month - 1] + ' ' + str(date.year) + ' года'
