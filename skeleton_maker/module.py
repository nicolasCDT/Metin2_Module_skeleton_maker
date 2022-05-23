#!/usr/bin/python

#  Copyright (c) 2022, Takuma.
#  Respect intellectual property, and do not delete these comments.

# -*- coding: <utf-8> -*-

from typing import TypeVar, AnyStr, List
from skeleton_maker.method import Method
from skeleton_maker.constant import Constant

# Used by self typing
mo = TypeVar("mo", bound="Module")


class Module:
	"""Represents a Module"""
	def __init__(self: mo, name: AnyStr) -> None:
		"""Initialization of Module class"""
		self._name: AnyStr = name
		self._py_name: AnyStr = str()
		self._methods: List[Method] = list()
		self._constants: List[Constant] = list()
		self._constants_name: List[AnyStr] = list()  # to remove duplicate

	def get_name(self: mo) -> AnyStr:
		"""Returns the module's name"""
		return self._name

	def add_method(self: mo, method: Method) -> None:
		"""Adds a method to the module"""
		self._methods.append(method)

	def add_constant(self: mo, constant: Constant) -> None:
		"""Adds a constant to the module"""
		if not constant.get_name() in self._constants_name:
			self._constants.append(constant)
			self._constants_name.append(constant.get_name())

	def get_methods(self: mo) -> List[Method]:
		"""Returns all module's methods"""
		return self._methods

	def get_constants(self: mo) -> List[Constant]:
		"""Returns all module's constants"""
		return self._constants

	def render(self: mo) -> AnyStr:
		"""Generate Python representation"""
		render: AnyStr = ""

		# Constants
		for constant in self.get_constants():
			render += f"{constant.render()}\n"
		render += "\n\n"

		# Finally, methods :
		for method in self.get_methods():
			render += method.render()
		render += "\n"

		return render
