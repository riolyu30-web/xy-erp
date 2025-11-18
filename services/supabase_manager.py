import os
from dotenv import load_dotenv
from supabase import create_client, Client
from typing import List, Dict, Any
# 导入hashlib模块用于生成哈希值
import hashlib
# 导入datetime模块用于处理时间
from datetime import datetime, timedelta
# 导入uuid模块用于生成唯一标识符
import uuid
import random

# 加载环境变量
load_dotenv()


class SupabaseManager:
    """
    Supabase 数据库管理类

    功能模块：
    - 数据库连接管理
    - CRUD 操作（增删改查）
    - 用户认证（注册、登录、登出）
    - 文件存储（上传、获取链接）

    数据表要求：

    1. 普通业务表（如 xunkebao）：
       必须包含以下字段用于软删除功能
       - deleted_at: TIMESTAMP NULL DEFAULT NULL
         * 软删除标记字段
         * NULL 表示数据未删除
         * 包含时间戳表示数据已删除

       示例建表语句：
       CREATE TABLE xunkebao (
           id BIGSERIAL PRIMARY KEY,
           company TEXT,
           phone TEXT,
           legal_person TEXT,
           contact TEXT,
           notes TEXT,
           deleted_at TIMESTAMP NULL DEFAULT NULL,  -- 必须字段
           created_at TIMESTAMP DEFAULT NOW(),
           updated_at TIMESTAMP DEFAULT NOW()
       );

    2. 用户认证表（user_table）：
       必须包含以下字段用于令牌认证
       - token: TEXT NULL
         * 用户登录令牌
         * 用于验证用户身份
       - expire: TIMESTAMP NULL
         * 令牌过期时间
         * 用于验证令牌是否有效

       示例建表语句：
       CREATE TABLE users (
           id BIGSERIAL PRIMARY KEY,
           username TEXT UNIQUE NOT NULL,
           password TEXT NOT NULL,
           email TEXT,
           phone TEXT,
           token TEXT NULL,                         -- 必须字段
           expire TIMESTAMP NULL,                   -- 必须字段
           created_at TIMESTAMP DEFAULT NOW(),
           updated_at TIMESTAMP DEFAULT NOW()
       );

    环境变量配置（.env 文件）：
       SUPABASE_URL=your_supabase_url
       SUPABASE_ANON_KEY=your_anon_key
       SUPABASE_USER_TABLE=users
       TOKEN_SECRET=your_secret_key
       TOKEN_EXPIRE=86400  # 令牌有效期（秒），86400=24小时

    使用示例：
       # 初始化
       manager = SupabaseManager()
       manager.connect()

       # CRUD 操作
       manager.insert_data("xunkebao", [{"company": "测试公司"}])
       data = manager.read_data("xunkebao")
       manager.update_data("xunkebao", ["company"], {"company": "测试公司", "phone": "新号码"})
       manager.delete_data("xunkebao", {"company": "测试公司"})

       # 认证操作
       manager.sign_up({"username": "user", "password": "pass"}, unique=["username"])
       token = manager.sign_in({"username": "user", "password": "pass"})
       is_valid = manager.verify_token(token)
       manager.sign_out(token)

       # 文件操作
       url = manager.upload_file("avatars", "image.jpg")
    """

    def __init__(self):
        self.url = os.getenv("SUPABASE_URL")
        self.key = os.getenv("SUPABASE_ANON_KEY")
        self.user_table = os.getenv("SUPABASE_USER_TABLE")
        self.token_secret = os.getenv("TOKEN_SECRET")
        self.token_expire = int(os.getenv("TOKEN_EXPIRE"))
        self.client: Client = None

    def connect(self):
        """连接到 Supabase"""
        try:
            self.client = create_client(self.url, self.key)
            return True
        except Exception as e:
            return False

    def insert_data(self, table_name: str, data: List[Dict[str, Any]]) -> bool:
        """
        插入数据到指定表

        Args:
            table_name: 要插入数据的表名
            data: 要插入的数据列表，每个元素是一个字典
                 格式: [{"company": "公司名", "phone": "电话", "legal_person": "法人", "contact": "联系人", "notes": "备注"}]

        Returns:
            bool: 插入是否成功
        """
        if not self.client:
            if not self.connect():
                return False

        try:
            result = self.client.table(table_name).insert(data).execute()
            if len(result.data) > 0:
                return True
            else:
                return False
        except Exception as e:
            return False

    def read_data(self, table_name: str, field: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        获取指定表的所有记录

        Args:
            table_name: 要获取记录的表名

        Returns:
            List[Dict]: 记录列表
        """
        if not self.client:
            if not self.connect():
                return []

        try:
            if field is None:
                result = self.client.table(table_name).select(
                    "*").is_("deleted_at", "null").execute()
            else:
                query = self.client.table(table_name).select(
                    "*").is_("deleted_at", "null")
                for key, value in field.items():
                    query = query.eq(key, value)
                result = query.execute()
            return result.data if result is not None and result.data is not None else []
        except Exception as e:
            return []

    def delete_data(self, table_name: str, field: Dict[str, Any] = None) -> bool:
        """
        软删除数据（设置 deleted_at 时间戳）

        Args:
            table_name: 表名
            field: 删除条件字典，如 {"company": "测试公司"}，如果为 None 则删除所有记录（慎用）

        Returns:
            bool: 删除是否成功
        """
        if not self.client:
            if not self.connect():
                return False
        try:
            # 先执行 update 设置删除时间
            query = self.client.table(table_name).update({
                "deleted_at": datetime.now().isoformat()
            })
            # 如果有指定条件，添加 WHERE 条件
            if field is not None:
                for key, value in field.items():
                    query = query.eq(key, value)
            # 执行更新
            result = query.execute()
            # 检查是否有数据被删除
            if result.data and len(result.data) > 0:
                return True
            else:
                return False
        except Exception as e:
            return False

    def update_data(self, table_name: str, field: List[str], data: Dict[str, Any]) -> bool:
        """
        更新数据

        Args:
            table_name: 表名
            field: 用于定位记录的字段列表，作为 WHERE 条件
            data: 要更新的数据字典（包含定位字段和更新字段）

        Returns:
            bool: 更新是否成功
        """
        if not self.client:
            if not self.connect():
                return False
        try:
            # 先执行 update，然后添加 WHERE 条件
            query = self.client.table(table_name).update(data)
            # 根据 field 列表添加查询条件
            for key in field:
                query = query.eq(key, data[key])
            # 执行查询
            result = query.execute()
            # 检查是否有数据被更新
            if result.data and len(result.data) > 0:
                return True
            else:
                return False
        except Exception as e:
            return False

    # ==================== 认证相关方法 ====================

    def generate_token(self) -> str:
        # 获取当前时间
        now = datetime.now()
        # 生成UUID4确保唯一性
        unique_id = str(uuid.uuid4())
        # 拼接令牌原始字符串：时间+周数+UUID+固定密钥
        token_raw = f"{now.isoformat()}{unique_id}{self.token_secret}"
        # 使用MD5算法生成令牌哈希值
        token = hashlib.md5(token_raw.encode()).hexdigest()
        return token

    def sign_up(self, user: Dict[str, Any], unique: List[str] = None) -> bool:
        """
            用户注册
        """
        if not self.client:
            if not self.connect():
                return False
        try:
            # 检查用户是否已存在
            query = self.client.table(self.user_table).select("*")
            if unique:
                # 使用指定的唯一字段进行查询
                for key in unique:
                    query = query.eq(key, user[key])
            else:
                # 使用user字典中的所有字段（排除token和expire）
                for key, value in user.items():
                    if key not in ["token", "expire"]:
                        query = query.eq(key, value)
            result = query.execute()

            # 如果已经有账号，更新token和expire
            if len(result.data) > 0:
                return True
            # 如果没有账号，插入新数据
            insert_result = self.client.table(
                self.user_table).insert(user).execute()
            return True
        except Exception as e:
            print(e)
            return False

    def sign_in(self, user: Dict[str, Any]) -> str:
        """
        用户登录
        """
        if not self.client:
            if not self.connect():
                return ""

        try:
            # 按提供的user字典在user_table数据库中查询是否存在，具体字段出参定义
            query = self.client.table(self.user_table).select("*")
            # 根据user字典中的每个字段动态构建查询条件
            for key, value in user.items():
                query = query.eq(key, value)
            # 执行查询
            result = query.execute()

            # 检查是否有这个用户
            if len(result.data) == 0:
                return ""

            # 如果有这个用户，生成token与过期时限
            user_id = result.data[0]["id"]
            new_token = self.generate_token()
            now = datetime.now()
            expire_time = (
                now + timedelta(seconds=self.token_expire)).isoformat()

            # 更新数据库
            self.client.table(self.user_table).update({
                "token": new_token,
                "expire": expire_time
            }).eq("id", user_id).execute()

            return new_token
        except Exception as e:
            return ""

    def sign_out(self, token: str) -> bool:
        """
        用户退出
        """
        if token is None or token == "" or token == "null":
            return False
        if not self.client:
            if not self.connect():
                return False
        try:
            result = self.client.table(self.user_table).select(
                "*").eq("token", token).execute()
            if result is not None and result.data is not None and len(result.data) > 0:
                # 如果有这个用户，更新token为空
                user_id = result.data[0]["id"]
                self.client.table(self.user_table).update({
                    "token": None,
                    "expire": None
                }).eq("id", user_id).execute()
                return True
            else:
                return False
        except Exception as e:
            return False

    def verify_token(self, token: str):
        """
        验证token是否有效
        """
        if not self.client:
            if not self.connect():
                return False, None

        try:
            user = self.get_user(token)
            if user:
                return user["expire"] > datetime.now().isoformat(), user
            else:
                return False, None
        except Exception as e:
            return False, None

    def get_user(self, token: str) -> Dict[str, Any]:
        """
        获取用户信息
        """
        if token is None or token == "" or token == "null":
            return None
        if not self.client:
            if not self.connect():
                return None
        try:
            result = self.client.table(self.user_table).select(
                "*").eq("token", token).execute()
            if result is not None and result.data is not None and len(result.data) > 0:
                return result.data[0]
            else:
                return None
        except Exception as e:
            return None

    # ==================== 文件库方法 ====================

    def upload_file(self, bucket: str, file_path: str) -> str:
        """
        上传文件到 Supabase 存储

        Args:
            bucket: 存储桶名称
            file_path: 本地文件路径
            remote_name: 远程文件名（可选，默认使用本地文件名）

        Returns:
            str: 上传成功返回文件的公开访问URL，失败返回空字符串
        """
        if not self.client:
            if not self.connect():
                return ""
        try:
            # 检查文件是否存在
            if not os.path.exists(file_path):
                print(f"文件不存在: {file_path}")
                return ""

            # 生成文件名：时间戳YYYYMMDDHHmmssSSS + 随机数 + 原文件后缀
            now = datetime.now()
            # 格式化时间戳：年月日时分秒毫秒
            timestamp = now.strftime("%Y%m%d%H%M%S") + \
                f"{now.microsecond // 10000:02d}"
            # 生成4位随机数
            random_num = random.randint(1000, 9999)
            # 获取原文件后缀
            file_ext = os.path.splitext(file_path)[1]
            # 组合文件名：20251114175433021_2344.jpg
            remote_name = f"{timestamp}_{random_num}{file_ext}"
            # 读取文件内容
            with open(file_path, 'rb') as file:
                file_content = file.read()

            # 上传到 Supabase 存储
            response = self.client.storage.from_(bucket).upload(
                remote_name,
                file_content
            )
            # 检查上传是否成功
            if response:
                # 获取文件的公开访问URL
                public_url = self.get_file_url(bucket, remote_name)
                return public_url
            else:
                return ""
        except Exception as e:
            return ""

    def get_file_url(self, bucket: str, file_name: str) -> str:
        """
        获取文件的公开访问URL（不上传，仅获取链接）

        Args:
            bucket: 存储桶名称
            file_name: 文件名（在存储桶中的路径）

        Returns:
            str: 文件的公开访问URL
        """
        if not self.client:
            if not self.connect():
                return ""
        try:
            # 获取文件的公开访问URL
            public_url = self.client.storage.from_(
                bucket).get_public_url(file_name)
            return public_url
        except Exception as e:
            return ""
