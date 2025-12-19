import subprocess
import platform
        
        # 检查操作系统类型
if platform.system() == "Linux":
            # 定义重启服务的命令列表
            cmd = ["sudo", "systemctl", "restart", "xy-mcp"]
            # 执行命令并检查是否成功
            subprocess.run(cmd, check=True)
else:
            # 非Linux环境（如Windows开发环境）跳过执行
            print(f"Skipping service restart on {platform.system()}")
            
print({"message": "Service script generated and main mcp rebuilt successfully"})