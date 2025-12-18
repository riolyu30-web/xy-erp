from fastmcp import FastMCP # 导入FastMCP

from services.admin_service import admin_mcp
from services.auth_service import auth_mcp
from services.calcu_service import calcu_mcp
from services.chart_service import chart_mcp
from services.csv_service import csv_mcp
from services.finance_service import finance_mcp
from services.order_service import order_mcp
from services.task_service import task_mcp

mcp = FastMCP("xy-erp-mcp") # 实例化FastMCP

mcp.mount(admin_mcp, prefix="admin")
mcp.mount(auth_mcp, prefix="auth")
mcp.mount(calcu_mcp, prefix="calcu")
mcp.mount(chart_mcp, prefix="chart")
mcp.mount(csv_mcp, prefix="csv")
mcp.mount(finance_mcp, prefix="finance")
mcp.mount(order_mcp, prefix="order")
mcp.mount(task_mcp, prefix="task")

def main(): # 定义主函数
    mcp.run(transport='sse', port=9050, host='0.0.0.0') # 运行MCP服务

if __name__ == "__main__": # 判断是否为主程序入口
    main() # 调用主函数