import os
import subprocess
import ctypes
from ctypes import c_char_p, CDLL


# Load the shared library
__lib: CDLL  # Adjust for your OS


def _initiliaze_dll(dll_path: str):
    lib = ctypes.CDLL(dll_path)
    lib.create_report.restype = c_char_p
    lib.create_report.argtypes = [c_char_p]

    lib.directory_summary.restype = c_char_p
    lib.directory_summary.argtypes = [c_char_p, c_char_p]

    lib.summary.restype = c_char_p
    lib.summary.argtypes = [c_char_p]
    global __lib
    __lib=lib


class Executor:
    __isDll: bool
    __path: str

    def __init__(self, type: str, path: str):
        path = os.path.abspath(path)
        if not os.path.exists(path):
            raise FileNotFoundError("dll or exe file not found", path)

        if type.lower() == "dll":
            self.__isDll = True
            _initiliaze_dll(path)
        else:
            self.__isDll = False

        self.__path = path
        self.__cwd = os.getcwd()

    def summary(self, report_path: str):
        if self.__isDll:
            return _summary_dll(report_path=report_path)
        else:
            return _summary_exe(
                path_to_exe=self.__path, cwd=self.__cwd, report_path=report_path
            )

    def create(self, dir_path: str):
        if self.__isDll:
            return _create_dll(dir_path=dir_path)
        else:
            return _create_exe(
                path_to_exe=self.__path, cwd=self.__cwd, directory_path=dir_path
            )

    def calculate(self, dir_path: str, report_path: str):
        if self.__isDll:
            return _directory_summary_dll(dir_path=dir_path, report_path=report_path)
        else:
            return _directory_summary_exe(
                path_to_exe=self.__path,
                cwd=self.__cwd,
                directory_path=dir_path,
                report_path=report_path,
            )

    def read(self, report_path: str):
        return _read(report_path)


def _summary_exe(path_to_exe, cwd: str, report_path) -> str:
    result = subprocess.run(
        [path_to_exe, "-m", "summary", "-r", report_path],
        capture_output=True,
        text=True,
        cwd=cwd,
    )
    return result.stdout


def _summary_dll(report_path: str) -> str:
    path = get_dll_string_input(report_path)
    result: str = __lib.summary(path)
    return result


def _create_exe(path_to_exe, cwd: str, directory_path) -> str:
    result = subprocess.run(
        [path_to_exe, "-m", "create", "-d", directory_path],
        capture_output=True,
        text=True,
        cwd=cwd,
    )
    return result.stdout


def _create_dll(dir_path: str) -> str:
    path = get_dll_string_input(dir_path)
    result: str = __lib.create_report(path)
    return result


def _directory_summary_exe(
    path_to_exe, cwd: str, directory_path: str, report_path: str
) -> str:
    result = subprocess.run(
        [path_to_exe, "-m", "calculate", "-r", report_path, "-d", directory_path],
        capture_output=True,
        text=True,
        cwd="D:\\Python\\summary-mcp\\reports",
    )
    return result.stdout


def _directory_summary_dll(dir_path: str, report_path: str) -> str:
    r_path = get_dll_string_input(report_path)
    d_path = get_dll_string_input(dir_path)
    result: str = __lib.directory_summary(r_path, d_path)
    return result


def _read(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as file:
        file_contents = file.read()
        return file_contents


def get_dll_string_input(value: str) -> bytes:
    return value.encode("utf-8")
