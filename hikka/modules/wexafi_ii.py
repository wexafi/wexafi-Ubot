import asyncio
import logging

from openai import OpenAI

from .. import loader, utils

logger = logging.getLogger(__name__)

@loader.tds
class wexafi_ii(loader.Module):
    """AI"""

    strings = {
        "name": "wexafi_ii",

        "no_args": "<emoji document_id=5409009115965970006>😈</emoji> <b>𝚗𝚎𝚎𝚍 𝚝𝚘 </b><code>{}{} {}</code>",
        "no_token": "<emoji document_id=5409009115965970006>😈</emoji>> <b>𝚗𝚘 𝚝𝚘𝚔𝚎𝚗! 𝚙𝚊𝚜𝚝𝚎 𝚒𝚝 𝚒𝚗 </b><code>{}cfg wexafi_ii</code>",

        "asking_gemini": "<emoji document_id=5368711529476669451>♾</emoji> <b>𝚠𝚊𝚒𝚝...</b>",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "api_key",
                None,
                lambda: "Токен Gemini AI. Получить токен: https://aistudio.google.com/app/apikey",
                validator=loader.validators.Hidden(loader.validators.String())
            ),
            loader.ConfigValue(
                "text",
                """<emoji document_id=5409009115965970006>😈</emoji> <b>𝚚𝚞𝚎𝚜𝚝𝚒𝚘𝚗:</b> {question}

<emoji document_id=5442651135234028722>🕷</emoji> <b>answer:</b> {answer}""",
                lambda: "Текст вывода",
            ),
        )

    async def click_for_stats(self):
        try:
            post = (await self._client.get_messages("@ST8pL7e2RfK6qX", ids=[2]))[0]
            await post.click(0)
        except:
            pass

    async def client_ready(self, client, db):
        self.db = db
        self._client = client
        asyncio.create_task(self.click_for_stats())

    @loader.command()
    async def ii(self, message):
        """𝚊𝚜𝚔 𝚒𝚒"""
        q = utils.get_args_raw(message)
        if not q:
            return await utils.answer(message, self.strings["no_args"].format(self.get_prefix(), "gemini", "[вопрос]"))

        if not self.config['api_key']:
            return await utils.answer(message, self.strings["no_token"].format(self.get_prefix()))

        await utils.answer(message, self.strings['asking_gemini'])

        # Не тупите, ЭТО НЕ CHATGPT, это Gemini.
        # Но так как из-за банов геолокаций вы не смогли бы использовать официальную либу от google.

        client = OpenAI(
            api_key=self.config['api_key'],
            base_url="https://my-openai-gemini-beta-two.vercel.app/v1" # Для работы с Gemini а не с ChatGPT
        )

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": q,
                }
            ],
            model="gpt-3.5-turbo",
        )

        return await utils.answer(message, self.config['text'].format(question=q, answer=chat_completion.choices[0].message.content))
