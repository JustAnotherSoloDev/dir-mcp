import ctypes

lib_path = "D:\\Python\\\dir-summary\\target\\debug\\dirSummary.dll"

lib = ctypes.CDLL(lib_path)

lib.create_report.argtypes = [ctypes.c_char_p]
lib.create_report.restype = ctypes.c_char_p

lib.summary.argtypes = [ctypes.c_char_p]
lib.summary.restype = ctypes.c_char_p

lib.directory_summary.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
lib.directory_summary.restype = ctypes.c_char_p


if __name__ == "main":
    report_name=lib.create_report(b"C:\\Users\\deven\\AppData\\Roaming\\Python")
    print(report_name)
