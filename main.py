import subprocess
from fastmcp import FastMCP
import os
from executor import Executor
app = FastMCP()

path_to_exe="bin\\dir-summary.exe"
path_to_dll="bin\\dirSummary.dll"

executor=Executor(type="exe",path=path_to_exe)
#executor=Executor(type="dll",path=path_to_dll)

if not (os.path.exists(path_to_exe)):
    raise FileNotFoundError("path to rust binary is incorrect")

@app.tool("create")
def create_file_report(directory_path:str):
    """
    this tool creates a report that will contain all the files and their sizes for the directory/folder passed as an input
    and returns the report path. This report must not be created for every call as this is an expensive operation.
    The output report can be used to generate future summaries and calculation. But make sure that the report is not tool old.
    
    :param directory_path: Path to the directory for which the analysis needs to be done and a report needs to be created
    :type directory_path: str
    :returns: path to the report that contains list of all files, their sizes and their extensions that can be used in future for calculation of sizes and summarization.
    """
    # result = subprocess.run([path_to_exe, "-m", "create","-d", directory_path], capture_output=True, text=True,
    #                         cwd="D:\\Python\\summary-mcp\\reports")
    # return result.stdout
    dir_path=normalize_path(directory_path)
    return executor.create(dir_path)

@app.tool("dir-stat")
def calculate_directory_stats(report_path:str,directory_path:str):
    """
    this tool will calculate the stats for a directory that is present in the report that was generated using the create_file_report 
    function path to report and the path to the directory that needs to be summarized must be provided as input to proceed.
    The output will contain the total number of files and total size of the directory.
    
    :param report_path: Path to the report that will be used to calculate the stats
    :type report_path: str
    :param directory_path: path to the directory for which the stats needs to be calculated
    :type directory_path: str
    :returns: total number of files and total size of the directory
    """
    report_path=normalize_path(report_path)
    directory_path=normalize_path(directory_path)
    # result = subprocess.run([path_to_exe, "-m","calculate","-r", report_path,"-d", directory_path], capture_output=True, text=True,
    #                         cwd="D:\\Python\\summary-mcp\\reports")
    # return result.stdout
    return executor.calculate(directory_path,report_path)

@app.tool("all-dir-stat")
def generate_stats_for_all_directories(report_path:str):
    """
    this tool will create the summary of the report provided as the input. This will create a summary csv file that will contain all the 
    directories present in the csv and their stats. This tool will return the path to the csv that contains the summary.
    
    :param report_path: path to the report that needs to be summarized
    :type report_path: str
    
    :returns: the path to the csv that contains the summary
    """
    report_path=normalize_path(report_path)
    # result = subprocess.run([path_to_exe, "-m","summary","-r", report_path], capture_output=True, text=True
    #                         ,cwd="D:\\Python\\summary-mcp\\reports")
    # return result.stdout
    return executor.summary(report_path)

@app.tool("read")
def read_report(report_path:str):
    """
    this tool will return the content of the report provided as the input
    
    :param report_path: path to the report that needs to be summarized
    :type report_path: str
    
    :returns: the content of the report provided as input
    """
    report_path=normalize_path(report_path)
    # result = subprocess.run([path_to_exe, "-m","print","-r", report_path], capture_output=True, text=True
    #                         ,cwd="D:\\Python\\summary-mcp\\reports")
    # return result.stdout
    return executor.read(report_path)


def normalize_path(path:str):
    path=path.replace("\\\\","\\")
    path=path.replace("\"","")
    return path.strip()



if __name__ == "__main__":
    app.run(transport="http", host="127.0.0.1", port=8000, path="/mcp")