#!/usr/bin/python

#  Copyright (c) 2022, Takuma.
#  Respect intellectual property, and do not delete these comments.

# -*- coding: <utf-8> -*-

from typing import *

# Used by self typing
co: TypeVar = TypeVar("co", bound="Constant")


class Constant:
	"""Represent a constant"""
	def __init__(self: co, name: AnyStr, constant_type: Type) -> None:
		"""Initialization of Constant class"""
		self._name: AnyStr = name
		self._constant_type: Type = constant_type

	def get_name(self: co) -> AnyStr:
		"""Return the constant's name"""
		return self._name

	def render(self: co) -> AnyStr:
		"""Generate Python representation"""
		return "{}: {} = {}".format(
			self._name,
			self._constant_type.__name__,
			self._constant_type.__name__ + "()"
		)
