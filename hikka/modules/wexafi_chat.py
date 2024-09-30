# meta developer: @wexafibio
from os import remove

from telethon.errors import (
    BotGroupsBlockedError,
    ChannelPrivateError,
    ChatAdminRequiredError,
    ChatWriteForbiddenError,
    InputUserDeactivatedError,
    MessageTooLongError,
    UserAlreadyParticipantError,
    UserBlockedError,
    UserIdInvalidError,
    UserKickedError,
    UserNotMutualContactError,
    UserPrivacyRestrictedError,
    YouBlockedUserError,
)

from telethon.tl.functions.channels import InviteToChannelRequest, LeaveChannelRequest
from telethon.tl.functions.messages import AddChatUserRequest
from telethon.tl.types import (
    ChannelParticipantCreator,
    ChannelParticipantsAdmins,
    ChannelParticipantsBots,
    PeerChat,
)
import os
from datetime import datetime

from telethon.tl.functions.channels import GetFullChannelRequest, GetParticipantsRequest
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.functions.photos import GetUserPhotosRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import (
    ChannelParticipantsAdmins,
    MessageActionChannelMigrateFrom,
    UserStatusOnline,
)
from .. import loader, utils
import asyncio
from datetime import datetime
import logging
from .. import loader, utils
from telethon.tl.functions.channels import JoinChannelRequest


@loader.tds
class wexafi_chat(loader.Module):
    """Чат модули"""

    strings = {"name": "wexafi_chat",
               "loading_stats": "<b><emoji document_id=5326015457155620929>🔄</emoji> Загрузка статистики...</b>",
               }
    async def client_ready(self, client, db):
        self.db = db
        self._client = client

    async def useridcmd(self, message):
        """ID выбранного пользователя."""
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()

        try:
            if args:
                user = await message.client.get_entity(
                    args if not args.isdigit() else int(args)
                )
            else:
                user = await message.client.get_entity(
                    reply.sender_id if reply else message.sender_id
                )
        except ValueError:
            user = await message.client.get_entity(message.sender_id)

        await message.edit(
            f"<b>Имя:</b> <code>{user.first_name}</code>\n"
            f"<b>ID:</b> <code>{user.id}</code>"
        )

    async def chatidcmd(self, message):
        """ID чата."""
        if not message.is_private:
            args = utils.get_args_raw(message)
            to_chat = None

            try:
                if args:
                    to_chat = args if not args.isdigit() else int(args)
                else:
                    to_chat = message.chat_id

            except ValueError:
                to_chat = message.chat_id

            chat = await message.client.get_entity(to_chat)

            await message.edit(
                f"<b>Название:</b> <code>{chat.title}</code>\n"
                f"<b>ID</b>: <code>{chat.id}</code>"
            )
        else:
            return await message.edit("<b>Это не чат!</b>")


    async def leavecmd(self, message):
        """Чтобы выйти из чата."""
        args = utils.get_args_raw(message)
        if not message.is_private:
            if args:
                await message.edit(f"<b>До связи.\nПричина: {args}</b>")
            else:
                await message.edit("<b>Пока.</b>")
            await message.client(LeaveChannelRequest(message.chat_id))
        else:
            return await message.edit("<b>Это не чат!</b>")

    async def userscmd(self, message):
        """Список всех пользователей в чате."""
        if not message.is_private:
            await message.edit("<b>Считаем...</b>")
            args = utils.get_args_raw(message)
            info = await message.client.get_entity(message.chat_id)
            title = info.title or "этом чате"

            if not args:
                users = await message.client.get_participants(message.chat_id)
                mentions = f'<b>Пользователей в "{title}": {len(users)}</b> \n'
            else:
                users = await message.client.get_participants(
                    message.chat_id, search=f"{args}"
                )
                mentions = (
                    f'<b>В чате "{title}" найдено {len(users)} пользователей с именем'
                    f" {args}:</b> \n"
                )

            for user in users:
                if not user.deleted:
                    mentions += (
                        f'\n• <a href ="tg://user?id={user.id}">{user.first_name}</a> |'
                        f" <code>{user.id}</code>"
                    )
                else:
                    mentions += f"\n• Удалённый аккаунт <b>|</b> <code>{user.id}</code>"

            try:
                await message.edit(mentions)
            except MessageTooLongError:
                await message.edit(
                    "<b>Черт, слишком большой чат. Загружаю список пользователей в"
                    " файл...</b>"
                )
                file = open("userslist.md", "w+")
                file.write(mentions)
                file.close()
                await message.client.send_file(
                    message.chat_id,
                    "userslist.md",
                    caption="<b>Пользователей в {}:</b>".format(title),
                    reply_to=message.id,
                )
                remove("userslist.md")
                await message.delete()
        else:
            return await message.edit("<b>Это не чат!</b>")

    async def adminscmd(self, message):
        """Список всех админов в чате."""
        if not message.is_private:
            await message.edit("<b>Считаем...</b>")
            info = await message.client.get_entity(message.chat_id)
            title = info.title or "this chat"

            admins = await message.client.get_participants(
                message.chat_id, filter=ChannelParticipantsAdmins
            )
            mentions = f'<b>Админов в "{title}": {len(admins)}</b>\n'

            for user in admins:
                admin = admins[
                    admins.index((await message.client.get_entity(user.id)))
                ].participant
                if not admin:
                    if type(admin) == ChannelParticipantCreator:
                        rank = "creator"
                    else:
                        rank = "admin"
                else:
                    rank = admin.rank or "admin"

                if not user.deleted:
                    mentions += (
                        f'\n• <a href="tg://user?id={user.id}">{user.first_name}</a> |'
                        f" {rank} | <code>{user.id}</code>"
                    )
                else:
                    mentions += f"\n• Удалённый аккаунт <b>|</b> <code>{user.id}</code>"

            try:
                await message.edit(mentions)
            except MessageTooLongError:
                await message.edit(
                    "Черт, слишком много админов здесь. Загружаю список админов в"
                    " файл..."
                )
                file = open("adminlist.md", "w+")
                file.write(mentions)
                file.close()
                await message.client.send_file(
                    message.chat_id,
                    "adminlist.md",
                    caption='<b>Админов в "{}":<b>'.format(title),
                    reply_to=message.id,
                )
                remove("adminlist.md")
                await message.delete()
        else:
            return await message.edit("<b>Это не чат!</b>")
        
    async def smcmd(self, message):
        """Используй: .sm «название» чтобы найти музыку по названию."""
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()
        if not args:
            return await message.edit("<b>Нету аргументов.</b>")
        try:
            await message.edit("<b>Загрузка...</b>")
            music = await message.client.inline_query("lybot", args)
            await message.delete()
            await message.client.send_file(
                message.to_id,
                music[0].result.document,
                reply_to=reply.id if reply else None,
            )
        except:
            return await message.client.send_message(
                message.chat_id,
                f"<b>Музыка с названием <code>{args}</code> не найдена.</b>",
            )

    async def botscmd(self, message):
        """Список всех ботов в чате."""
        if not message.is_private:
            await message.edit("<b>Считаем...</b>")

            info = await message.client.get_entity(message.chat_id)
            title = info.title if info.title else "this chat"

            bots = await message.client.get_participants(
                message.to_id, filter=ChannelParticipantsBots
            )
            mentions = f'<b>Ботов в "{title}": {len(bots)}</b>\n'

            for user in bots:
                if not user.deleted:
                    mentions += (
                        f'\n• <a href="tg://user?id={user.id}">{user.first_name}</a> |'
                        f" <code>{user.id}</code>"
                    )
                else:
                    mentions += f"\n• Удалённый бот <b>|</b> <code>{user.id}</code>"

            try:
                await message.edit(mentions, parse_mode="html")
            except MessageTooLongError:
                await message.edit(
                    "Черт, слишком много ботов здесь. Загружаю список ботов в файл..."
                )
                file = open("botlist.md", "w+")
                file.write(mentions)
                file.close()
                await message.client.send_file(
                    message.chat_id,
                    "botlist.md",
                    caption='<b>Ботов в "{}":</b>'.format(title),
                    reply_to=message.id,
                )
                remove("botlist.md")
                await message.delete()
        else:
            return await message.edit("<b>Это не чат!</b>")
        
    @loader.command()
    async def stats(self, message):
            """𝚝𝚎𝚕𝚎𝚐𝚛𝚊𝚖 𝚊𝚌𝚌𝚘𝚞𝚗𝚝 𝚜𝚝𝚊𝚝𝚒𝚜𝚝𝚒𝚌𝚜"""

            await utils.answer(message, self.strings['loading_stats'])
            u_chat = 0
            b_chat = 0
            c_chat = 0
            ch_chat = 0
            all_chats = 0

            async for dialog in self._client.iter_dialogs():
                all_chats += 1
                if dialog.is_user:
                    if dialog.entity.bot:
                        b_chat += 1
                    elif not dialog.entity.bot:
                        u_chat += 1
                elif dialog.is_group:
                    c_chat += 1
                elif dialog.is_channel:
                    if dialog.entity.megagroup or dialog.entity.gigagroup:
                        if dialog.entity.megagroup:
                            c_chat += 1
                        elif dialog.entity.gigagroup:
                            c_chat += 1
                    elif not dialog.entity.megagroup and not dialog.entity.gigagroup:
                        ch_chat += 1
            await utils.answer(message,
    f"""<b><emoji document_id=5370740407602782301>✝️</emoji> 𝚖𝚢 𝚜𝚝𝚊𝚝𝚒𝚜𝚝𝚒𝚌𝚜 𝚒𝚗 𝚝𝚎𝚕𝚎𝚐𝚛𝚊𝚖

    <emoji document_id=6028338546736107668>⭐️</emoji> 𝚝𝚘𝚝𝚊𝚕 𝚌𝚑𝚊𝚝𝚜: <code>{all_chats}</code>

    <emoji document_id=6037249452824072506>🔒</emoji> <code>{u_chat}</code> 𝚙𝚎𝚛𝚜𝚘𝚗𝚊𝚕 𝚌𝚑𝚊𝚝𝚜
    <emoji document_id=5879905000972358125>👥</emoji> <code>{c_chat}</code> 𝚐𝚛𝚘𝚞𝚙𝚜
    <emoji document_id=6021418126061605425>📢</emoji> <code>{ch_chat}</code> 𝚌𝚑𝚊𝚗𝚗𝚎𝚕𝚜
    <emoji document_id=5258093637450866522>🤖</emoji> <code>{b_chat}</code> 𝚋𝚘𝚝𝚜</b>""")
            
