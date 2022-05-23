#!/usr/bin/python

#  Copyright (c) 2022, Takuma.
#  Respect intellectual property, and do not delete these comments.

# -*- coding: <utf-8> -*-

import os
import re
from skeleton_maker.CONSTANTS import *
from skeleton_maker.method_searcher import MethodSearcher
from typing import Match, Tuple
from skeleton_maker.module import *

# Typing for self -> SkeletonMaker
sf = TypeVar("sf", bound="SourceFile")


def get_header() -> AnyStr:
	return """#!/usr/bin/python

#  Copyright (c) 2022, Takuma.
#  Respect intellectual property, and do not delete these comments.

# -*- coding: <utf-8> -*-

from typing import *"""


class SourceFile:
	"""Representation of a .cpp file.
	SourceFile can read the file, get all the modules and write the skeleton in an output directory
	"""

	def __init__(self: sf, path: AnyStr) -> None:
		"""Initialization of SourceFile"""
		self._path: AnyStr = path
		self._name: AnyStr = os.path.basename(path)
		self._has_module: bool = False
		self._content: AnyStr = str()
		self._modules: List[Module] = list()
		self._methods: Dict[AnyStr, AnyStr] = dict()

	def scan_for_all_methods(self: sf) -> None:
		"""Scan to find all methods."""
		# Get all methods
		# methods: List = re.findall("PyObject\s*\*\s*(.*)\(.*\)\s*{((?:[^{}]+|{([^{}]+)}){3})}", self._content)
		# print(f"Avant: {len(methods)}")

		m = MethodSearcher(self._content, r'PyObject\s*\*\s*(.*)\(.*\)\s*')
		m.read()
		methods: List[Tuple[AnyStr, AnyStr]] = m.get_methods()
		if methods:
			# Add them to methods attribut
			for method in methods:
				# self.methods[NAME] = BODY
				self._methods[method[0]] = method[1]

	def scan_for_module(self: sf, object_name: AnyStr,  module_name: AnyStr, module_dict: AnyStr) -> None:
		"""Scan to find all modules and init a Module object"""
		# Start to find dict block :
		regex: AnyStr = r"static\s*" + MODULE_DICT_TYPE + "\s*" + module_dict
		regex += "\[\]\s*=\s*\{[\s\S]*{\s*(?:NULL)|(?:nullptr)\s*,"

		block: List = re.findall(regex, self._content)

		# Prevent NoneType on block
		if not block:
			print(f"Can't read: {self._path}")
			return

		# Create Module
		module: Module = Module(module_name)

		raw_block: AnyStr = block[0]  # Take first item

		# Find all methods :
		methods: List = re.findall(r"{\s*[\"\'](\S*)[\"\'][\s\t]*,[\s\t]*(\S*)[\s\t]*,.*},", raw_block)

		for py_name, cpp_name in methods:
			if cpp_name in self._methods:
				module.add_method(
					Method(py_name, cpp_name, self._methods[cpp_name])
				)

		# If object isn't returned, module can't have constant -> End of reading()
		if not object_name:
			return

		# Find all constants :
		# For each function used to register constants:
		for cpp_function, py_type in CONSTANTS_FUNCTION.items():
			# Try to find constants
			constants: List = re.findall(
				"{}\(\s*{}s*,\s*\"(.*)\"".format(cpp_function, object_name),
				self._content
			)
			# If constants found
			if constants:
				# For each constant
				for constant in constants:
					# Build Constant object and att it to Module
					module.add_constant(
						Constant(constant, py_type)
					)
		# Add module to list
		self._modules.append(module)

	def read(self: sf) -> None:
		"""Read files and search for modules"""
		# If file doesn't exist
		if not os.path.exists(self._path):
			raise FileNotFoundError("No such file {}".format(self._path))  # Exit

		# Get content
		content: AnyStr = open(self._path, 'r+', encoding="utf-8", errors="ignore").read()

		# Remove all comment :
		self._content = re.sub(r"(//[^\n]*|/\*(?:(?!\*/).)*\*/)", "", content, 0, re.DOTALL)

		# Search for module :
		modules: List[Match[AnyStr]] = re.findall(
			# Function name + ( "object_name", "module", dict_name) -> support \n...
			"(?:\s+(\S*)\s*=\s+)?" + INIT_MODULE_FUNCTION + "\(\s*\"(.*)\"\s*,\s*(.*)\s*\)",
			self._content
		)

		# if file hasn't module, end processing
		if not modules:
			return

		# Specify that we have found a module (useful for write method)
		self._has_module = True

		# Search all methods
		self.scan_for_all_methods()

		# For each module:
		for match in modules:
			self.scan_for_module(
				match[0],
				match[1],
				match[2]
			)  # Scan to load modules in self.modules

	def write(self: sf, output_directory: AnyStr) -> None:
		"""Write the python representation of the module"""
		# If file hasn't module: there is nothing to do:
		if not self._has_module:
			return

		# For each module
		for module in self._modules:
			with open(output_directory+"/"+module.get_name().lower()+".py", "w+", encoding="utf-8") as file:
				# Header
				file.write(get_header())
				file.write("\n\n")
				file.write(module.render())

	def __str__(self: sf) -> AnyStr:
		"""Representation in string of the class: name"""
		return self._name

	def __repr__(self: sf) -> AnyStr:
		"""Representation in string of the class: name"""
		return self._name
