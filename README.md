# Metin2_Module_skeleton_maker

This tool allows you to create a skeleton of your Python modules generated by the C API to use the editors'
autocompletion

**This tool only support one module per files.**

## Installation

You must have Python3 installed.

Modules used:

* glob
* re
* typing
* os

## How to use :

* Put your .cpp files in **src** folder.
* Launch **main.py** with `py main.py`.
* Get output in **bin** folder.

## Next Stape ?
To continue, you can use [VegaS](https://github.com/Vegas007/)'s script to convert your python2 code to python3 : [Script here](https://github.com/Vegas007/Python-Code-Translator-2-to-3). 
This will adapt your code to be usable both in python2 and python 3

## Authors

* Takuma - [Email](mailto:work.takuma@gmail.com) - Discord: Takuma#2725

### Thanks

* [Gurgarath](https://github.com/Gurgarath) for his help with regex.
* [VegaS](https://github.com/Vegas007) for his tools to convert py2 code to py3.
* [Mali61](https://github.com/blackdragonx61) for having complete C++ functions list.
* [Arves100](https://github.com/arves100) to have corrected something forgotten in the code.
* msnas on [metin2dev](https://metin2.dev/profile/16588-msnas/) to have corrected the return type (NoReturn -> None)

## License

[MIT](LICENSE)
