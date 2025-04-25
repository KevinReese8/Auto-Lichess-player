# Lichess 自动对弈机器人

这个项目是一个自动化的国际象棋机器人，可以连接到 lichess.org 并自动进行对弈。它能够读取棋盘状况，使用国际象棋引擎计算最佳走法，并自动在 lichess.org 上执行这些走法。当一局游戏结束后，它会自动开始新的对局。

## 功能特点

- 自动连接到 lichess.org API
- 读取当前棋盘状况
- 使用国际象棋引擎（如 Stockfish）计算最佳走法
- 自动在 lichess.org 上执行走法
- 一局结束后自动开始新的对局

## 安装要求

- Python 3.6 或更高版本
- 国际象棋引擎（推荐使用 Stockfish）
- Lichess API 令牌

## 安装步骤

1. 克隆或下载此仓库

2. 安装所需的 Python 依赖包：

```bash
pip install python-chess berserk
```

3. 下载并安装 Stockfish 国际象棋引擎：
   - 从 [Stockfish 官网](https://stockfishchess.org/download/) 下载适合您操作系统的版本
   - 将下载的引擎文件放在项目的 `stockfish` 目录下
   - 确保引擎文件具有执行权限（在 macOS/Linux 上使用 `chmod +x stockfish-xxx`）

4. 获取 Lichess API 令牌：
   - 登录您的 Lichess 账户
   - 访问 https://lichess.org/account/oauth/token
   - 创建一个新的访问令牌，确保它具有以下权限：
     - 读取偏好设置
     - 读取电子邮件地址
     - 在网站上下棋
     - 挑战 AI 和真人玩家

5. 配置您的 API 令牌：
   - 打开 `config.py` 文件
   - **将您的 Lichess API 令牌替换 `LICHESS_API_TOKEN` 变量的值**
   - 如果需要，设置 `ENGINE_PATH` 变量为您的国际象棋引擎路径

## 使用方法

1. 确保您已完成所有安装步骤

2. 运行机器人：

```bash
python lichess_bot.py
```

3. 机器人将自动连接到 Lichess，创建一个新的对局或接受现有的挑战，并开始下棋

4. 要停止机器人，按 `Ctrl+C`

## 自定义设置

您可以在 `config.py` 文件中修改以下设置：

- `ENGINE_PATH`：国际象棋引擎的路径
- `ENGINE_THINK_TIME`：引擎思考时间（秒）
- `GAME_SETTINGS`：游戏设置，包括时钟设置、游戏变体和颜色选择

## 注意事项

- 请遵守 Lichess 的服务条款和 API 使用政策
- 不要过于频繁地创建和放弃游戏，这可能会导致您的账户被限制
- 确保您的国际象棋引擎路径正确设置

## 故障排除

- 如果遇到 "找不到国际象棋引擎" 错误，请检查您的引擎路径是否正确
- 如果遇到 API 连接问题，请确保您的 API 令牌有效且具有正确的权限
- 如果机器人无法创建新游戏，请检查您的网络连接和 Lichess 服务状态
