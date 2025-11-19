import redis
import csv
import io
import os
from typing import Optional
from dotenv import load_dotenv


# Redis连接池（懒加载）
_redis_pool = None


def _get_redis_client():
    """
    获取Redis客户端实例（私有方法）

    Returns:
        redis.Redis: Redis客户端实例

    Raises:
        Exception: 当Redis连接失败时抛出
    """
    global _redis_pool

    # 如果连接池不存在，创建新的连接池
    if _redis_pool is None:
        # 加载环境变量
        load_dotenv()

        # Redis连接配置
        REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
        REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
        REDIS_DB = int(os.getenv("REDIS_DB", "0"))
        REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", None)
        # 创建Redis连接池
        _redis_pool = redis.ConnectionPool(
            host=REDIS_HOST,
            port=REDIS_PORT,
            db=REDIS_DB,
            password=REDIS_PASSWORD,
            decode_responses=True,
            max_connections=10
        )

    # 从连接池获取Redis客户端
    return redis.Redis(connection_pool=_redis_pool)


def cache_load(token: str) -> Optional[str]:
    """
    从Redis缓存中读取数据并返回CSV格式字符串

    Args:
        token: 访问令牌，用作Redis的键

    Returns:
        str: CSV格式的字符串数据，如果缓存不存在则返回None

    Raises:
        Exception: 当Redis连接失败或数据处理异常时抛出
    """
    # 使用线程锁确保线程安全
    try:
        # 获取Redis客户端
        redis_client = _get_redis_client()

        # 检查Redis连接是否正常
        redis_client.ping()

        # 使用token作为键从Redis获取缓存数据
        cached_data = redis_client.get(token)

        # 如果缓存不存在，返回None
        if cached_data is None:
            return None

        # 如果缓存数据已经是CSV格式字符串，直接返回
        if isinstance(cached_data, str):
            return cached_data

        # 如果缓存数据是其他格式，尝试转换为CSV格式
        return _convert_to_csv(cached_data)

    except redis.ConnectionError as e:
        # Redis连接异常
        raise Exception(f"Redis连接失败: {str(e)}")
    except redis.TimeoutError as e:
        # Redis超时异常
        raise Exception(f"Redis操作超时: {str(e)}")
    except Exception as e:
        # 其他异常
        raise Exception(f"缓存读取失败: {str(e)}")


def _convert_to_csv(data) -> str:
    """
    将数据转换为CSV格式字符串

    Args:
        data: 需要转换的数据

    Returns:
        str: CSV格式的字符串
    """
    # 创建字符串IO对象
    output = io.StringIO()

    try:
        # 如果数据是字典列表，转换为CSV
        if isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict):
            # 获取字段名
            fieldnames = data[0].keys()
            # 创建CSV写入器
            writer = csv.DictWriter(output, fieldnames=fieldnames)
            # 写入表头
            writer.writeheader()
            # 写入数据行
            writer.writerows(data)

        # 如果数据是二维列表，直接写入CSV
        elif isinstance(data, list) and len(data) > 0 and isinstance(data[0], list):
            writer = csv.writer(output)
            writer.writerows(data)

        # 如果数据是字符串，直接返回
        elif isinstance(data, str):
            return data

        # 其他格式，转换为字符串后返回
        else:
            return str(data)

        # 获取CSV字符串
        csv_string = output.getvalue()
        return csv_string

    finally:
        # 关闭字符串IO对象
        output.close()


def cache_save(token: str, data, expire_time: int = 3600) -> bool:
    """
    将数据存储到Redis缓存中

    Args:
        token: 访问令牌，用作Redis的键
        data: 要缓存的数据
        expire_time: 过期时间（秒），默认1小时

    Returns:
        bool: 存储成功返回True，失败返回False
    """

    try:
        # 获取Redis客户端
        redis_client = _get_redis_client()

        # 将数据转换为CSV格式字符串
        csv_data = _convert_to_csv(data)

        # 存储到Redis并设置过期时间
        result = redis_client.setex(token, expire_time, csv_data)

        return result

    except Exception as e:
        # 记录错误日志（这里简化处理）
        print(f"缓存存储失败: {str(e)}")
        return False


def cache_delete(token: str) -> bool:
    """
    删除Redis缓存中的数据

    Args:
        token: 访问令牌，用作Redis的键

    Returns:
        bool: 删除成功返回True，失败返回False
    """

    try:
        # 获取Redis客户端
        redis_client = _get_redis_client()

        # 删除缓存
        result = redis_client.delete(token)

        return result > 0

    except Exception as e:
        # 记录错误日志（这里简化处理）
        print(f"缓存删除失败: {str(e)}")
        return False
