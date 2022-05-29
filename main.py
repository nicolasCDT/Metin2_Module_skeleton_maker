#!/usr/bin/python

#  Copyright (c) 2022, Takuma.
#  Respect intellectual property, and do not delete these comments.

# -*- coding: <utf-8> -*-

# Imports:
from skeleton_maker import *
from argparse import ArgumentParser


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
	"NewWars"  # Command arguments options
]

from skeleton_maker import CONSTANTS


def parse_args():
	parser = ArgumentParser()
	parser.add_argument('-s', '--source', required=True, type=str, help='Source location path')
	parser.add_argument('-o', '--output', required=True, type=str, help='Output location path')
	parser.add_argument('-f', '--format-snake-case', type=bool, default=True,
	                    help='Formats the functions arguments to snake case style, example: '
	                         'def func(p_arg: int) instead of def func(pArg:int)')
	
	return parser.parse_args()


def main() -> None:
	"""Main entry
	Use this function to start the SkeletonMaker
	"""
	
	args = parse_args()
	CONSTANTS.FORMAT_ARGUMENTS_TO_SNAKE_CASE = args.format_snake_case
	
	print("Welcome !")
	print("I was coded by Takuma! A Frenchman who loves baguettes!")
	print("You can find me on my github: https://github.com/nicolasCDT/")
	maker: SkeletonMaker = SkeletonMaker(args.source, args.output)
	maker.process()

	print("Have a nice day!")


# Main entry
if __name__ == '__main__':
	main()
