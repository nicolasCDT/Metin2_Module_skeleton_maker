#!/usr/bin/python
# -*- coding: <utf-8> -*-

import os
import glob
from typing import *
import re

OUTPUT_DIRECTORY: str = 'bin'
INPUT_DIRECTORY: str = 'src'

TYPE_CORRESPONDENCES = {
	"byte": "int",
	"int": "int",
	"string": "str"
}


def get_python_type(arg_type: str) -> str:
	if arg_type in TYPE_CORRESPONDENCES:
		return TYPE_CORRESPONDENCES[arg_type]
	raise Exception("Unknown C++ type: {}".format(arg_type))


class Argument:

	def __init__(self, name: str, arg_type: str) -> NoReturn:
		self.name: str = name
		self.arg_type: str = arg_type

	def set_name(self, name: str) -> NoReturn:
		self.name = name

	def set_arg_type(self, arg_type: str) -> NoReturn:
		self.arg_type = arg_type

	def get_name(self) -> str:
		return self.name

	def get_arg_type(self) -> str:
		return self.arg_type

	def render(self) -> Union[str, None]:
		if self.name != str() and self.arg_type != str():
			return f'{self.name}: {(get_python_type(self.arg_type))}'

	def __str__(self) -> str:
		return self.name


class Function:
	def __init__(self) -> NoReturn:
		self.name: str = str()
		self.arguments: List[Argument] = list()
		self.returned_value: Union[None, Argument] = None
		self.content: str = str()
		self.f_return: List[Argument] = list()

	def set_name(self, name: str) -> NoReturn:
		self.name = name

	def add_argument(self, argument: Argument) -> NoReturn:
		self.arguments.append(argument)

	def get_name(self) -> str:
		return self.name

	def set_content(self, content: str) -> NoReturn:
		self.content = content

	def get_content(self) -> str:
		return self.content

	def set_returned_value(self, value: Argument) -> NoReturn:
		self.returned_value = value

	def get_returned_value(self) -> Argument:
		return self.returned_value

	def get_argument(self, index: int = -1) -> Union[List[Argument], Argument]:
		if 0 <= index < len(self.arguments):
			return self.arguments[index]
		return self.arguments

	def render(self) -> Union[str, None]:
		if self.name != str() and self.arguments != list():
			return ""  # make render and return it
		return None

	def __str__(self) -> str:
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
		print("".join(self.lines))

	def process(self) -> NoReturn:
		self.read_lines()
		self.read_module_name()
		self.read_module_content()

	def has_module(self) -> bool:
		return self.module_name != str()

	def __str__(self) -> str:
		return self.path


class SrcFiles:

	def __init__(self, path: str) -> NoReturn:
		self.files: List[SrcFile] = list()
		self.path: str = path

	def add_file(self, file: str) -> NoReturn:
		current_file: SrcFile = SrcFile(file)
		self.files.append(current_file)

	def remove_file(self, file: SrcFile) -> NoReturn:
		self.files.remove(file)

	def process(self) -> NoReturn:
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
		return f"[{', '.join(str(x) for x in self.files)}]"


def process() -> NoReturn:
	print("Getting all files in src directory")

	files = SrcFiles('src')
	files.process()


if __name__ == '__main__':
	print("Welcome !")
	print("I was coded by Takuma! A Frenchman who loves baguettes!")
	print("This tools only support one module per files...")
	print("And module initialisation have to be on only one line.")
	process()
