#!/usr/bin/python

#  Copyright (c) 2022, Takuma.
#  Respect intellectual property, and do not delete these comments.

# -*- coding: <utf-8> -*-

from typing import Dict, Type, List, AnyStr

# Configuration part
# Here, you can configure a little the skeleton_maker.

# Function to get data from arguments. Example: GetString() try to catch a str argument.
FUNCTIONS_TYPE_CORRESPONDENCES: Dict[str, Type] = {
	"GetLong": int,
	"GetDouble": int,
	"GetFloat": float,
	"GetByte": int,
	"GetInteger": int,
	"GetUnsignedLong": int,
	"GetTextInstance": int,
	"GetUnsignedInteger": int,
	"GetString": str,
	"GetWindow": int,
	"GetBoolean": bool,
	"GetThingInstance": int,
	"GetImageInstance": int,
	"GetExpandedImageInstance": int,
	"GetObject": object
}

# Letter type correspondences. Used by C++ to build value who will be returns to Python.
# {C++ letter :  Python type}
LETTER_TYPE_CORRESPONDENCES: Dict[str, Type] = {
	'i': int,
	's': str,
	'c': int,
	'l': int,
	'f': float,
	'b': bool,
	'O': object,
	'L': int,
}

# Functions used to define new constants. {C++ Function:  Python type}
CONSTANTS_FUNCTION: Dict[str, Type] = {
	"PyModule_AddIntConstant": int,
	"PyModule_AddStringConstant": str
	# Add new type in Constant's render method
}

# Keyword reserved by Python. You can't use them. So, maker need to rename them.
RESERVED_KEYWORD: List[str] = [
	"False", "def", "if", "raise", "None", "del", "import", "return", "True", "elif", "in", "try", "and", "else", "is",
	"while", "as", "except", "lambda", "with", "assert", "finally", "nonlocal", "yield", "break", "for", "not", "class",
	"from", "or", "continue", "global", "pass"
]

# Function used to initialize a new Python module
INIT_MODULE_FUNCTION: AnyStr = "Py_InitModule"

# Type of the dict with all methods
MODULE_DICT_TYPE: AnyStr = "PyMethodDef"

# Format ags name to snakeCase
FORMAT_ARGUMENTS_TO_SNAKE_CASE: bool = True
