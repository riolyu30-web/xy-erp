from fastmcp import FastMCP
from services.auth_service import auth_mcp
from services.order_service import order_mcp
from services.calcu_service import calcu_mcp
from services.csv_service import csv_mcp

mcp = FastMCP("xy-erp-mcp")
mcp.mount(auth_mcp, prefix="auth")
mcp.mount(order_mcp, prefix="order")
mcp.mount(calcu_mcp, prefix="calcu")
mcp.mount(csv_mcp, prefix="csv")


def main():
    mcp.run(transport='sse', port=9050, host='0.0.0.0')  # 修复变量名错误


if __name__ == "__main__":
    main()
