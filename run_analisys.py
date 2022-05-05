import main
import re
import os


def except_lines():
    fl_wo = input('''Для завершения работы введите 1.
    ENTER чтобы продолжить''')
    fl_e = 1
    return fl_e, fl_wo


if __name__ == '__main__':
    fl_work = 0
    print('''Данная версия программы позволяет выявить, были ли получены студентом следующие компетенции:
ОПК-6.1  : Разрабатывает алгоритмы и компоненты программных модулей;
ОПК-6.2  : Использует современные инструментальные средства разработки программ.
Программа способна обрабатывать файлы с расширениями .pdf и .docx''')
    while fl_work != '1':
        try:
            print('Укажите путь к файлу для анализа:')
            filename = input()
            fl_pdf = 0
            if filename[len(filename)-3:len(filename)] == 'pdf':
                input_file = filename
                output_file = filename[0:len(filename)-4] + '.docx'
                main.convert_pdf2docx(input_file, output_file)
                filename = filename[0:len(filename)-4] + '.docx'
                fl_pdf = 1
            theme = main.take_theme(filename)  # find the theme of the project
            list_text_prep = main.take_from_docx(filename)  # take text to start its analysis
            y = 0
            for i in range(len(list_text_prep) - 1):  # find where literature starts
                if re.search('список', list_text_prep[i]) and (
                        re.search('использов', list_text_prep[i + 1]) or re.search('литератур', list_text_prep[i + 1])):
                    y = i  # it could be 'список использованной литературы' or 'список использованных источников'
                    # take only the last position where the condition is true
            if y != 0:
                del list_text_prep[y:]
            y = 0
            fl = -1
            for i in range(len(list_text_prep) - 1):  # find where text of project itself starts
                if list_text_prep[i] == 'введение':
                    for j in range(i - 20, i - 1):  # if under 'введение' is 'список ист' -> here the text itself starts
                        if re.search('список', list_text_prep[j]) and (
                                re.search('использов', list_text_prep[j + 1]) or
                                re.search('литератур', list_text_prep[j + 1])):
                            y = i
                            fl = 1
                            break
                if fl == 1:
                    break
            del list_text_prep[:y]
            list_text_prep,  code_len = main.find_and_delete_code(list_text_prep)
            list_text_prep = main.del_numbers(list_text_prep)
            core_text_list = main.count_most_fr(list_text_prep, 10)
            main.print_list_tuple(core_text_list, len(list_text_prep))
            print('\nКомпетенции:')
            main.OPK61(code_len)
            main.OPK62(list_text_prep)
            if fl_pdf == 1:
                os.remove(filename)
            fl_ex = 0
        except FileNotFoundError:
            print('Файл не найден!')
            fl_ex, fl_work = except_lines()
        except Exception:
            print('Ошибка!')
            fl_ex, fl_work = except_lines()
        if fl_ex == 0:
            fl_work = input('''Для завершения работы введите 1.
ENTER чтобы продолжить''')
