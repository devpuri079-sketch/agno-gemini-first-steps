import chainlit as cl
from agno.agent import Agent
from agno.models.google import Gemini
from agno.media import Image
from dotenv import load_dotenv
from agno.db.in_memory import InMemoryDb
from agno.agent import RunEvent
from csv_db import register_to_csv, search_in_csv

load_dotenv()


@cl.on_chat_start
async def on_chat_start():

    agent = Agent(
        model=Gemini(id="gemini-2.0-flash"),
        description="あなたは、さまざまな分野で人々を支援する有能なAIエージェントです。",
        instructions=[
            "内容をよく理解し、正確かつ丁寧に回答してください。",
            "ツールの呼び出しは、ユーザーの入力内容に応じて適切なタイミングで行ってください。",
        ],
        db=InMemoryDb(),
        add_history_to_context=True,
        tools=[register_to_csv, search_in_csv],
    )

    cl.user_session.set("agent", agent)


@cl.on_message
async def on_message(message: cl.Message):
    content_started = False
    images = [
        Image(filepath=file.path) for file in message.elements if "image" in file.mime
    ]

    agent = cl.user_session.get("agent")

    msg = cl.Message(content="")
    async for chunk in agent.arun(
        message.content,  # ユーザーからの入力メッセージ（テキスト）
        images=images,  # 添付された画像（Imageオブジェクトのリスト）
        stream=True,  # モデルの応答をチャンク（分割）で受け取るかどうか（Trueならストリーミング）
        stream_events=True,  # ツール呼び出しなどのイベントもチャンクとして受け取るかどうか
    ):
        if chunk.event in [RunEvent.run_started, RunEvent.run_completed]:
            print(f"\nEVENT: {chunk.event}")

        if chunk.event in [RunEvent.tool_call_started]:
            print(f"\nEVENT: {chunk.event}")
            print(f"TOOL CALL: {chunk.tool.tool_name}")  # type: ignore
            print(f"TOOL CALL ARGS: {chunk.tool.tool_args}")  # type: ignore

        if chunk.event in [RunEvent.tool_call_completed]:
            print(f"\nEVENT: {chunk.event}")
            print(f"TOOL CALL: {chunk.tool.tool_name}")  # type: ignore
            print(f"TOOL CALL RESULT: {chunk.tool.result}")  # type: ignore

        if chunk.event in [RunEvent.run_content]:
            if not content_started:
                print("\nCONTENT:")
                content_started = True
            else:
                print(chunk.content, end="")

            await msg.stream_token(getattr(chunk, "content", str(chunk)))

    await msg.send()
