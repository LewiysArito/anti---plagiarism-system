end_punctuations = [".", "!", "?", ";"]  # Список пунктуационных знаков,
#которые могут встречаться в конце предложения
middle_punctuations = [":", ",", "(",
                       ")", "-", "–",
                       "'", "[", "]",
                       "+", "/", "*",
                       "=", "\\"]  # Список пунктуационных знаков,
# которые могут встречаться в середине предложения
punctuations = end_punctuations + middle_punctuations
path = "C:\\Users\\nikit\\Desktop\\coursework\\"  # Директория, в которой
# находятся необходимые для работы файлы
count_file = 1  # Количество файлов, с которыми будет идти сравнение
folder = "compare\\"


# Функция, превращающая файл состоящий из стоп слов в единый массив
def stop_word(name_file):
    with open(path + name_file, encoding="utf-8") as text:
        list_stop = []
        for row in text:
            word = []
            for symbol in row:
                if symbol in punctuations or symbol == " ":
                    if len(word) >= 1:
                        list_stop.append("".join(word))
                        word = []
                else:
                    if symbol == "ё":
                        symbol = "е"
                    word.append(symbol)
    return list_stop


# Функция, превращающая исследуемый на антиплагиат файл,
# в список, состоящий из предложений, который включают в себя
# только слова
def formatting_file(name_file):
    with open(path + name_file, encoding="utf-8") as file:
        format_text = []
        for text in file:
            sentense = []
            word = []
            for symbol in text:
                if symbol in punctuations or symbol == " " or symbol.isdigit() == True:
                    if len(word) >= 1:
                        sentense.append("".join(word).lower())
                        word = []
                    if symbol in end_punctuations:
                        format_text.append(sentense)
                else:
                    if symbol == "ё":
                        symbol = "е"
                    word.append(symbol)
    return format_text


# Функция, которая дорабатывет список из предложений,
# убирая стоп-слова
def end_formatting_file(text, list_stop):
    end_format_text = []
    for row in text:
        sentense = []
        for word in row:
            if word not in list_stop:
                if word not in sentense:
                    sentense.append(word)
        end_format_text.append(sentense)
    return end_format_text


# Функция, сортирующая слова из каждого списка предлоложений исходного массива
def sorting_list(mas):
    sorted_list = []
    for row in mas:
        sort_row = sorted(row, key=lambda x: x[0] and x[1] and len(x))
        sorted_list.append(sort_row)
    return sorted_list


# Функция ищущая количество слов в массиве
def searh_lenght(mas):
    lenght = 0
    for word in mas:
        lenght += len(word)
    return lenght


# Функция, совмещающая в себе функция создания и дороботку
# массива, а также его сортировку
def change_list(name_file):
    format_text = formatting_file(name_file)
    end_format_text = end_formatting_file(format_text, list_stop)
    sorted_list = sorting_list(end_format_text)
    return sorted_list


# Функция, сравнивающая два массива на схожесть
def compare(list_1, list_2):
    global list_repeat
    index = 0
    for lines_1 in list_1:
        max_mas = []
        for lines_2 in list_2:
            current_mas = []
            for word_1 in lines_1:
                for word_2 in lines_2:
                    if word_1 == word_2:
                        if word_1 not in current_mas:
                            current_mas.append(word_1)
                        break
            if len(current_mas) > len(max_mas):
                max_mas = current_mas
        if len(list_repeat[index]) < len(max_mas):
            list_repeat[index] = max_mas
        index += 1
    return None


# Функция, подсчитывающая оригинальность исходного файла
def count_originals(explorer_list):
    for number in range(1, count_file + 1):
        comparable_list = change_list(folder + "text" + str(number) + ".txt")
        compare(explorer_list, comparable_list)
    return f"Уникальность текста {round((1 - (searh_lenght(list_repeat) / searh_lenght(explorer_list))) * 100)}%"


list_stop = stop_word("list_stop-word.txt")
explorer_list = change_list("explorer.txt")
list_repeat = [[] for line in explorer_list]
print(count_originals(explorer_list))
