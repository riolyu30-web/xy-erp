import os
from neo4j import GraphDatabase

# ================= 配置区 =================
# Neo4j 配置 (请根据你的实际情况修改)
NEO4J_URI = "neo4j://127.0.0.1:7687"
NEO4J_USER = "neo4j"
# 默认密码通常是 neo4j，如果修改过请替换
NEO4J_PASSWORD = "12345678"  

def verify_connection():
    print(f"正在尝试连接 Neo4j ({NEO4J_URI})...")
    driver = None
    try:
        driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
        # 验证连接是否可用
        driver.verify_connectivity()
        print("✅ 连接成功！Neo4j 服务运行正常且可访问。")
        
        # 简单查询测试
        with driver.session() as session:
            result = session.run("RETURN 'Hello Neo4j' AS message")
            msg = result.single()["message"]
            print(f"✅ 查询测试通过，数据库返回: {msg}")
            
    except Exception as e:
        print("❌ 连接失败！请检查以下几点：")
        print("1. Neo4j Desktop 是否已启动并点击了 'Start'？")
        print("2. 密码是否正确？(代码中当前密码为 'your_password')")
        print("3. 端口 7687 是否被占用或修改？")
        print(f"详细错误信息: {e}")
    finally:
        if driver:
            driver.close()

if __name__ == "__main__":
    # 提示用户检查密码
    print("注意：运行前请确保代码中的 NEO4J_PASSWORD 已修改为你设置的真实密码。")
    verify_connection()
