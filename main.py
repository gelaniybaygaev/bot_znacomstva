from aiogram import Bot,Dispatcher
import asyncio
from feeling_profile.handlers import router
from show_profiles.handlers import router_show_profiles

bot = Bot("7375974121:AAEXoVnmh1cDmnL3CVOkb48p7838JVRAn08")

dispatcher = Dispatcher()
async def main():
    dispatcher.include_routers(router,router_show_profiles)
    await dispatcher.start_polling(bot)



if __name__ == "__main__":
    asyncio.run(main())





