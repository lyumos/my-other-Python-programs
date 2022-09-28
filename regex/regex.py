import csv
import re

if __name__ == '__main__':

    numbers_list = []
    lastname_name_list = []
    count = 0
    index_count = 0
    double_indexes = []

    with open("phonebook_raw.csv", encoding="utf-8") as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)

        for person in contacts_list:
            # форматирование ФИО
            full_name = (' '.join([person[0], person[1], person[2]]))
            full_name_list = full_name.split(' ')
            person[0] = full_name_list[0]
            person[1] = full_name_list[1]
            person[2] = full_name_list[2]

            # форматирование телефонов
            number = person[-2]
            number_pattern = r'(\+7|8)([\s\(]*)(\d{3})([\()]*)([\s\-]*)(\d{3})([\s\-]*)(\d{2})([\-]*)(\d{2})([\s\(]*)([\w\.]*)([\s]*)([\d{4}]*)([\)]*)'
            number_substitute = r"+7(\3)\6-\8-\g<10> \g<12>\g<14>"
            number_res = re.sub(number_pattern, number_substitute, number)
            numbers_list.append(number_res)
            person[-2] = number_res

            # выявление дублирований
            lastname_name = person[0] + ' ' + person[1]

            if lastname_name not in lastname_name_list:
                lastname_name_list.append(lastname_name)
            else:
                original_index = lastname_name_list.index(lastname_name) + count
                double_index = contacts_list.index(person)
                count += 1
                original_info = contacts_list[original_index]
                double_info = contacts_list[double_index]
                # объединение дублирований
                for info in double_info:
                    if info not in original_info:
                        index = double_info.index(info)
                        original_info[index] = info
                #  сохранение полной информации о человеке в оригинале и сохранение индексов повторений
                person = original_info
                double_indexes.append(double_index)

        # удаление повторений
        for double in double_indexes:
            if double == double_indexes[0]:
                del contacts_list[double]
            else:
                index_count += 1
                correct_double = double - index_count
                del contacts_list[correct_double]

    with open("phonebook.csv", "w", encoding="utf-8") as f:
      datawriter = csv.writer(f, delimiter=',')
      datawriter.writerows(contacts_list)