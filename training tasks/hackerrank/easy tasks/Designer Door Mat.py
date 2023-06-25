n,m = [int(k) for k in input('Введите два чилса через пробел - x и 3*x: ').split()]
odd_list = [1]
start = 2
for i in range(1, n):
    if i == 1:
        print('.|.'.center(m, '-'))
    else:
        for j in range(start, i):
            if i % j != 0 and j % 2 != 0:
                if j not in odd_list:
                    s = j * '.|.'
                    print(s.center(m, '-'))
                odd_list.append(j)
            start = j
        odd_list = list(set(odd_list))
print('WELCOME'.center(m,'-'))
for i in odd_list[::-1]:
        s = i * '.|.'
        print(s.center(m, '-'))
