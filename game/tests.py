import random

import time
from django.test import TestCase

# Create your tests here.

row = 4
col = 4

row_count = 8
col_count = 8
icon_map = []
empty_positions = []


def choices(src_arr, count):
    # 拷贝一份防止修改原来的数组内容
    arr = src_arr.copy()
    length = len(arr)
    for i in range(count):
        index = random.randint(0, length - i - 1)
        last_index = length - 1 - i
        arr[index], arr[last_index] = arr[last_index], arr[index]
    return arr[length - count:]


# 序号转换为位置
def number2position(number, col_count):
    r = number // col_count
    c = number % col_count
    return r, c


# 位置转换为序号
def position2number(position, col_count):
    return position[0] * col_count + position[1]


def is_out_border(arr, r, c):
    return not (r >= 0 and r < len(arr) and c >= 0 and c < len(arr[r]))


def connected(p1, p2):
    position_queue = []
    p1 = [p1[0] + 1, p1[1] + 1]
    p2 = [p2[0] + 1, p2[1] + 1]
    position_queue.append(p1)
    map = []
    end = False
    for i in range(row_count):
        map.append([])
        for j in range(col_count):
            map[i].append({'icon': icon_map[i][j], 'zedian': -1, 'src': None})
    map.append([])
    map.insert(0, [])
    for i in range(col_count):
        map[0].append({'icon': -1, 'zedian': -1, 'src': None})
        map[-1].append({'icon': -1, 'zedian': -1, 'src': None})
    for i in range(row_count + 2):
        map[i].append({'icon': -1, 'zedian': -1, 'src': None})
        map[i].insert(0, {'icon': -1, 'zedian': -1, 'src': None})
    row_col_offset = [[0, 1], [0, -1], [1, 0], [-1, 0]]
    while position_queue:
        p = position_queue.pop(0)
        for offset in row_col_offset:
            r = p[0]
            c = p[1]
            rr = p[0] + offset[0]
            cc = p[1] + offset[1]
            while not is_out_border(map, rr, cc):
                if map[rr][cc]['zedian'] != -1 and map[rr][cc]['zedian'] != 100:
                    pass
                elif map[rr][cc]['icon'] == -1:
                    map[rr][cc]['zedian'] = map[r][c]['zedian'] + 1
                    map[rr][cc]['src'] = [r, c]
                    if map[rr][cc]['zedian'] <= 2:
                        position_queue.append([rr, cc])
                elif map[rr][cc]['icon'] != -1 and rr == p2[0] and cc == p2[1]:
                    if map[r][c]['zedian'] + 1 <= 2:
                        map[rr][cc]['zedian'] = map[r][c]['zedian'] + 1
                        map[rr][cc]['src'] = [r, c]
                        end = True
                        break
                else:
                    map[rr][cc]['zedian'] = 100
                    break
                rr += offset[0]
                cc += offset[1]
            if end:
                break
        if end:
            break
    if map[p2[0]][p2[1]]['src'] == None:
        return False
    t = p2
    link_positions = []
    while map[t[0]][t[1]]['src'] != None:
        print([t[0] - 1, t[1] - 1])
        link_positions.append([t[0] - 1, t[1] - 1])
        t = map[t[0]][t[1]]['src']
    print([p1[0] - 1, p1[1] - 1])
    link_positions.append([p1[0] - 1, p1[1] - 1])
    return link_positions


def can_continue():
    for i in range(row_count * col_count):
        r1, c1 = number2position(i, col_count)
        if icon_map[r1][c1] == -1:
            continue
        for j in range(i + 1, row_count * col_count):
            r2, c2 = number2position(j, col_count)
            if icon_map[r2][c2] == -1:
                continue
            if icon_map[r1][c1] != icon_map[r2][c2]:
                continue
            if connected([r1, c1], [r2, c2]):
                print(r1, c1, r2, c2)
                return r1, c1, r2, c2
                # return True
    return False


def is_win(icon_map):
    for r in icon_map:
        for i in r:
            if i != -1:
                return False
    return True


def game():
    global icon_map
    global empty_positions
    icon_map = []
    empty_positions = []
    # 初始化iconMap数组和emptyPositions数组
    for i in range(row_count):
        icon_map.append([])
        for j in range(col_count):
            empty_positions.append(position2number([i, j], col_count))
            icon_map[i].append(-1)

    # 遍历图片上的图标 每个图标从空白位置中随机抽取四个位置填上代表该图标的数字
    for i in range(row * col):
        positions = choices(empty_positions, 4)
        for v in positions:
            empty_positions.remove(v)
            r, c = number2position(v, col_count)
            icon_map[r][c] = i
    # icon_map= [
    #     [5, 4, 14, 12, 1, 6, 7, 1],
    #     [6, 11, 13, 8, 3, 14, 8, 12],
    #     [11, 11, 9, 15, 12, 10, 1, 15],
    #     [12, 7, 8, 4, 3, 10, 14, 10],
    #     [8, 2, 7, 9, 4, 1, 0, 0],
    #     [1, 5, 0, 2, 14, 9, 7, 11],
    #     [9, 13, 4, 15, 5, 13, 5, 6],
    #     [6, 2, 3, 15, 13, 3, 0, 2]
    # ]
    for r in icon_map:
        for i in r:
            print('%02d' % i, end=',')
        print()
    while True:
        can = can_continue()
        if is_win(icon_map):
            game()
        if not can:
            break
        # s = input()
        # ss = s.split(' ')
        # ss = [int(i) for i in ss]
        ss = can
        p1 = [ss[0], ss[1]]
        p2 = [ss[2], ss[3]]
        eq = icon_map[ss[0]][ss[1]] == icon_map[ss[2]][ss[3]]
        a = connected(p1, p2)
        print(eq, a)
        if eq and a:
            icon_map[ss[0]][ss[1]] = -1
            icon_map[ss[2]][ss[3]] = -1
        for r in icon_map:
            for i in r:
                print('%02d' % i, end=',')
            print()
        time.sleep(0.1)


if __name__ == '__main__':
    game()
