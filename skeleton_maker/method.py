#!/usr/bin/python

#  Copyright (c) 2022, Takuma.
#  Respect intellectual property, and do not delete these comments.

# -*- coding: <utf-8> -*-

from skeleton_maker.CONSTANTS import *
from skeleton_maker.argument import Argument
import re
from typing import TypeVar

# Used by self typing
me: TypeVar = TypeVar("me", bound="Method")


class Method:
	"""Represent a method (or function)"""
	def __init__(self: me, py_name: AnyStr, cpp_name: AnyStr, content: AnyStr) -> None:
		"""Initialization of Method class"""
		self._py_name: AnyStr = py_name
		self._cpp_name: AnyStr = cpp_name
		self._content: AnyStr = content
		self._args: Dict[int, Argument] = dict()
		self._can_be_none: bool = False
		self._returns: List[AnyStr] = list()

		# Load content
		self.load()

	def create_new_return(self: me, representation: AnyStr) -> None:
		"""Create python return with c++ representation"""
		# Python representation
		py_representation: AnyStr = str()
		need_to_close_tuple: bool = False  # Have to close prevent Tuple open juste after this line

		# Special case for BuildValue("None")
		if representation == "None":
			self._returns.append("None")
			return

		# Check if return need to be contains in Tuple:
		if len(representation) > 1 and not representation.startswith('('):
			py_representation += "Tuple["
			need_to_close_tuple = True
		# For each letter
		for letter in representation:
			if letter == '(':  # Start a tuple
				py_representation += "Tuple["
			elif letter == ')':  # End a tuple
				py_representation += "]"
			elif letter not in LETTER_TYPE_CORRESPONDENCES.keys():  # Unknown letter
				raise Exception("Can't find representation for letter: {}, name: {}".format(letter, self._cpp_name))
			else:
				if py_representation and not py_representation.endswith('['):  # Add a coma if necessary
					py_representation += ", "
				py_representation += LETTER_TYPE_CORRESPONDENCES[letter].__name__  # Get type and add it

		# Check if we need to close the tuple
		if need_to_close_tuple:
			py_representation += "]"

		# Add to returns
		self._returns.append(py_representation)

	def load(self: me) -> None:
		"""Load informations about method"""
		# Args :
		# For each function to catch args :
		for cpp_function, py_type in FUNCTIONS_TYPE_CORRESPONDENCES.items():
			raw_args: List = re.findall(
				"{}\(.*?,\s*(\d+)\s*,\s*&(\w*)".format(cpp_function),
				self._content
			)
			if raw_args:
				for i, name in raw_args:
					self._args[int(i)] = Argument(name, py_type)

		# Returns :

		# Find all returns
		returns: List = re.findall(
			"Py_BuildValue\(\s*\"([\w()]*)\"",
			self._content
		)
		if returns:
			# Remove duplicates
			returns = list(dict.fromkeys(returns))
			for ret in returns:
				self.create_new_return(ret)

	def render(self: me) -> AnyStr:
		"""Generate Python representation"""
		# Header :
		py_render: AnyStr = f"def {self._py_name}("  # def ...(
		number: int = len(self._args.keys())
		for i in range(number): # Args
			if not py_render.endswith('('):  # Add coma
				py_render += ", "
			py_render += self._args[i].render()
		py_render += ") -> "

		# Return
		if not self._returns:  # If no return -> None
			py_render += "None"
		else:
			if len(self._returns) == 1:  # If only one return
				py_render += self._returns[0]
			else:  # Else, make a Union
				py_render += "Union["
				py_render += ", ".join(self._returns)
				py_render += "]"
		py_render += ":\n"

		# Body
		py_render += "\tpass\n\n\n"

		return py_render
