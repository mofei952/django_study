#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Author  : mofei
# @Time    : 2018/9/5 15:50
# @File    : service.py
# @Software: PyCharm
import random


def choices(src_arr, count):
    """从列表中随机取count个数，不能重复"""
    # 拷贝一份防止修改原来的数组内容
    arr = src_arr.copy()
    length = len(arr)
    for i in range(count):
        index = random.randint(0, length - i - 1)
        last_index = length - 1 - i
        arr[index], arr[last_index] = arr[last_index], arr[index]
    return arr[length - count:]


def number2position(number, col_count):
    """序号转换为位置"""
    r = number // col_count
    c = number % col_count
    return r, c


def position2number(position, col_count):
    """位置转换为序号"""
    return position[0] * col_count + position[1]


def is_out_border(map, r, c):
    """是否出界"""
    return not (r >= 0 and r < len(map) and c >= 0 and c < len(map[r]))


def icon_map(icon_count, row_count, col_count):
    """生成图标map"""
    # icon_count = 16
    # row_count = 8
    # col_count = 8
    # icon二位数组 存放显示的图标情况
    icon_map = []
    # 空白位置列表 初始化随机抽取位置时使用
    empty_positions = []
    # 初始化iconMap数组和emptyPositions数组
    for i in range(row_count):
        icon_map.append([])
        for j in range(col_count):
            empty_positions.append(position2number([i, j], col_count))
            icon_map[i].append(-1)
    # 遍历图片上的图标 每个图标从空白位置中随机抽取四个位置填上代表该图标的数字
    count_pre_icon = int(row_count * col_count / icon_count)
    for i in range(icon_count):
        positions = choices(empty_positions, count_pre_icon)
        for v in positions:
            empty_positions.remove(v)
            r, c = number2position(v, col_count)
            icon_map[r][c] = i
    # icon_map = [
    #     [-1, -1, -1, -1, -1, -1, -1, -1],
    #     [-1, -1, -1, -1, -1, -1, -1, -1],
    #     [-1, -1, -1, -1, -1, -1, -1, -1],
    #     [-1, -1, 6, 12, -1, -1, -1, -1],
    #     [11, -1, 12, 4, -1, 9, -1, -1],
    #     [0, -1, 8, 1, 0, 8, -1, -1],
    #     [-1, -1, 9, 6, -1, -1, -1, 4],
    #     [-1, -1, -1, -1, 1, 11, -1, -1],
    # ]
    return icon_map


def connected(icon_map, p1, p2):
    """在map中p1和p2点是否连通，若连通返回连通的关键点列表"""
    row_count = len(icon_map)
    col_count = len(icon_map[0])
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
        # print([t[0] - 1, t[1] - 1])
        link_positions.append([t[0] - 1, t[1] - 1])
        t = map[t[0]][t[1]]['src']
    # print([p1[0] - 1, p1[1] - 1])
    link_positions.append([p1[0] - 1, p1[1] - 1])
    return link_positions


def hint(icon_map):
    """提示，返回可连接的两个点"""
    row_count = len(icon_map)
    col_count = len(icon_map[0])
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
            if connected(icon_map, [r1, c1], [r2, c2]):
                return [r1, c1], [r2, c2]
    return False


def is_win(icon_map):
    for r in icon_map:
        for i in r:
            if i != -1:
                return False
    return True


def status(icon_map):
    """
        游戏状态
        返回true代表胜利，false代表没结束继续游戏，
        返回map代表没有连通的了，则将map打乱后返回
    """
    if is_win(icon_map):
        return True
    if hint(icon_map):
        return False
    # 打乱
    arr = []
    for r in icon_map:
        for i in r:
            arr.append(i)
    random.shuffle(arr)
    index = 0
    for i in range(len(icon_map)):
        for j in range(len(icon_map[i])):
            icon_map[i][j] = arr[index]
            index += 1
    return icon_map
