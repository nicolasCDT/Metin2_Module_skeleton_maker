#!/usr/bin/python

#  Copyright (c) 2022, Takuma.
#  Respect intellectual property, and do not delete these comments.

# -*- coding: <utf-8> -*-

from skeleton_maker.CONSTANTS import *
from typing import TypeVar

# Used by self typing
arg: TypeVar = TypeVar("arg", bound="Argument")


class Argument:
	"""Representation of a method's argument"""
	def __init__(self: arg, name: AnyStr, arg_type: Type) -> None:
		"""Class initialization"""
		self._name: AnyStr = f"_{name}" if name in RESERVED_KEYWORD else name
		self._arg_type: Type = arg_type

	def render(self: arg) -> AnyStr:
		"""Generate Python representation"""
		return f"{self._name}: {self._arg_type.__name__}"

	def __str__(self: arg) -> AnyStr:
		"""String representation"""
		return f"{self._name}: {self._arg_type.__name__} "

	def __repr__(self: arg) -> AnyStr:
		"""String representation"""
		return f"{self._name}: {self._arg_type.__name__} "
