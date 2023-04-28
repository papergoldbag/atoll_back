

def main():
    from atoll_back.tg_bot.filters import setup_filters
    setup_filters()

    from atoll_back.tg_bot.middleware import setup_middleware
    setup_middleware()

    from atoll_back.tg_bot.handlers import import_handlers
    import_handlers()

    from atoll_back.tg_bot.events import setup_events
    setup_events()

    from atoll_back.core import executor_

    from atoll_back.core import settings
    if settings.tg_bot_use_webhook is False:
        executor_.start_polling(reset_webhook=True)
    else:
        executor_.start_webhook(
            webhook_path=settings.tg_webhook_path,
            host=settings.tg_webhook_host,
            port=settings.tg_bot_webapp_port
        )


if __name__ == '__main__':
    main()
