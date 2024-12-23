import os
import asyncio
from telethon import TelegramClient, events
from telethon.errors import SessionPasswordNeededError

from data import api_id, api_hash  # 确保 data.py 中定义了 api_id 和 api_hash

# 会话名称，可以自己取一个用来保存 session，如 "my_session"
session_name = 'my_session'
print(f"Session file will be: {os.path.abspath(session_name + '.session')}")

# 创建客户端
client = TelegramClient(session_name, api_id, api_hash)

# 在这里指定你想监听的群组或频道ID
TARGET_CHAT_ID = -1009876543210  # <--- 替换成你想监听的目标群组/频道 ID

# 监听指定群组/频道的新消息事件
@client.on(events.NewMessage(chats=TARGET_CHAT_ID))
async def handler(event):
    try:
        sender = await event.get_sender()
        sender_name = sender.username if sender.username else (sender.first_name or "无名氏")
        message_text = event.message.message

        log_line = f"[{sender_name}] {message_text}\n"
        print(log_line, end='')  # 打印到控制台

        # 将新消息写入到 log.txt 文件（追加写入）
        with open("log.txt", 'a', encoding='utf-8') as f:
            f.write(log_line)
    except Exception as e:
        print(f"处理消息时发生错误: {e}")

async def main():
    print("----- 开始获取所有对话 -----")
    # 获取所有对话（包括群组、私聊、频道等）
    dialogs = await client.get_dialogs()

    print("----- 所有群组/频道列表 -----")
    for dialog in dialogs:
        # 这里仅示例打印：对话标题、ID、以及是否是群组/频道
        # dialog.is_group / dialog.is_channel 可以用于区分
        print(
            f"标题: {dialog.title}, "
            f"ID: {dialog.entity.id}, "
            f"是群组?: {dialog.is_group}, "
            f"是频道?: {dialog.is_channel}"
        )

    print("---------------------------------")
    print("请在上面列表中找出你想监听的群组或频道 ID，将它填到下面的变量中。")
    print("然后保存脚本并重新运行。")

if __name__ == '__main__':
    async def run():
        await client.connect()
        if not await client.is_user_authorized():
            phone = input('Please enter your phone (in international format, e.g., +8618175968252): ')
            try:
                await client.send_code_request(phone)
                code = input('Please enter the code you received: ')
                try:
                    await client.sign_in(phone, code)
                except SessionPasswordNeededError:
                    password = input('Two-step verification is enabled. Please enter your password: ')
                    await client.sign_in(password=password)
                print("登录成功!")
            except Exception as e:
                print(f"发生错误: {e}")
                return

        # 如果目标 ID 未设置，获取并提示用户设置
        if TARGET_CHAT_ID == 1234567890:
            await main()
            print("请在脚本中设置 TARGET_CHAT_ID 后重新运行。")
        else:
            print("开始监听新消息...")
            try:
                await client.run_until_disconnected()
            except KeyboardInterrupt:
                print("脚本已手动终止.")
            except Exception as e:
                print(f"监听过程中发生错误: {e}")

    asyncio.run(run())
