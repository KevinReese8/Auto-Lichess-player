#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试脚本：检查Lichess游戏事件的结构
"""

import berserk
import json

print("\nBoard.stream_game_state方法的文档:")
print(berserk.clients.Board.stream_game_state.__doc__)

print("\n游戏事件类型:")
print("gameFull - 完整游戏信息，包含白方和黑方信息")
print("gameState - 游戏状态更新")

print("\n示例gameFull事件结构:")
print("{")  
print("  'type': 'gameFull',")
print("  'id': '游戏ID',")
print("  'rated': true/false,")
print("  'variant': { 'key': 'standard', ... },")
print("  'clock': { ... },")
print("  'white': { 'id': '白方玩家ID', 'name': '白方玩家名称', ... },")
print("  'black': { 'id': '黑方玩家ID', 'name': '黑方玩家名称', ... },")
print("  'state': { ... }")
print("}")

print("\n在handle_game_start方法中，我们通过检查event['white']['id']是否等于self.username来确定机器人执白棋还是黑棋。")
print("如果event['white']['id'] == self.username，则self.my_color = chess.WHITE，否则self.my_color = chess.BLACK。")

print("\n在handle_game_state方法中，我们通过检查self.board.turn和self.my_color来确定是否轮到机器人走棋:")
print("if (self.board.turn == chess.WHITE and self.my_color == chess.WHITE) or (self.board.turn == chess.BLACK and self.my_color == chess.BLACK)")

print("\n问题可能出在:")
print("1. gameFull事件中的white/black结构与预期不符")
print("2. self.username与event['white']['id']或event['black']['id']的比较方式有问题")
print("3. self.my_color在某些情况下没有正确设置或被意外修改")