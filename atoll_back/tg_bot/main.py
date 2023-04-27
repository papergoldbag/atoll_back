def main():
    from atoll_back.tg_bot.filters import setup_filters
    setup_filters()

    from atoll_back.tg_bot.middleware import setup_middleware
    setup_middleware()

    from atoll_back.tg_bot.handlers import import_handlers
    import_handlers()

    from atoll_back.core import executor_
    executor_.start_polling(reset_webhook=True)


if __name__ == '__main__':
    main()
