from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import json
import os
import sys
from fastapi import Depends
from api.v1.dependencies import get_current_user

# 添加项目根目录到 sys.path，以便导入 codegen_tool
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

import codegen_tool

router = APIRouter()

# 指向 erp-service/mcp.json (当前项目根目录下的 mcp.json)
MCP_JSON_PATH = os.path.join(BASE_DIR, "mcp.json")

class McpData(BaseModel):
    mcp: list

@router.get("/")
async def get_mcp():
    try:
        if os.path.exists(MCP_JSON_PATH):
            with open(MCP_JSON_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            return {"mcp": []}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/save")
async def save_mcp(data: McpData, current_user: dict = Depends(get_current_user)):
    try:
        # 确保目录存在
        os.makedirs(os.path.dirname(MCP_JSON_PATH), exist_ok=True)
        
        with open(MCP_JSON_PATH, 'w', encoding='utf-8') as f:
            json.dump(data.model_dump(), f, ensure_ascii=False, indent=4)
        return {"message": "Saved successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/restart")
async def restart_service(current_user: dict = Depends(get_current_user)):
    try:
        # 调用代码生成工具
        codegen_tool.generate_service_script(MCP_JSON_PATH)
        codegen_tool.rebulid_main_mcp()
        # 导入subprocess模块以便执行系统命令
        import subprocess
        import platform
        
        # 检查操作系统类型
        if platform.system() == "Linux":
            # 定义重启服务的命令列表
            # 确认 systemctl 在哪里 which systemctl
            # 通常会输出 /usr/bin/systemctl
            cmd = ["systemctl", "restart", "xy-mcp"]
            # 执行命令并检查是否成功
            # 如果是用 Systemd ( .service 文件) 启动： 找到你的服务配置文件（通常在 /etc/systemd/system/你的服务名.service ），在 [Service] 部分添加或修改 Environment        
            subprocess.run(cmd, check=True)
        else:
            # 非Linux环境（如Windows开发环境）跳过执行
            print(f"Skipping service restart on {platform.system()}")
            
        return {"message": "Service script generated and main mcp rebuilt successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
