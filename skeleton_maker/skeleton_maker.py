#!/usr/bin/python

#  Copyright (c) 2022, Takuma.
#  Respect intellectual property, and do not delete these comments.

# -*- coding: <utf-8> -*-

from pathlib import Path
import os
from skeleton_maker.source_file import SourceFile
from typing import *


# Typing for self -> SkeletonMaker
sk = TypeVar("sk", bound="SkeletonMaker")


class SkeletonMaker:
	"""Skeleton Maker
	This is the main project's class, the main file of skeleton_maker.
	"""
	def __init__(self: sk, input_directory: AnyStr, output_directory: AnyStr) -> None:
		"""Initialization of SkeletonMaker class"""
		self._input_directory: AnyStr = input_directory
		self._output_directory: AnyStr = output_directory
		self._files: List[SourceFile] = list()

	def scan_for_files(self: sk) -> None:
		"""Scan all files and add them tout files attribut"""
		# For each .cpp in input directory
		for path in Path(self._input_directory).rglob("*.cpp"):
			# Add a new SourceFile for this file
			self._files.append(SourceFile(str(path)))

	def read_all_files(self: sk) -> None:
		"""Read all files and call read() and write() on each them"""
		# For each file
		for file in self._files:
			# print(f"Processing on {file}...")
			# Read file
			file.read()

			# Check for render directory
			if not os.path.exists(self._output_directory):
				try:
					os.makedirs(self._output_directory)
				except Exception:
					raise Exception("Can't create output directory")

			# Write skeleton in output directory
			file.write(self._output_directory)

	def process(self: sk) -> None:
		"""Main process"""
		# Get all files
		self.scan_for_files()

		# Read all files
		self.read_all_files()

		# Just for display:
		print("Maker has process on {} files !".format(len(self._files)))
