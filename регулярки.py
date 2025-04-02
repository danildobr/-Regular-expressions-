import re
from pprint import pprint
import csv

def fix_names(contacts_list):
    '''Функция для разделения ФИО на отдельные поля (lastname, firstname, surname)
    
    Обрабатывает первые три элемента каждой записи, объединяет их в строку,
    затем разделяет по пробелам и распределяет по полям:
    - Первое слово -> фамилия (lastname)
    - Второе слово -> имя (firstname)
    - Третье слово -> отчество (surname)
    '''
    for contact in contacts_list[1:]:  # Пропускаем заголовок таблицы
        # Объединяем первые 3 поля и разбиваем по пробелам
        name_parts = ' '.join(contact[:3]).split()
        # Добавляем пустые строки, если элементов меньше 3
        name_parts += [''] * (3 - len(name_parts))
        # Записываем фамилию, имя и отчество в соответствующие поля
        contact[0], contact[1], contact[2] = name_parts[:3]

def fix_phones(contacts_list):
    '''Функция для приведения телефонов к единому формату
    
    Преобразует все номера телефонов к формату:
    - Основной номер: +7(999)999-99-99
    - С добавочным номером: +7(999)999-99-99 доб.9999
    '''
    phone_pattern = re.compile(
        r'(\+7|8)\s*\(?(\d{3})\)?[\s-]*(\d{3})[\s-]*(\d{2})[\s-]*(\d{2})(?:\s*\(?(доб\.?)\s*(\d+)\)?)?'
    )
    
    for contact in contacts_list[1:]:  # Пропускаем заголовок таблицы
        if not contact[5]:  # Если нет номера телефона, пропускаем
            continue
            
        phone = contact[5]
        match = phone_pattern.search(phone)
        if not match:  # Если номер не соответствует шаблону, пропускаем
            continue
            
        groups = match.groups()
        # Форматируем основной номер
        formatted = f'+7({groups[1]}){groups[2]}-{groups[3]}-{groups[4]}'
        # Добавляем добавочный номер, если есть
        if groups[5] and groups[6]:
            formatted += f' {groups[5].replace(".", "")}.{groups[6]}'
        contact[5] = formatted

def merge_duplicates(contacts_list):
    '''Функция для объединения дублирующихся записей
    
    Объединяет записи с одинаковыми фамилией (lastname) и именем (firstname).
    При объединении сохраняет все доступные данные из дубликатов.
    '''
    unique_contacts = {}  # Словарь для хранения уникальных контактов
    
    for contact in contacts_list[1:]:  # Пропускаем заголовок таблицы
        key = (contact[0], contact[1])  # Ключ - кортеж (фамилия, имя)
        if key not in unique_contacts:
            unique_contacts[key] = contact  # Добавляем новый контакт
        else:
            # Объединяем с существующей записью
            existing = unique_contacts[key]
            for i in range(len(contact)):
                if contact[i] and not existing[i]:  # Заполняем пустые поля
                    existing[i] = contact[i]
    
    # Собираем новый список: заголовок + уникальные контакты
    merged_list = [contacts_list[0]] + list(unique_contacts.values())
    return merged_list

def main():
    # Чтение исходного CSV файла
    with open(r'Gid Hub\ДЗ на проверку GidHub\регулярные выражения\phonebook_raw.scv', encoding='utf-8') as f:
        rows = csv.reader(f, delimiter=',')
        contacts_list = list(rows)
    
    # Обработка данных:
    fix_names(contacts_list)      # Стандартизация ФИО
    fix_phones(contacts_list)     # Форматирование телефонов
    contacts_list = merge_duplicates(contacts_list)  # Объединение дубликатов
    
    # Запись результата в новый CSV файл
    with open(r'Gid Hub\ДЗ на проверку GidHub\регулярные выражения\phonebook.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerows(contacts_list)
    
    print('Обработка завершена. Результат сохранен в phonebook.csv')
    print('Результат обработки:')
    pprint(contacts_list)

if __name__ == '__main__':
    main()






# # TODO 2: сохраните получившиеся данные в другой файл
# # код для записи файла в формате CSV
# with open('phonebook.csv', 'w', encoding='utf-8') as f:
#   datawriter = csv.writer(f, delimiter=',')
#   # Вместо contacts_list подставьте свой список
#   datawriter.writerows(contacts_list)