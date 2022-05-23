#!/usr/bin/python

#  Copyright (c) 2022, Takuma.
#  Respect intellectual property, and do not delete these comments.

# -*- coding: <utf-8> -*-

# Imports:
from skeleton_maker import *


__author__ = "Takuma"
__version__ = "1.1"
__status__ = "development"
__credits__ = [
	"Takuma",  # Original author
	"Gurgarath",  # Regex and metin2 knowledge
	"VegaS",  # Tools to convert Python2 to Python3
	"Mali61",  # Completed functions list
	"Arves100",  # Fixed something forgotten in code
	"msnas"  # Fixed return type (NoReturn -> None)
]


def main() -> None:
	"""Main entry
	Use this function to start the SkeletonMaker
	"""
	print("Welcome !")
	print("I was coded by Takuma! A Frenchman who loves baguettes!")
	print("You can find me on my github: https://github.com/nicolasCDT/")
	maker: SkeletonMaker = SkeletonMaker("src", "bin")
	maker.process()

	print("Have a nice day!")


# Main entry
if __name__ == '__main__':
	main()
