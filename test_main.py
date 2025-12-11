


def test():
    """
    测试auth_login方法 - 登录ERP系统获取访问令牌
    """
    from services.admin_service import find_all_staff,find_all_department,find_all_role,find_all_team
    from services.csv_service import merge_data,get_data
    from services.cache import cache_load

    try:
        token = "3p1f2lxeci3t9sk085fpbtwz6ebbrw6yurnu2wiv52w2aru54et8na7qrh3t"
        # auth_login方法无需参数，直接调用
        table_token1 = find_all_staff (token)
        print(f"Result: {table_token1}")
        
        table_token2 = find_all_role (token)
        print(f"Result: {table_token2}")

        table_token3 = find_all_team(token)
        print(f"Result: {table_token3}")


        table_token4 = find_all_department(token)
        print(f"Result: {table_token4}")

        # 测试合并表
        table_token3 = merge_data(table_token1, table_token2)
        print(f"Result: {table_token3}")
        
        table_data = cache_load(table_token3)
        lines = table_data.splitlines()
        #print(f"Result: {len(lines)}")
        print(f"Result: {lines[-5:]}")
    except Exception as e:
        print(f"登录失败，错误信息: {str(e)}")

if __name__ == "__main__":
    test()
