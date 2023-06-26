def merge_the_tools(s, k):
    char_list = []
    i = 0
    for item in s:
        if (i+1) % k == 0:
            if item not in char_list:
                char_list.append(item)
            print(''.join(char_list))
            char_list.clear()
        elif i == len(s)-1:
            if item not in char_list:
                char_list.append(item)
            print(''.join(char_list))
        else:
            if item not in char_list:
                char_list.append(item)
        i += 1



if __name__ == '__main__':
    string, k = input('Введите строку: '), int(input('Введите число: '))
    merge_the_tools(string, k)