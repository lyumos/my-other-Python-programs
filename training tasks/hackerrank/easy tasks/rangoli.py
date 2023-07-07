import string
def print_rangoli(size):
    alpha = string.ascii_lowercase
    width = (size-1) * 4 + 1
    print_list = ['-' for k in range(0, width)]
    char_list, str_list = [], []
    for i in range(size-1, -1, -1):
        char = alpha[i]
        char_list.insert(0, char)
        for j in char_list:
            id = char_list.index(j)
            print_list[width // 2 + 2 * id] = j
            print_list[width // 2 - 2 * id] = j
        s = ''.join(print_list)
        str_list.insert(0, s)
        print(s)
    for item in str_list:
        if str_list.index(item) != 0:
            print(item)


if __name__ == '__main__':
    n = int(input('Введите число не больше 26: '))
    print_rangoli(n)