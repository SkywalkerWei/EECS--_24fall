def is_safe(loca):
    # 检查冲突情况，狼羊，羊菜
    a, b, c, d = (loca & 8) > 0, (loca & 4) > 0, (loca & 2) > 0, (loca & 1) > 0
    return not ((a != c and c == d) or (a != b and b == c))
'''
# 十进制输出位置情况
def print_route(route, status):
    if status == -2:
        print("start", end="")
    else:
        print_route(route, route[status])
        print(f"->{status}", end="")
'''
# 二进制输出位置情况
def print_route(route, status):
    # status存储当前位置状态，route[status]是下一步的状态，类似链表
    if status == -2:
        print("start", end="")
    else:
        print_route(route, route[status])
        print(f"->{bin(status)[2:].zfill(4)}", end="")


def process(loc, route, count):
    if route[15] != -1:
        count[0] += 1
        print(f"第{count[0]}种方法：")
        print_route(route, 15)
        print("\n")
        return

    for move in [1, 2, 4, 8]:
        if ((loc & 8) > 0) == ((loc & move) > 0):
            next_loc = loc ^ (8 | move)
            if is_safe(next_loc) and route[next_loc] == -1:
                route[next_loc] = loc
                process(next_loc, route[:], count)

if __name__ == "__main__":
    route = [-1] * 16
    route[0] = -2
    process(0, route, [0])

# 目标右1 原地左0，农夫/狼/羊/菜 四位二进制判定位置 用位运算模拟移动和冲突判断