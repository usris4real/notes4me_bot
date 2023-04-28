import asyncio

import uvicorn

from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import PlainTextResponse, Response

from telegram import Update

from telegram.ext import (
    Application,
    CommandHandler
)

from data import config as _config
from log_utils import CustomLogger

import handlers

# Enable logging
logger = CustomLogger()

# Create FastAPI app
app = FastAPI()


async def main() -> None:
    """Set up the FastAPI app and uvicorn webserver."""

    url = _config.BASE_URL
    admin_chat_id = _config.ADMIN
    port = int(_config.APP_PORT)

    # Here we set updater to None because we want our custom webhook server to handle the updates
    # and hence we don't need an Updater instance
    application = Application.builder().token(_config.BOT_TOKEN).updater(None).build()

    # save the values in `bot_data` such that we may easily access them in the callbacks
    application.bot_data["url"] = url
    application.bot_data["admin_chat_id"] = admin_chat_id
    application.bot_data['fastapi_app'] = app

    # register handlers
    application.add_handler(CommandHandler("start", handlers.start))

    # Pass webhook settings to telegram
    await application.bot.set_webhook(url=f"{_config.WEBHOOK_URL}")

    # Set up webserver
    @app.on_event("startup")
    async def startup_events() -> None:
        logger.info('Bot successfully started!')

    @app.post("/telegram")
    async def telegram(request: Request) -> Response:
        """Handle incoming Telegram updates by putting them into the `update_queue`"""
        update_data = str(await request.json())
        log_text = f'New Update: {update_data}'
        logger.info(log_text)

        await application.update_queue.put(
            Update.de_json(data=await request.json(), bot=application.bot)
        )
        return Response()

    @app.get("/healthcheck")
    async def health(_: Request) -> PlainTextResponse:
        """For the health endpoint, reply with a simple plain text message."""
        return PlainTextResponse(content="The bot is still running fine :)")

    webserver = uvicorn.Server(
        config=uvicorn.Config(
            app=app,
            port=port,
            use_colors=True,
            host="127.0.0.1",
        )
    )

    # Run application and webserver together
    async with application:
        await application.start()
        await webserver.serve()
        await application.stop()


if __name__ == "__main__":
    asyncio.run(main())
