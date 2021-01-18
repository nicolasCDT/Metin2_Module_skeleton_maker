#!/usr/bin/python

#  Copyright (c) 2021, Takuma.
#  Respect intellectual property, and do not delete these comments.
#  Thanks to Gurgarath for his help !

# Perl regex: {((?>[^{}]++|(?R))*)}

# -*- coding: <utf-8> -*-

import os
import glob
from typing import *
import re

__author__ = "Takuma"
__version__ = "1.0"
__email__ = "dev.takuma@gmail.com"
__status__ = "development"

OUTPUT_DIRECTORY: str = 'bin'
INPUT_DIRECTORY: str = 'src'

TYPE_CORRESPONDENCES = {
	"byte": "int",
	"int": "int",
	"string": "str"
}


def get_python_type(arg_type: str) -> str:
	"""
	Return python type for c++ arg_type
	:param arg_type: argument's type in C++
	:return: Python's equivalent for arg_type
	"""
	if arg_type in TYPE_CORRESPONDENCES:
		return TYPE_CORRESPONDENCES[arg_type]
	raise Exception("Unknown C++ type: {}".format(arg_type))


class Argument:
	"""
	Model an argument, and allows to determine its equivalent in Python.
	"""

	def __init__(self, name: str, arg_type: str) -> NoReturn:
		"""
		Argument class constructor.
		:param name: Argument's name
		:param arg_type: Argument's type
		"""
		self.name: str = name
		self.arg_type: str = arg_type

	def set_name(self, name: str) -> NoReturn:
		"""
		Set Argument's name
		:param name: Argument's name
		"""
		self.name = name

	def set_arg_type(self, arg_type: str) -> NoReturn:
		"""
		Set Argument's type
		:param arg_type: Argument's type
		"""
		self.arg_type = arg_type

	def get_name(self) -> str:
		"""
		Get Argument's name
		:return: str: Argument's name
		"""
		return self.name

	def get_arg_type(self) -> str:
		"""
		Get Argument's type (C++)
		:return: str: Argument's type
		"""
		return self.arg_type

	def render(self) -> Union[str, None]:
		"""
		Get Python's equivalent of current argument
		:return: str: "name: type"
		"""
		if self.name != str() and self.arg_type != str():
			return f'{self.name}: {(get_python_type(self.arg_type))}'

	def __str__(self) -> str:
		"""
		Get Argument's name
		:return: str: Argument's name
		"""
		return self.name


class Function:
	"""
	Modeling and processing of a function
	"""

	def __init__(self) -> NoReturn:
		"""
		Initialization for Function class
		"""
		self.name: str = str()
		self.arguments: List[Argument] = list()
		self.returned_value: Union[None, Argument] = None
		self.content: str = str()
		self.f_return: List[Argument] = list()

	def set_name(self, name: str) -> NoReturn:
		"""
		Set function's name
		:param name: str: Function's name
		"""
		self.name = name

	def add_argument(self, argument: Argument) -> NoReturn:
		"""
		Add one function's argument
		:param argument: Argument: arg
		"""
		self.arguments.append(argument)

	def get_name(self) -> str:
		"""
		Get function's name
		:return: str: function's name
		"""
		return self.name

	def set_content(self, content: str) -> NoReturn:
		"""
		Set function's content
		:param content: str: function's content
		"""
		self.content = content

	def get_content(self) -> str:
		"""
		Get function's content
		:return: str: function's content
		"""
		return self.content

	def set_returned_value(self, value: Argument) -> NoReturn:
		"""
		Set function's returned values
		:param value: Argument: value
		"""
		self.returned_value = value

	def get_returned_value(self) -> Argument:
		"""
		Get function's returned value
		:return: Argument: returned value
		"""
		return self.returned_value

	def get_argument(self, index: int = -1) -> Union[List[Argument], Argument]:
		"""
		Get argument(s)
		:param index: index of element
		:return: Union[List[Argument], Argument]: argumen(s)
		"""
		if 0 <= index < len(self.arguments):
			return self.arguments[index]
		return self.arguments

	def render(self) -> Union[str, None]:
		"""
		Render a function
		:return: Union[str, None]: function's render
		"""
		if self.name != str() and self.arguments != list():
			return ""  # make render and return it
		return None

	def __str__(self) -> str:
		"""
		String for represent a functions
		:return: str: representation
		"""
		return "{}({})".format(
			self.name,
			", ".join(str(arg) for arg in self.arguments)
		)


class SrcFile:
	def __init__(self, path: str) -> NoReturn:
		self.path: str = path
		self.lines: List[str] = list()
		self.module_name: str = str()
		self.methods_dic_name: str = str()
		self.constants: str = str()
		self.methods: Dict[str, str] = dict()  # s_methods\[\]((.|\n)*){((.|_n)*)} --> {.*\"(.*)\",(.*),.*} --> strip
		self.methods_list_contents: List[Dict[str, str]] = list()  # PyObject\s*\*\s*(.*)\(.*\)(.|\n*){(.|\n)*?}

	def read_lines(self) -> NoReturn:
		with open(self.path, "r+", encoding="utf-8", errors="ignore") as file:
			self.lines = file.readlines()

	def read_module_name(self) -> NoReturn:
		for line in self.lines:
			if "Py_InitModule(" in line:
				groups = re.search("Py_InitModule\(\\\"(.*?)\\\",\s*(.*)\)", line)
				if groups:
					groups = groups.groups()
				self.module_name = groups[0]
				self.methods_dic_name = groups[1]

	def read_module_content(self) -> NoReturn:
		# --> Remove comments
		content: str = "".join(self.lines)
		methods: Match = re.search(self.methods_dic_name + '\[]((.|\n)*){((.|_n)*)}', content)

		if not methods:
			return

		methods_group: str = methods.groups()[0]
		methods_list: list = re.findall('{.*\"(.*)\",\t*(.*),.*}', methods_group)
		if methods_list:
			for m in methods_list:
				if len(m) == 2:
					self.methods[m[0]] = m[1]
		content = "".join(self.lines)
		with open("test.txt", "w", encoding="utf-8") as file:
			file.write(content)
		f_content = re.findall("PyObject\s*\*\s*(.*)\(.*\)\s*{((?:[^{}]+|{([^{}]+)}){3})}", content)
		print(f_content)

	#  Continue

	def process(self) -> NoReturn:
		self.read_lines()
		self.read_module_name()
		self.read_module_content()

	def has_module(self) -> bool:
		return self.module_name != str()

	def __str__(self) -> str:
		return self.path


class SrcFiles:
	"""
	Class for processing on multiple SrcFile
	"""

	def __init__(self, path: str) -> NoReturn:
		"""
		Initialization of class
		:param path: strm path of files
		"""
		self.files: List[SrcFile] = list()
		self.path: str = path

	def add_file(self, file: str) -> NoReturn:
		"""
		Add SrcFile's path
		:param file: str: path
		"""
		current_file: SrcFile = SrcFile(file)
		self.files.append(current_file)

	def remove_file(self, file: SrcFile) -> NoReturn:
		"""
		Remove path from list
		:param file: src: file's path to delete
		"""
		self.files.remove(file)

	def process(self) -> NoReturn:
		"""
		Processing on each SrcFile
		"""
		input_files = glob.glob(f"{self.path}/*", recursive=True)
		for file in input_files:
			if os.path.exists(file):
				self.add_file(file)

		for file in self.files:
			file.process()

		for file in self.files:
			if not file.has_module():
				self.remove_file(file)

	def __str__(self) -> str:
		"""
		Making string to represent class
		:return: str: representation
		"""
		return f"[{', '.join(str(x) for x in self.files)}]"


def process() -> NoReturn:
	"""
	Initialize SrcFiles objet, and start process.
	"""
	print("Getting all files in src directory")

	files = SrcFiles('src')
	files.process()


if __name__ == '__main__':
	print("Welcome !")
	print("I was coded by Takuma! A Frenchman who loves baguettes!")
	print("This tools only support one module per files...")
	print("And module initialisation have to be on only one line.")
	print("As it's by default.")
	process()
