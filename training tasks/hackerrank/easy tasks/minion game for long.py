def minion_game(string):
    stuart_score, kevin_score = 0, 0
    for index in range(len(string)):
        char = string[index]
        if char in {'A', 'E', 'I', 'O', 'U'}:
            kevin_score += (len(string) - index)
        else:
            stuart_score += (len(string) - index)
    if stuart_score == kevin_score:
        print('Draw')
    elif stuart_score > kevin_score:
        print('Stuart', stuart_score)
    else:
        print('Kevin', kevin_score)

if __name__ == '__main__':
    s = input('Ввдите слово капсом: ')
    minion_game(s)