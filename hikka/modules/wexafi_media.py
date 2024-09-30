from .. import loader
# meta developer: @wexafibio


@loader.tds
class wexafi_media(loader.Module):
    """Голосовые сообщения от wexafi"""

    strings = {"name": "wexafi_media"}

    async def васяcmd(self, message):
        """ - Вася не дрочи судьбу→"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/wexafi_gs/16",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def дапиздыcmd(self, message):
        """ - Да мне Да мне до пизды→"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/wexafi_gs/17",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return
    
    async def рускиеcmd(self, message):
        """ - А нам и че→"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/wexafi_gs/18",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return
    
    async def пёсcmd(self, message):
        """ - А вы помолчите→"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/wexafi_gs/19",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return
    
    async def буквыcmd(self, message):
        """ - Иди ты→"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/wexafi_gs/20",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return
    
    async def пареньcmd(self, message):
        """ - Ищю парня→"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/wexafi_gs/21",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return
    
    async def завалиcmd(self, message):
        """ - Да все завали свой→"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/wexafi_gs/22",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return
    
    async def материcmd(self, message):
        """ - Я щас твоей матери→"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/wexafi_gs/23",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return
    
    async def монашкаcmd(self, message):
        """ - Слыш кончай на публику→"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/wexafi_gs/24",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return
    
    async def пожалуйстаcmd(self, message):
        """ - Ну пожалуйста→"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/wexafi_gs/25",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return
    
    async def колениcmd(self, message):
        """ - Вставай на колени→"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/wexafi_gs/26",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return
    
    async def убилcmd(self, message):
        """ - Я бы всех ваших родных→"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/wexafi_gs/27",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return
    
    async def долгоегсcmd(self, message):
        """ - Долгое гс→"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/wexafi_gs/28",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def тянкаcmd(self, message):
        """ - Я ТЯНКА→"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/wexafi_gs/29",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return
    
