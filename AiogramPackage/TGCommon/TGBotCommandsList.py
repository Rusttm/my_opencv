from aiogram.types import BotCommand

private_commands = [BotCommand(command="start", description="🆕Обновиться"),
                    BotCommand(command="menu", description="🔼Включить меню"),
                    BotCommand(command="hide_menu", description="🔽Выключить меню"),
                    BotCommand(command="admin", description="📃Обновление списка пользователей"),
                    BotCommand(command="upload", description="📥Сохранить файл"),
                    BotCommand(command="download", description="📤Получить файл"),
                    BotCommand(command="records", description="📹Записи камер")]
