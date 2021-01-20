#!/usr/bin/python

#  Copyright (c) 2021, Takuma.
#  Respect intellectual property, and do not delete these comments.
#  Thanks to Gurgarath for his help !

# -*- coding: <utf-8> -*-

import os
import glob
from typing import *
from typing import IO
import re

__author__ = "Takuma"
__version__ = "1.0"
__email__ = "dev.takuma@gmail.com"
__status__ = "development"

# CONFIGURATION BLOCK
OUTPUT_DIRECTORY: str = 'bin'
INPUT_DIRECTORY: str = 'src'

MAKE_ALL_IN_ONE_FILE: bool = False

# DEVELOPMENT CONSTANTS
FUNCTIONS_TYPE_CORRESPONDENCES: dict = {
	"GetLong": "int",
	"GetDouble": "int",
	"GetFloat": "float",
	"GetByte": "int",
	"GetInteger": "int",
	"GetUnsignedLong": "int",
	"GetUnsignedInteger": "int",
	"GetString": "str",
	"GetBoolean": "bool",
	"GetObject": "object"
}

LETTER_TYPE_CORRESPONDENCES: dict = {
	'i': "int",
	's': "str",
	'c': "int",
	'l': "int",
	'f': "float",
	'b': "bool"
}

RESERVED_KEYWORD: list = [
	"False", "def", "if", "raise", "None", "del", "import", "return", "True", "elif", "in", "try", "and", "else", "is",
	"while", "as", "except", "lambda", "with", "assert", "finally", "nonlocal", "yield", "break", "for", "not", "class",
	"from", "or", "continue", "global", "pass"
]


def get_python_type_by_function(arg_type: str) -> str:
	"""
	Return python type for c++ arg_type with function as reference
	:param arg_type: argument's type in C++
	:return: Python's equivalent for arg_type
	"""
	if arg_type in FUNCTIONS_TYPE_CORRESPONDENCES:
		return FUNCTIONS_TYPE_CORRESPONDENCES[arg_type]
	raise Exception("Unknown C++ type: {}".format(arg_type))


def get_python_type_by_letter(arg_type: str) -> str:
	"""
	Return python type for c++ arg_type with letter as reference
	:param arg_type: argument's type in C++
	:return: Python's equivalent for arg_type
	"""
	if arg_type in LETTER_TYPE_CORRESPONDENCES:
		return LETTER_TYPE_CORRESPONDENCES[arg_type]
	raise Exception("Unknown C++ type: {}".format(arg_type))


def comment_remover(text) -> str:
	"""
	Remove comments from C++ text
	:param text: str: C++ code
	:return: str: code uncomment.
	"""

	def replacer(match):
		s: str = match.group(0)
		if s.startswith('/'):
			return " "
		else:
			return s

	pattern = re.compile(
		r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"',
		re.DOTALL | re.MULTILINE
	)
	return re.sub(pattern, replacer, text)


def write_head_block(file: IO, ) -> NoReturn:
	"""
	Write in file the common file's header
	:param file: file
	"""
	file.write("""from typing import *


__author__ = "Takuma"
__version__ = "1.0"
__email__ = "dev.takuma@gmail.com"
__status__ = "development"


#  Copyright (c) 2021, Takuma.
#  Respect intellectual property, and do not delete these comments.
#  Thanks to Gurgarath for his help !
""")


def check_render_space() -> NoReturn:
	"""
	Check if render file can be created by check if output directory is/can be created
	"""
	if not os.path.exists(OUTPUT_DIRECTORY):
		try:
			os.makedirs("bin")
		except Exception:
			raise Exception("Can't create output directory")


class Argument:
	"""
	Model an argument, and allows to determine its equivalent in Python.
	"""

	def __init__(self, name: str, arg_type: Union[str, None]) -> NoReturn:
		"""
		Argument class constructor.
		:param name: Argument's name
		:param arg_type: Argument's type
		"""
		self.name: str = name
		self.arg_type: Union[str, None] = arg_type
		self.check_name()

	def check_name(self):
		if self.name in RESERVED_KEYWORD:
			self.name = '_' + self.name
		self.name = self.name.replace(".", "")

	def render(self) -> Union[str, None]:
		"""
		Get Python's equivalent of current argument
		:return: str: "name: type"
		"""
		if self.name and self.arg_type:
			return f"{self.name}: {(get_python_type_by_function(self.arg_type))}"
		elif self.name:
			return f"{self.name}"

	def __str__(self) -> str:
		"""
		Get Argument's name
		:return: str: Argument's name
		"""
		return self.name


class Method:
	"""
	Modeling and processing of a function
	"""

	def __init__(self) -> NoReturn:
		"""
		Initialization for Function class
		"""
		self.name: str = str()
		self.arguments: List[Argument] = list()
		self.returned_value: Union[None, str] = None
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

	def set_returned_value(self, value: str) -> NoReturn:
		"""
		Set function's returned values
		:param value: str: value
		"""
		self.returned_value = value

	def get_argument(self, index: int = -1) -> Union[List[Argument], Argument]:
		"""
		Get argument(s)
		:param index: index of element
		:return: Union[List[Argument], Argument]: argument(s)
		"""
		if 0 <= index < len(self.arguments):
			return self.arguments[index]
		return self.arguments

	def process(self) -> NoReturn:
		"""
		Read content and parse arguments + return
		"""
		args_matches = re.findall("PyTuple_(.*)\(.*,\s*(.*)\s*,\s*&(.*)\)\)", self.content)
		args_matches = sorted(args_matches, key=lambda tup: tup[1])
		used_id: List[int] = list()
		unknown_format: bool = False
		for match in args_matches:
			if match[2] not in used_id:
				used_id.append(match[2])
			else:
				unknown_format = True
		if unknown_format:
			arg_count: int = int(max(args_matches, key=lambda index: index[1])[1])
			for i in range(0, arg_count + 1):
				argument: Argument = Argument(f"unknown_{i}", None)
				self.add_argument(argument)
			return

		for match in args_matches:
			arg: Argument = Argument(match[2], match[0])
			self.add_argument(arg)

		return_match: List = re.findall("return\s*Py_BuildValue\(\"(.*)\"", self.content)
		if return_match:
			if len(return_match) == 1:
				return_format: str = return_match[0].replace('#', '').replace('*', '')  # Remove unknown char Python
				if len(return_format) == 1:
					self.set_returned_value(get_python_type_by_letter(return_format.lower()))
				else:
					output_str: str = "Tuple["
					for letter in return_format:
						output_str += get_python_type_by_letter(letter.lower())
						output_str += ", "
					output_str = output_str[:-2] + "]"
					self.set_returned_value(output_str)

	def render(self) -> str:
		"""
		Render a function
		:return: str: function's render
		"""
		if self.name != str():
			render: str = f"\tdef {self.name}(self, "  # def xxx(self,_

			# Arguments
			if self.arguments:
				for arg in self.arguments:
					render += arg.render() + ", "
			render = render[:-2] + ")"

			# Return
			render += " -> "
			if self.returned_value:
				render += self.returned_value
			else:
				render += "NoReturn"
			render += ":"

			# Body
			render += "\n\t\tpass\n"

			return render
		return ""

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
	"""
	Modeling of one source file
	"""

	def __init__(self, path: str) -> NoReturn:
		"""
		Initialization for SrcFile class
		"""
		self.path: str = path
		self.lines: List[str] = list()
		self.module_name: str = str()
		self.methods_dic_name: str = str()
		self.constants: str = str()  # s_methods
		self.methods: Dict[str, str] = dict()  # s_methods\[\]((.|\n)*){((.|_n)*)} --> {.*\"(.*)\",(.*),.*} --> strip
		self.methods_list_contents: Dict[str, str] = dict()  # PyObject\s*\*\s*(.*)\(.*\)(.|\n*){(.|\n)*?}
		self.methods_object: List[Method] = list()
		self.output: str = str()  # use for do all in one file

	def read_lines(self) -> NoReturn:
		"""
		Read files in utf-8 and save them
		"""
		with open(self.path, "r+", encoding="utf-8", errors="ignore") as file:
			self.lines = file.readlines()

	def read_module_name(self) -> NoReturn:
		"""
		Search line with module and get his name
		"""
		for line in self.lines:
			if "Py_InitModule(" in line:
				groups = re.search("Py_InitModule\(\\\"(.*?)\\\",\s*(.*)\)", line)
				if groups:
					groups = groups.groups()
				self.module_name = groups[0]
				self.methods_dic_name = groups[1]

	def read_module_content(self) -> NoReturn:
		"""
		Read module content to find method and her content
		"""
		content: str = "".join(self.lines)
		content = comment_remover(content)
		methods: Match = re.search(self.methods_dic_name + '\[]((.|\n)*){((.|_n)*)}', content)

		if not methods:
			return

		methods_group: str = methods.groups()[0]
		methods_list: list = re.findall('{.*\"(.*)\",\t*(.*),.*}', methods_group)
		if methods_list:
			for m in methods_list:
				if len(m) == 2:
					self.methods[m[1].strip()] = m[0].strip()
		occurrences: List = re.findall("PyObject\s*\*\s*(.*)\(.*\)\s*{((?:[^{}]+|{([^{}]+)}){3})}", content)
		for occurrence in occurrences:
			self.methods_list_contents[occurrence[0]] = occurrence[1]

		to_delete: list = list()
		for method in self.methods_list_contents:
			if method not in self.methods.keys():
				to_delete.append(method)
		for method in to_delete:
			self.methods_list_contents.pop(method)

	def read_functions(self) -> NoReturn:
		"""
		Read all functions name, create object and work on it
		:return:
		"""
		for method in self.methods_list_contents:
			function = Method()
			function.set_name(self.methods[method])
			function.set_content(self.methods_list_contents[method])
			function.process()
			self.methods_object.append(function)

	def process(self) -> NoReturn:
		"""
		Work on the file
		"""
		self.read_lines()
		self.read_module_name()
		self.read_module_content()
		self.read_functions()

	def render(self) -> NoReturn:
		"""
		Render a module
		"""
		if self.module_name == "" or not self.methods_object:
			return
		check_render_space()
		if not MAKE_ALL_IN_ONE_FILE:
			with open(f"{OUTPUT_DIRECTORY}/{self.module_name}.py", "w", encoding="utf-8") as rendering_file:
				print(f"Rendering {self.module_name}...")
				write_head_block(rendering_file)
				rendering_file.write("\n\n")  # Two \n for conventions
				rendering_file.write(f"class {self.module_name}:")
				for method in self.methods_object:
					rendering_file.write("\n")
					rendering_file.write(method.render())
		else:
			self.output += "\n\n"
			self.output += f"class {self.module_name}:"
			for method in self.methods_object:
				self.output += "\n"
				self.output += method.render()

	def has_module(self) -> bool:
		"""
		If file has module
		:return: bool: has module
		"""
		return self.module_name != str()

	def __str__(self) -> str:
		"""
		Make string who represent SrcFile current object
		:return: str: representation
		"""
		return self.path


class SrcFiles:
	"""
	Class for processing on multiple SrcFile
	"""

	def __init__(self, path: str) -> NoReturn:
		"""
		Initialization of class
		:param path: str: path of files
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

		for file in self.files:
			file.render()

		if MAKE_ALL_IN_ONE_FILE:
			with open("bin/modules.py", "w", encoding="utf-8") as render_file:
				print("Rendering modules.py..")
				write_head_block(render_file)
				for file in self.files:
					render_file.write(file.output)

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
	print("Ended.")
