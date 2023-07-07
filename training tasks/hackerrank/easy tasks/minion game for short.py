import re


def count_str(string, substring):
    substring_re = '(?=(%s))' % re.escape(substring)
    return len(re.findall(substring_re, string))


def minion_game(s):
    vowels = ['A', 'E', 'I', 'O', 'U']
    words = {}
    stuart_score, kevin_score, index = 0, 0, -1
    for char in s:
        index += 1
        j = index
        while j <= len(s) - 1:
            word = s[index:j + 1]
            count = count_str(s, word)
            words.update({word: count})
            j += 1
    for item in words:
        if item[0] in vowels:
            kevin_score += words[item]
        else:
            stuart_score += words[item]
    if stuart_score > kevin_score:
        print(f'Stuart {stuart_score}')
    elif stuart_score == kevin_score:
        print('Draw')
    else:
        print(f'Kevin {kevin_score}')


if __name__ == '__main__':
    s = input('Введите слово капсом: ')
    minion_game(s)
