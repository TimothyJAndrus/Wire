#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

sys.path.append("/home/jacobsin/wire")

import wire


class PersonalPage(wire.Page):

    url = "http://jacobsin.xyz"

    elements = {
        "topHero": ".hero",
        "autoHero": [".hero", 1],
        "devHero": [".hero", 2],
        "openHero": [".hero", 3],
        "formHero": [".hero", 4],
        "footer": ".footer",
    }


def main():
    with wire.Chrome(True) as b:
        personalpage = PersonalPage(b)
        print(dir(personalpage))
        print(type(personalpage.topHero))


main()
