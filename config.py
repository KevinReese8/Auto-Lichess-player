#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
配置文件

此文件包含Lichess机器人所需的配置参数。
"""

# 请从 https://lichess.org/account/oauth/token 获取您的API令牌
# 确保您的令牌具有以下权限：
# - 读取偏好设置
# - 读取电子邮件地址
# - 在网站上下棋
# - 挑战AI和真人玩家
LICHESS_API_TOKEN = "lip_p3F5IDTXoHVfszc5fLqt"  # 请替换为您的实际令牌

# 国际象棋引擎路径
# 如果留空，程序将尝试在默认位置查找Stockfish引擎
ENGINE_PATH = "/opt/homebrew/bin/stockfish"

# 引擎思考时间（秒）
ENGINE_THINK_TIME = 2.0

# 游戏设置
GAME_SETTINGS = {
    "clock": {
        "limit": 10,  # 初始时间（分钟）
        "increment": 0  # 每步增加的时间（秒）
    },
    "variant": "standard",  # 游戏变体：standard, chess960, crazyhouse, etc.
    "color": "random",  # 颜色选择：white, black, random
    "rated": True  # 是否为评级游戏
}