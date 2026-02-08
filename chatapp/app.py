import chainlit as cl
from agno.agent import Agent
from agno.models.google import Gemini
from agno.media import Image
from dotenv import load_dotenv
from agno.db.in_memory import InMemoryDb

load_dotenv()


@cl.on_chat_start
async def on_chat_start():

    agent = Agent(
        model=Gemini(id="gemini-2.5-flash"),
        description="あなたは、さまざまな分野で人々を支援する有能なAIエージェントです。",
        instructions=["内容をよく理解し、正確かつ丁寧に回答してください。"],
        db=InMemoryDb(),
        add_history_to_context=True,
    )

    cl.user_session.set("agent", agent)


@cl.on_message
async def on_message(message: cl.Message):

    images = [
        Image(filepath=file.path) for file in message.elements if "image" in file.mime
    ]

    agent = cl.user_session.get("agent")

    msg = cl.Message(content="")
    async for chunk in agent.arun(
        message.content,  # ユーザーからの入力メッセージ（テキスト）
        images=images,  # 添付された画像（Imageオブジェクトのリスト）
        stream=True,  # モデルの応答をチャンク（分割）で受け取るかどうか（Trueならストリーミング）
    ):

        await msg.stream_token(getattr(chunk, "content", str(chunk)))

    await msg.send()
