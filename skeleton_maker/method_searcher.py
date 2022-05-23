#!/usr/bin/python

#  Copyright (c) 2022, Takuma.
#  Respect intellectual property, and do not delete these comments.

# -*- coding: <utf-8> -*-
import re
from typing import TypeVar, AnyStr, List, Tuple

# Typing for self -> SkeletonMaker
ms = TypeVar("ms", bound="MethodSearcher")


def remove_until(string: AnyStr, marker: AnyStr) -> AnyStr:
	"""Remove all chars in string until string starts with marker"""
	while not string.startswith(marker) and string:  # While don't start with marker and string not empty
		string = string[1:]  # Remove first char
	return string


class MethodSearcher:
	"""Little lexical analyser to parse method in .cpp file. We can't use regex because of backtracking with { and }"""
	def __init__(self: ms, content: AnyStr, start_function_regex: AnyStr) -> None:
		"""Initialization of MethodSearcher class"""
		self._regex = start_function_regex
		self._content: AnyStr = content
		self._methods: List[Tuple[AnyStr, AnyStr]] = list()

	def remove_specials_whitespaces(self: ms) -> None:
		"""Remplace \n, \t and double space with simple space"""
		specials: List[AnyStr] = ["\n", "\t", " "]
		for s in specials:
			self._content = self._content.replace(s, " ")

	def read(self: ms) -> None:
		"""Read content and try to find all the methods who started with the specified regex"""
		# Remove useless char
		self.remove_specials_whitespaces()

		# While script can find method

		while founds := re.findall(self._regex, self._content):
			# Remove previous content to get method at the head of string
			self._content = remove_until(self._content, founds[0])
			name: AnyStr = ""  # Method name
			body: AnyStr = ""  # Method body

			# While content doesn't start with '(' -> Is the method name
			while self._content[0] != "(":
				name += self._content[0]  # Add to name
				self._content = self._content[1:]  # Remove first char

			# Go to method definition with first {
			self._content = remove_until(self._content, "{")[1:]

			stack: List[AnyStr] = ["{"]
			while stack and self._content:
				if self._content[0] == '{':
					stack.append('{')
				elif self._content[0] == '}':
					if stack.pop() != '{':
						raise Exception("Can't parse {}".format(name))
				body += self._content[0]
				self._content = self._content[1:]
			if name and body:
				self._methods.append((name, body))

	def get_methods(self: ms) -> List[Tuple[AnyStr, AnyStr]]:
		"""Return all methods"""
		return self._methods
