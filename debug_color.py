#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
调试脚本：用于诊断Lichess机器人颜色识别问题

此脚本会打印出游戏事件中的关键信息，帮助诊断为什么机器人无法正确识别执棋颜色。
"""

import os
import time
import json
import chess
import berserk
from config import LICHESS_API_TOKEN

# 创建Lichess客户端
client = berserk.Client(berserk.TokenSession(LICHESS_API_TOKEN))

# 获取用户信息
user_profile = client.account.get()
username = user_profile['username']
print(f"已连接到Lichess账户: {username}")

# 获取当前正在进行的游戏
def get_ongoing_game():
    try:
        ongoing_games = client.games.get_ongoing()
        if ongoing_games:
            return ongoing_games[0]  # 返回第一个正在进行的游戏
        return None
    except Exception as e:
        print(f"获取正在进行的游戏失败: {e}")
        return None

# 调试游戏事件
def debug_game_events(game_id):
    print(f"\n开始调试游戏 {game_id} 的颜色识别问题...")
    print("等待游戏事件...\n")
    
    try:
        for event in client.board.stream_game_state(game_id):
            print("\n收到事件:")
            print(f"事件类型: {event['type']}")
            
            # 打印完整事件（格式化为JSON）
            print("\n完整事件数据:")
            print(json.dumps(event, indent=2, ensure_ascii=False))
            
            if event['type'] == 'gameFull':
                print("\n游戏开始事件分析:")
                # 检查白方信息
                if 'white' in event:
                    print(f"白方信息: {event['white']}")
                    if 'id' in event['white']:
                        print(f"白方ID: {event['white']['id']}")
                        print(f"是否为当前用户: {event['white']['id'] == username}")
                    else:
                        print("警告: 白方信息中没有'id'字段")
                else:
                    print("警告: 事件中没有'white'字段")
                
                # 检查黑方信息
                if 'black' in event:
                    print(f"黑方信息: {event['black']}")
                    if 'id' in event['black']:
                        print(f"黑方ID: {event['black']['id']}")
                        print(f"是否为当前用户: {event['black']['id'] == username}")
                    else:
                        print("警告: 黑方信息中没有'id'字段")
                else:
                    print("警告: 事件中没有'black'字段")
                
                # 确定我的颜色
                my_color = None
                if 'white' in event and 'id' in event['white'] and event['white']['id'] == username:
                    my_color = "白棋 (chess.WHITE)"
                elif 'black' in event and 'id' in event['black'] and event['black']['id'] == username:
                    my_color = "黑棋 (chess.BLACK)"
                else:
                    my_color = "未知"
                
                print(f"\n根据事件分析，您应该执: {my_color}")
                
            elif event['type'] == 'gameState':
                print("\n游戏状态更新分析:")
                if 'moves' in event:
                    moves = event['moves'].split()
                    move_count = len(moves)
                    print(f"当前已走步数: {move_count}")
                    
                    # 根据步数判断当前轮到谁走
                    current_turn = "白棋" if move_count % 2 == 0 else "黑棋"
                    print(f"当前轮到: {current_turn}")
            
            print("\n按Ctrl+C退出调试...")
            
    except KeyboardInterrupt:
        print("\n调试已停止")
    except Exception as e:
        print(f"\n调试过程中出错: {e}")

# 主程序
def main():
    print("Lichess机器人颜色识别调试工具")
    print("=============================")
    
    # 获取当前游戏
    game = get_ongoing_game()
    
    if game:
        print(f"\n找到正在进行的游戏: {game['gameId']}")
        debug_game_events(game['gameId'])
    else:
        print("\n没有找到正在进行的游戏。请先在Lichess上开始一局游戏，然后再运行此脚本。")

if __name__ == "__main__":
    main()