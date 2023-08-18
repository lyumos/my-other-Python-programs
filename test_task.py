def calculate_min_score(x: int, y: int, z: int) -> int:
    score_diff = abs(x-y) #разница (модуль) между очками
    z_max_score_diff = z - max(x, y) #сколько при хорошем раскладе нужно набрать для победы (для max(x, y))
    if score_diff >= 2 and z <= max(x, y):
        return 0 #один из участников уже выиграл
    elif score_diff < 2: #если плотная борьба
        # 2 - score_diff -> сколько нужно набрать (потерять) очков для разницы в 2
        return max(z_max_score_diff, 2 - score_diff)
    else: #отрыв в очках есть, но z еще не достигнут
        return z_max_score_diff


if __name__ == '__main__':
    x = int(input('X: '))
    y = int(input('Y: '))
    z = int(input('Z: '))
    print(calculate_min_score(x, y, z))
