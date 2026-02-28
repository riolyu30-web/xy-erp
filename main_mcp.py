from fastmcp import FastMCP # 导入FastMCP

from services.admin_service import admin_mcp
from services.auth_service import auth_mcp
from services.business_service import business_mcp
from services.calcu_service import calcu_mcp
from services.chart_service import chart_mcp
from services.csv_service import csv_mcp
from services.finance_service import finance_mcp
from services.neo4j_service import neo4j_mcp
from services.order_service import order_mcp
from services.outgoing_service import outgoing_mcp
from services.pay_service import pay_mcp
from services.purchase_service import purchase_mcp
from services.quality_service import quality_mcp
from services.task_service import task_mcp
from services.work_service import work_mcp

mcp = FastMCP("xy-erp-mcp") # 实例化FastMCP

mcp.mount(admin_mcp, prefix="admin")
mcp.mount(auth_mcp, prefix="auth")
mcp.mount(business_mcp, prefix="business")
mcp.mount(calcu_mcp, prefix="calcu")
mcp.mount(chart_mcp, prefix="chart")
mcp.mount(csv_mcp, prefix="csv")
mcp.mount(finance_mcp, prefix="finance")
mcp.mount(neo4j_mcp, prefix="neo4j")
mcp.mount(order_mcp, prefix="order")
mcp.mount(outgoing_mcp, prefix="outgoing")
mcp.mount(pay_mcp, prefix="pay")
mcp.mount(purchase_mcp, prefix="purchase")
mcp.mount(quality_mcp, prefix="quality")
mcp.mount(task_mcp, prefix="task")
mcp.mount(work_mcp, prefix="work")

def main(): # 定义主函数
    mcp.run(transport='sse', port=9050, host='0.0.0.0') # 运行MCP服务

if __name__ == "__main__": # 判断是否为主程序入口
    main() # 调用主函数