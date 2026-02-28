import psycopg2
import os

# ================= 配置区 =================
# Supabase (Postgres) 连接配置
# 请替换为您的真实连接字符串
# 格式: postgresql://postgres:[PASSWORD]@[HOST]:[PORT]/postgres
PG_CONN_STR = "postgresql://192.168.0.33:5432/xy_erp_fwz_ai_test?user=root&password=123456"

def verify_postgres_connection():
    print(f"正在尝试连接 Postgres ({PG_CONN_STR})...")
    conn = None
    try:
        conn = psycopg2.connect(PG_CONN_STR)
        print("✅ 连接成功！Postgres (Supabase) 服务运行正常且可访问。")
        
        # 简单查询测试
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        print(f"✅ 查询测试通过，数据库返回: {result[0]}")
        
        cursor.close()
            
    except Exception as e:
        print("❌ 连接失败！请检查以下几点：")
        print("1. 连接字符串是否正确？(PG_CONN_STR)")
        print("2. 密码是否正确？")
        print("3. 网络是否能访问 Supabase？")
        print(f"详细错误信息: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    print("注意：运行前请确保代码中的 PG_CONN_STR 已修改为您真实的 Supabase 连接字符串。")
    verify_postgres_connection()
