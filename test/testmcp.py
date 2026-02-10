import asyncio
from fastmcp import Client

import asyncio
from fastmcp import Client

client = Client("http://localhost:8000/mcp")


async def call_tool(name: str):
    async with client:
        dir_path = "D:\\github\\dir-mcp"
        result = await client.call_tool("create", {"directory_path": dir_path})
        report_name=get_file_name(result)
        print(report_name)
        result = await client.call_tool(
            "dir-stat", {"report_path": report_name, "directory_path": dir_path}
        )
        print(result)
        result = await client.call_tool("all-dir-stat", {"report_path": report_name})
        summary=get_file_name(result)
        print("Directory Summary:",summary)
        
        result = await client.call_tool("read", {"report_path": report_name})
        print(result)


def get_file_name(result):
    report_name = result.content[0].text
    report_name = report_name.replace("\\\\", "\\")
    report_name = report_name.replace("ReportFile=", "")
    report_name = report_name.replace("reportPath=", "")
    return report_name.replace('"', "")
    


asyncio.run(call_tool(""))
