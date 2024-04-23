#!/usr/bin/env python3
# _*_ coding:utf-8 _*_


import random

# 双色球红球最大数和蓝球最大数
RED_MAX = 33
BLUE_MAX = 16

def generate_ssc():
    # 随机生成6个红球
    red_balls = random.sample(range(1, RED_MAX + 1), 6)
    red_balls.sort()  # 对红球排序（因为开奖结果是按从小到大排列）

    # 随机生成1个蓝球
    blue_ball = random.randint(1, BLUE_MAX)

    return red_balls, blue_ball


if __name__=="__main__":

    red_nums, blue_num = generate_ssc()
    print(f"本期推荐的双色球号码为：红球 {', '.join(map(str, red_nums))} 蓝球 {blue_num}")

