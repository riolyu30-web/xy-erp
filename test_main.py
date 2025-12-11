


def test():
    """
    测试auth_login方法 - 登录ERP系统获取访问令牌
    """
    from services.admin_service import find_all_group, find_all_staff
    from services.csv_service import merge_data,get_data
    from services.cache import cache_load

    try:
        
        # auth_login方法无需参数，直接调用
        table_token1 = find_all_staff ("40k9uklnip27hbdau1dpa9ugkuhfo6052ecbhkj8s95rr3wlutshgym95oty")
        print(f"Result: {table_token1}")
        
        table_token2 = find_all_group ("40k9uklnip27hbdau1dpa9ugkuhfo6052ecbhkj8s95rr3wlutshgym95oty")
        print(f"Result: {table_token2}")

        # 测试合并表
        table_token3 = merge_data(table_token1, table_token2)
        print(f"Result: {table_token3}")
        
        table_data = cache_load(table_token3)
        lines = table_data.splitlines()
        print(f"Result: {len(lines)}")
        print(f"Result: {lines[-5:]}")
    except Exception as e:
        print(f"登录失败，错误信息: {str(e)}")

if __name__ == "__main__":
    test()
