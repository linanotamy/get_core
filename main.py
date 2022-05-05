import re
import docx2txt
from pymorphy2 import MorphAnalyzer
from nltk.tokenize import RegexpTokenizer
from collections import Counter
from pdf2docx import parse
from typing import Tuple


def take_theme(text):  # find the theme on the standard mirea title
    text = docx2txt.process(text)
    text = text.lower()
    list_text = text.split()
    p = 0
    while list_text[p] != 'на' and list_text[p + 1] != 'тему':
        p = p + 1
    p = p + 2
    g = p
    while not re.search('студент', list_text[g]):
        g = g + 1
    theme_l = list_text[p:g]
    print(f'Тема :')  # print the theme
    theme_str = ''
    for k in range(len(theme_l)):
        theme_str = theme_str + ' ' + theme_l[k]
    print(theme_str)
    return theme_l


def take_from_docx(file):  # take docx
    text = docx2txt.process(file)  # convert to text
    return take_text(text, 'todel.txt')  # call take_text


def take_text(text_to_prepare, list_to_clean):  # take text variable and prepare it to analysis
    obr_text = preprocessing(text_to_prepare)  # call preprocessing to transform the text to proper form
    list_text = obr_text.split()  # convert it to the list
    list_text = cleaner(list_text, list_to_clean)  # call cleaner to remove lines from list of extra words
    return list_text  # return prepared list


def preprocessing(text):  # take text variable and change every world to nominative case/ infinitive/ etc
    new_morph_analyzer = MorphAnalyzer(lang='ru')  # use pymorphy2
    new_tokenizer = RegexpTokenizer(r"[А-Яа-яA-Za-z0-9]+|[\.\,:\(\)\;\!\^\?*]+")
    # use nltk.tokenize to separate signs and words
    return ' '.join([new_morph_analyzer.parse(word)[0].normal_form if not re.search(r"[.,:();!^?]", word) else word
                     for word in new_tokenizer.tokenize(text)])


def cleaner(list_to_check, list_to_delete):  # take list to clear and delete lines from list of extra words
    lines_sep = take_list(list_to_delete)  # take list from txt file
    j = 0
    while lines_sep[j] != "ENDOFDOCUMENT":  # if line in list to clean then delete it from there
        while lines_sep[j] in list_to_check:
            list_to_check.remove(lines_sep[j])
        j += 1
    return list_to_check


def take_list(list_name):  # take txt file and convert in list
    with open(list_name) as t:
        lines = t.read()
    sep_lines = lines.split()
    return sep_lines


def count_most_fr(list_txt, n):  # take prepared text and find 10 most frequent which are key words for the text
    counter_list = Counter(list_txt)   # use Counter from collections
    most_freq = counter_list.most_common(n)  # take n most frequent
    return most_freq  # return them as a list of tuple


def print_list_tuple(list_tuple, n):  # small function to print the list of tuple in a nice way
    for i in range(len(list_tuple)):
        print(list_tuple[i][0], ' ', f"{list_tuple[i][1]/n*100:.2f}%")
        # print a word and calculated frequency in the text
        # in list_tuple[i][1] is a amount of the word in the text
        # n is keeping length of the prepared text


def find_and_delete_code(list_txt):  #  create progr
    i = 0
    codes = 0  # var to keep len of code
    while i < len(list_txt):  # find code and delete it
        if not re.match(r'[a-z0-9]', list_txt[i]):  # if word i is not code just go to the next word
            i = i + 1
        else:  # if it could be code than check next 10 words
            k = 0
            if i + 10 <= len(list_txt):
                for j in range(i, i + 10):
                    if re.match(r'[a-z0-9]', list_txt[j]):
                        k = k + 1
            else:
                for j in range(i, len(list_txt)):
                    if re.match(r'[a-z0-9]', list_txt[j]):
                        k = k + 1
            if k < 7:  # if less 7/10 is possible code than just go to the next word
                i = i + 1
            else:
                u = i  # beginning of the code
                fl = 0  # flag, non code words
                while fl < 7 and i <= len(list_txt):  # while not code words less than 7/10 guess that still code
                    fl = 0  # fl = 0
                    if i + 10 <= len(list_txt):
                        for j in range(i, i + 10):  # check next 10 words
                            if not re.match(r'[a-z0-9]', list_txt[j]):  # if not code then flag+1
                                fl = fl + 1
                    elif i <= len(list_txt):
                        for j in range(i, len(list_txt)):
                            if not re.match(r'[a-z0-9]', list_txt[j]):  # if not code then flag+1
                                fl = fl + 1
                    i = i + 1  # go to the next word, if fl < 7
                y = i  # if fl >= 7 than it's no longer the code and y = i become the end
                del list_txt[u:y]  # delete code in borders [u:y]
                i = u  # go to i = u
                codes = codes + y - u  # add len of code (amount of words)
    return list_txt, codes


def del_numbers(list_txt):
    i = 0
    while i < len(list_txt):  # find number
        if not re.match(r'[0-9]', list_txt[i]):
            i = i + 1
        else:
            del list_txt[i]
    return list_txt


def OPK61(codes):
    if codes > 0:
        print('ОПК-6.1: ДА')
    else:
        print('ОПК-6.1: НЕТ')


def OPK62(list_txt):  # use insrt
    i = 0
    j = 0
    dic_OPK62 = 'OPK6.2.txt'
    list_dic_OPK62 = take_list(dic_OPK62)
    while i < len(list_txt):
        if re.match(r'[a-z]', list_txt[i]):
            for k in range(len(list_dic_OPK62)):
                if list_txt[i] == list_dic_OPK62[k]:
                    j = j + 1
        i = i + 1
    if j > 0:
        print('ОПК-6.2: ДА')
    else:
        print('ОПК-6.2: НЕТ')


def convert_pdf2docx(input_file: str, output_file: str, pages: Tuple = None):
    if pages:
        pages = [int(i) for i in list(pages) if i.isnumeric()]
    result = parse(pdf_file=input_file,
                   docx_with_path=output_file, pages=pages)
    return result



if __name__ == '__main__':
    try:
       pass
    except:
        print('Mistake!')

