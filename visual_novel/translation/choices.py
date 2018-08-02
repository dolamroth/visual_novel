# 0. shortlink for status_name, should be the same as bitfield keys in model
# 1. Status name (in Russian)
# 2. Bootstrap 3 style for text or table row
# 3. Whether user can change TranslationItem status TO this exact status by himself.
#           "False" means, that this status can be only changed TO automatically
# 4. Whether mailing should inform about changing TO this status.
# 5. Description of status for TranslationItem editing page

TRANSLATION_ITEMS_STATUSES = (
    ('active', 'Активный', 'default', True, False, 'Когда перевод активный, можно редактировать прогресс перевода.'),
    ('frozen', 'Замороженный', 'info', True, True, 'Когда перевод заморожен, редактировать прогресс перевода нельзя.'),
    ('onhold', 'Давно не обновлялся', 'warning', False, False, 'Системный статус, показывающий, что перевод давно не обновлялся. Не влияет на возможность редактирования прогресса.'),
    ('finished', 'Завершен', 'success', True, True, 'Для завершенного перевода прогресс нельзя редактировать.'),
    ('readytogo', 'Готовится к выпуску', 'success', True, False, 'Прогресс перевода нельзя будет редактировать.'),
    ('intest', 'Тестирование', 'default', True, False, 'Прогресс перевода можно будет редактировать.'),
    ('dropped', 'Заброшен', 'danger', True, True, 'Если перевод отмечен как брошенный, редактировать его нельзя.'),
)
