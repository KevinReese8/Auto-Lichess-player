import os
import time
import chess
import chess.engine
import berserk
from config import LICHESS_API_TOKEN, GAME_SETTINGS


class LichessBot:
    def __init__(self, token, engine_path=None, game_settings=None):
        """
        初始化Lichess机器人
        
        参数:
            token (str): Lichess API令牌
            engine_path (str): 国际象棋引擎路径，如果为None，将使用Stockfish
            game_settings (dict): 游戏设置
        """
        self.client = berserk.Client(berserk.TokenSession(token))
        self.user_profile = self.client.account.get()
        self.username = self.user_profile['username']
        print(f"已连接到Lichess账户: {self.username}")
        
        # 保存游戏设置
        if game_settings:
            self.game_settings = self._convert_game_settings(game_settings)
        else:
            self.game_settings = {}
        
        # 设置国际象棋引擎
        if engine_path is None:
            # 尝试找到Stockfish引擎
            if os.name == 'nt':  # Windows
                engine_path = "stockfish/stockfish-windows-x86-64.exe"
            elif os.name == 'posix':  # macOS/Linux
                engine_path = "stockfish/stockfish-macos-x86-64"
                if not os.path.exists(engine_path):
                    engine_path = "stockfish/stockfish-ubuntu-x86-64"
        
        try:
            self.engine = chess.engine.SimpleEngine.popen_uci(engine_path)
            print(f"已连接到国际象棋引擎: {engine_path}")
        except FileNotFoundError:
            print(f"错误: 找不到国际象棋引擎 {engine_path}")
            print("请下载Stockfish引擎并放在正确的位置，或者提供正确的引擎路径")
            raise
        
        self.current_game = None
        self.board = None
        self.my_color = None
    
    def start_game(self):
        """
        开始一个新的游戏
        """
        print("正在寻找新对局...")
        # 使用快速匹配模式寻找对局
        try:
            # 提取游戏设置中的参数
            clock_limit = self.game_settings.get('clock', {}).get('limit', 600)
            clock_increment = self.game_settings.get('clock', {}).get('increment', 0)
            variant = self.game_settings.get('variant', 'standard')
            color = self.game_settings.get('color', 'random')
            rated = self.game_settings.get('rated', True)
            
            # 使用正确的参数格式调用seek方法
            self.client.board.seek(
                time=clock_limit,
                increment=clock_increment,
                variant=variant,
                color=color,
                rated=rated
            )
            print(f"已加入快速匹配队列，等待匹配对手... (时间设置: {clock_limit}秒, 增量: {clock_increment}秒)")
        except berserk.exceptions.ResponseError as e:
            print(f"加入匹配队列失败: {e}")
            # 尝试寻找现有的挑战并接受
            try:
                challenges = self.client.challenges.list()
                for challenge in challenges:
                    if challenge['status'] == 'created' and challenge['challenger']['id'] != self.username:
                        self.client.challenges.accept(challenge['id'])
                        print(f"已接受来自 {challenge['challenger']['name']} 的挑战")
                        return
            except Exception as e:
                print(f"接受挑战失败: {e}")
    
    def get_ongoing_game(self):
        """
        获取当前正在进行的游戏
        
        返回:
            dict: 游戏信息，如果没有正在进行的游戏则返回None
        """
        try:
            ongoing_games = self.client.games.get_ongoing()
            if ongoing_games:
                return ongoing_games[0]  # 返回第一个正在进行的游戏
            return None
        except Exception as e:
            print(f"获取正在进行的游戏失败: {e}")
            return None
    
    def stream_game_state(self, game_id):
        """
        流式获取游戏状态
        
        参数:
            game_id (str): 游戏ID
        """
        try:
            for event in self.client.board.stream_game_state(game_id):
                if event['type'] == 'gameFull':
                    # 游戏开始
                    self.handle_game_start(event)
                elif event['type'] == 'gameState':
                    # 游戏状态更新
                    if self.handle_game_state(event):
                        # 如果游戏结束，退出循环
                        break
        except Exception as e:
            print(f"流式获取游戏状态失败: {e}")
    
    def handle_game_start(self, event):
        """
        处理游戏开始事件
        
        参数:
            event (dict): 游戏开始事件
        """
        self.current_game = event
        self.board = chess.Board()
        
        # 打印详细的事件信息以便调试
        print("\n游戏开始事件详情:")
        print(f"事件类型: {event['type']}")
        
        # 确定我的颜色（增强版本，带有详细日志和错误处理）
        try:
            # 检查白方信息
            if 'white' in event and 'id' in event['white']:
                print(f"白方ID: {event['white']['id']}")
                print(f"当前用户: {self.username}")
                
                if event['white']['id'].lower() == self.username.lower():
                    self.my_color = chess.WHITE
                    print("我执白棋 (chess.WHITE)")
                else:
                    # 检查黑方信息
                    if 'black' in event and 'id' in event['black']:
                        print(f"黑方ID: {event['black']['id']}")
                        
                        if event['black']['id'].lower() == self.username.lower():
                            self.my_color = chess.BLACK
                            print("我执黑棋 (chess.BLACK)")
                        else:
                            print("警告: 我既不是白方也不是黑方，默认设置为黑棋")
                            self.my_color = chess.BLACK
                    else:
                        print("警告: 事件中没有完整的黑方信息，默认设置为黑棋")
                        self.my_color = chess.BLACK
            else:
                print("警告: 事件中没有完整的白方信息，尝试从黑方信息确定颜色")
                
                # 尝试从黑方信息确定颜色
                if 'black' in event and 'id' in event['black']:
                    if event['black']['id'] == self.username:
                        self.my_color = chess.BLACK
                        print("我执黑棋 (chess.BLACK)")
                    else:
                        self.my_color = chess.WHITE
                        print("我执白棋 (chess.WHITE)")
                else:
                    print("警告: 事件中没有完整的黑方信息，默认设置为黑棋")
                    self.my_color = chess.BLACK
        except Exception as e:
            print(f"确定颜色时出错: {e}")
            print("默认设置为黑棋")
            self.my_color = chess.BLACK
        
        # 打印最终确定的颜色
        print(f"最终确定的颜色: {'白棋' if self.my_color == chess.WHITE else '黑棋'}")
        
        # 如果我是白棋，先走一步
        if self.my_color == chess.WHITE:
            self.make_move()
    
    def handle_game_state(self, event):
        """
        处理游戏状态更新事件
        
        参数:
            event (dict): 游戏状态更新事件
        
        返回:
            bool: 如果游戏结束则返回True，否则返回False
        """
        # 更新棋盘状态
        moves = event['moves'].split()
        
        # 打印当前游戏状态信息
        print("\n游戏状态更新:")
        print(f"当前移动序列: {event['moves']}")
        print(f"移动数量: {len(moves)}")
        
        # 重置棋盘并应用所有移动
        self.board = chess.Board()
        for move_uci in moves:
            try:
                move = chess.Move.from_uci(move_uci)
                self.board.push(move)
            except ValueError:
                print(f"无效的移动: {move_uci}")
        
        # 检查游戏是否结束
        if 'status' in event and event['status'] != 'started':
            print(f"游戏结束，状态: {event['status']}")
            return True
        
        # 打印当前棋盘状态和颜色信息
        current_turn = "白棋" if self.board.turn == chess.WHITE else "黑棋"
        my_color_str = "白棋" if self.my_color == chess.WHITE else "黑棋"
        print(f"当前轮到: {current_turn} (self.board.turn = {self.board.turn})")
        print(f"我的颜色: {my_color_str} (self.my_color = {self.my_color})")
        
        # 如果轮到我走棋
        is_my_turn = (self.board.turn == chess.WHITE and self.my_color == chess.WHITE) or \
                     (self.board.turn == chess.BLACK and self.my_color == chess.BLACK)
        print(f"是否轮到我走棋: {is_my_turn}")
        
        if is_my_turn:
            print("现在轮到我走棋，开始计算最佳走法...")
            self.make_move()
        else:
            print("现在轮到对手走棋，等待对手行动...")
        
        return False
    
    def make_move(self):
        """
        计算并执行最佳走法
        """
        if self.board.is_game_over():
            print("游戏已结束")
            return
        
        print("计算最佳走法...")
        # 使用国际象棋引擎计算最佳走法
        think_time = getattr(self, 'think_time', 2.0)  # 默认为2秒
        result = self.engine.play(self.board, chess.engine.Limit(time=think_time))
        best_move = result.move
        
        # 执行最佳走法
        try:
            self.board.push(best_move)
            self.client.board.make_move(self.current_game['id'], best_move.uci())
            print(f"已执行走法: {best_move.uci()}")
        except Exception as e:
            print(f"执行走法失败: {e}")
    
    def run(self):
        """
        运行机器人
        """
        try:
            while True:
                # 获取当前正在进行的游戏
                game = self.get_ongoing_game()
                
                if game:
                    print(f"正在进行游戏: {game['gameId']}")
                    # 流式获取游戏状态
                    self.stream_game_state(game['gameId'])
                else:
                    # 如果没有正在进行的游戏，开始一个新游戏
                    self.start_game()
                    # 等待一段时间，避免过于频繁地请求
                    time.sleep(5)
        except KeyboardInterrupt:
            print("程序已停止")
        finally:
            # 关闭国际象棋引擎
            if hasattr(self, 'engine'):
                self.engine.quit()
    
    def reload_config(self):
        """
        重新加载配置
        """
        try:
            import importlib
            import config
            importlib.reload(config)
            from config import GAME_SETTINGS, LICHESS_API_TOKEN, ENGINE_PATH
            # 更新配置
            self.game_settings = GAME_SETTINGS
            print("配置已重新加载")
            # 打印当前配置信息
            self.print_config()
        except Exception as e:
            print(f"重新加载配置失败: {e}")
    
    def print_config(self):
        """
        打印当前配置信息
        """
        print("\n当前配置信息:")
        print(f"Lichess API令牌: {LICHESS_API_TOKEN[:5]}...{LICHESS_API_TOKEN[-5:]}")
        print(f"引擎路径: {ENGINE_PATH}")
        print("游戏设置:")
        for key, value in GAME_SETTINGS.items():
            print(f"  {key}: {value}")
    
    def _convert_game_settings(self, settings):
        """
        转换游戏设置格式，处理带点的键名
        """
        result = {}
        for key, value in settings.items():
            if '.' in key:
                parts = key.split('.')
                if parts[0] not in result:
                    result[parts[0]] = {}
                result[parts[0]][parts[1]] = value
            else:
                result[key] = value
        return result


if __name__ == "__main__":
    try:
        from config import LICHESS_API_TOKEN, ENGINE_PATH, GAME_SETTINGS, ENGINE_THINK_TIME
    except ImportError as e:
        print(f"错误: {e}")
        print("请确保config.py文件包含所有必要的配置变量")
        exit(1)
    
    # 如果ENGINE_PATH未定义，使用None
    engine_path = ENGINE_PATH if 'ENGINE_PATH' in globals() else None
    
    # 创建机器人
    bot = LichessBot(LICHESS_API_TOKEN, engine_path, GAME_SETTINGS)
    bot.think_time = ENGINE_THINK_TIME  # 设置思考时间
    
    # 打印当前配置
    print("\n当前配置信息:")
    print(f"Lichess API令牌: {LICHESS_API_TOKEN[:5]}...{LICHESS_API_TOKEN[-5:]}")
    print(f"引擎路径: {ENGINE_PATH}")
    print("游戏设置:")
    for key, value in GAME_SETTINGS.items():
        print(f"  {key}: {value}")
    
    # 运行机器人
    bot.run()