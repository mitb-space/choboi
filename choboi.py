# -*- coding: utf-8 -*-
"""
Supported commands:

@choboi

    herro -> parese

    set LAN party <date> -> save LAN party date
    when's LAN party? -> list LAN party dates

    is <name> a cuck?

    help -> print commands
"""
from choboi import config
from choboi.bot import Bot


def main():
    bot = Bot()
    bot.connect()

if __name__ == '__main__':
    main()
