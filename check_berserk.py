#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
检查berserk库中Board类的seek方法的参数格式
"""

import berserk

# 打印Board类的seek方法的文档
print("\nBoard.seek方法的文档:")
print(berserk.clients.Board.seek.__doc__)

# 尝试创建一个客户端实例并查看其方法
client = berserk.Client()
board = client.board

# 打印seek方法的参数信息
print("\nseek方法的参数信息:")
print("参数名称:", board.seek.__code__.co_varnames)