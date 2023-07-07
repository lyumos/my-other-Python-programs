def print_formatted(number):
    width = len(bin(number)[2:])
    for i in range(1, number+1):
        print(str(i).rjust(width),oct(i)[2:].rjust(width),hex(i)[2:].title().rjust(width),bin(i)[2:].rjust(width))
if __name__ == '__main__':
    n = int(input('Введите любое число, чтобы отобразить числа до него в разных СС: '))
    print_formatted(n)