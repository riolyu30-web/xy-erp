from fastmcp import FastMCP
from services.auth_service import auth_mcp


mcp = FastMCP("xy_erp_mcp")
mcp.mount(auth_mcp, prefix="auth")


def main():
    mcp.run(transport='sse', port=9050, host='0.0.0.0')  # 修复变量名错误


if __name__ == "__main__":
    main()
