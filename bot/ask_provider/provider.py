import asyncio
import g4f

_providers = {
    "Liaobots": g4f.Provider.Liaobots,
    "Phind": g4f.Provider.Phind,
    "ChatBase": g4f.Provider.ChatBase,
    "Bing": g4f.Provider.Bing,
    "GptGo": g4f.Provider.GptGo,
    "You": g4f.Provider.You,
}


async def ask_provider(provider: g4f.Provider.BaseProvider, text: str):
    try:
        response = await g4f.ChatCompletion.create_async(
            model=g4f.models.default,
            messages=[{"role": "user", "content": text}],
            provider=provider,
        )
        return f"{provider.__name__}:{response}"
    except Exception as e:
        return f"Вибачте, не зміг обробити ваш запит, спробуйте трохи змінити його."
