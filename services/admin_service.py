from multiprocessing import Value
from os import name
from fastmcp import FastMCP  # 导入FastMCP框架
from services.tool import fetch_data  # 导入工具函数

admin_mcp = FastMCP(name="admin")  # 创建计算服务MCP实例

@admin_mcp.tool()
def find_all_staff(access_token: str) -> str:
    """
    获取员工列表，主表，字段为姓名、性别、手机号、是否临时工、入职时间
    1、需要班组字段请合并find_all_team
    2、需要部门字段请合并find_all_department
    3、需要岗位字段请合并find_all_role
    
    Args:
        access_token: 访问令牌
        
    Returns:
        table_token: 员工表令牌
    """
    # 构建请求URL
    url = "/staff/findList"
     
    # 构建请求体数据
    data = {

        "orderBys": [
            {"field": "staffSerialNumber", "order": "ASC"},
            {"field": "staffCreateTime", "order": "DESC"},
            {"field": "staffUpdateTime", "order": "DESC"}
        ],
    }
    
    # 定义需要保留的字段列表
    filtered_fields = {
        "staffName": {"name": "姓名"},
        "staffSex": {"name": "性别", "value": {"1": "男", "2": "女", "3": "未知"}},
        "staffPhone": {"name": "手机号"},
        "staffIsTemporary": {"name": "是否临时工", "value": {"true": "是", "false": "否"}},
        "staffHireDate": {"name": "入职时间"}
    }
    
    # 调用通用工具方法获取并过滤数据

    return fetch_data("员工表", url, data, access_token, filtered_fields) 

@admin_mcp.tool()
def find_all_team(access_token: str) -> str:
    """
    获取班组列表，从表，字段为班组名称、班组编码、是否启用
    
    Args:
        access_token: 访问令牌
        
    Returns:
        table_token: 班组表令牌
    """
    # 构建请求URL
    url = "/group/findList"
     
    # 构建请求体数据
    data = {
        "groupDefaultType": "TEAM",
        "orderBys": [
            {"field": "groupSerialNumber", "order": "ASC"},
            {"field": "groupCreateTime", "order": "DESC"},
        ],
    }
    
    # 定义需要保留的字段列表
    filtered_fields = {
        "groupName": {"name": "班组名称"},
        "groupUserCode": {"name": "班组编码"},
        "groupInUsed": {"name": "是否启用", "value": {"true": "是", "false": "否"}},
    }
    
    # 调用通用工具方法获取并过滤数据

    return fetch_data("班组表", url, data, access_token, filtered_fields) 
  
@admin_mcp.tool()
def find_all_department(access_token: str) -> str:
    """
    获取部门列表，从表，字段为部门名称、部门编码、是否启用
    
    Args:
        access_token: 访问令牌
        
    Returns:
        table_token: 部门表令牌
    """
    # 构建请求URL
    url = "/group/findList"
     
    # 构建请求体数据
    data = {
        "groupDefaultType": "DEPARTMENT",
        "orderBys": [
            {"field": "groupSerialNumber", "order": "ASC"},
            {"field": "groupCreateTime", "order": "DESC"},
        ],
    }
    
    # 定义需要保留的字段列表
    filtered_fields = {
        "groupName": {"name": "部门名称"},
        "groupUserCode": {"name": "部门编码"},
        "groupInUsed": {"name": "是否启用", "value": {"true": "是", "false": "否"}},
    }
    
    # 调用通用工具方法获取并过滤数据

    return fetch_data("部门表", url, data, access_token, filtered_fields) 

@admin_mcp.tool()
def find_all_role(access_token: str) -> str:
    """
    获取岗位列表，从表，字段为岗位名称、岗位编码、是否启用
    
    Args:
        access_token: 访问令牌
        
    Returns:
        table_token: 岗位表令牌
    """
    # 构建请求URL
    url = "/role/findList"
     
    # 构建请求体数据
    data = {"orderBys":[{"field":"roleSerialNumber","order":"ASC"},{"field":"roleCreateTime","order":"DESC"},{"field":"roleUpdateTime","order":"DESC"}]}
    
    # 定义需要保留的字段列表
    filtered_fields = {
        "roleName": {"name": "岗位名称"},
        "roleUserCode": {"name": "岗位编码"},
        "roleInUsed": {"name": "是否启用", "value": {"true": "是", "false": "否"}},
    }
    
    # 调用通用工具方法获取并过滤数据

    return fetch_data("岗位表", url, data, access_token, filtered_fields)   

@admin_mcp.tool()
def find_all_euq(access_token: str) -> str:
    """
    获取设备列表，主表，字段为岗位名称、岗位编码、是否启用
    
    Args:
        access_token: 访问令牌
        
    Returns:
        table_token: 设备表令牌
    """
    # 构建请求URL
    url = "/equ/findList"
     
    # 构建请求体数据
    data = {"orderBys":[{"field":"equSerialNumber","order":"ASC"},{"field":"equCreateTime","order":"DESC"}],"equClazz":"EQUIPMENT"}
    
    # 定义需要保留的字段列表
    filtered_fields = {
        "equName": {"name": "设备名称"},
        "equBrand": {"name": "设备品牌"},
        'equDailyProductionCapacity': {"name": "标准日生产能"},
        'equRunTime': {"name": "标准日运行时长"},
        "equInUsed": {"name": "是否启用", "value": {"true": "是", "false": "否"}},
    }
    
    # 调用通用工具方法获取并过滤数据

    return fetch_data("设备表", url, data, access_token, filtered_fields) 

@admin_mcp.tool()
def find_all_client(access_token: str) -> str:
    """
    获取客户列表，主表，字段为客户名称、客户编码、是否启用
    
    Args:
        access_token: 访问令牌
        
    Returns:
        table_token: 客户表令牌
    """
    # 构建请求URL
    url = "/client/findList"
     
    # 构建请求体数据
    data = {"orderBys":[{"field":"customerCreateTime","order":"DESC"}]}
    
    # 定义需要保留的字段列表
    filtered_fields = {
        "customerName": {"name": "客户名称"},
        "customerShortName": {"name": "客户简称"},
        'customerUserCode': {"name": "客户编码"},
        'customerCurrencyId': {"name": "客户货币"},
        "customerAuditStatus": {"name": "审核状态", "value": {"draft": "草稿", "finish": "已审核", "rejected": "已拒绝"}},
    }
    
    # 调用通用工具方法获取并过滤数据

    return fetch_data("客户表", url, data, access_token, filtered_fields) 

@admin_mcp.tool()
def find_all_contract(access_token: str) -> str:
    """
    获取合同列表，主表，字段为合同名称、合同编码、是否启用
    
    Args:
        access_token: 访问令牌
        
    Returns:
        table_token: 合同表令牌
    """
    # 构建请求URL
    url = "/contract-detail/findList"
     
    # 构建请求体数据
    data = {"orderBys":[{"field":"contractDetailContractCreateTime","order":"DESC"},{"field":"contractDetailParentId","order":"DESC"},{"field":"contractDetailSerialNumber","order":"ASC"}],"contractDetailClazz":"CONTRACT_DETAIL"}
    
    # 定义需要保留的字段列表
    filtered_fields = {
        "contractDetailContractName": {"name": "合同名称"},
        "contractDetailContractReceiptDate": {"name": "合同签订日期"},
        'contractDetailContractUserCode': {"name": "合同编码"},
        'contractDetailExtMatName': {"name": "客户产品名称"},
        'contractDetailQuantity': {"name": "合同数量"},
        'contractDetailSpareQuantity': {"name": "备品数量"},
        'contractDetailUnitPriceIncludingTax': {"name": "合同含税单价"},

    }
    
    # 调用通用工具方法获取并过滤数据

    return fetch_data("合同表", url, data, access_token, filtered_fields) 

@admin_mcp.tool()
def find_all_vm(access_token: str) -> str:
    """
    获取车辆列表，主表，字段为车辆名称、车辆编码、是否启用
    
    Args:
        access_token: 访问令牌
        
    Returns:
        table_token: 车辆表令牌
    """
    # 构建请求URL
    url = "/vm/findList"
     
    # 构建请求体数据
    data = {"orderBys":[{"field":"vmSerialNumber","order":"ASC"},{"field":"vmCreateTime","order":"DESC"},{"field":"vmUpdateTime","order":"DESC"}]}
    
    # 定义需要保留的字段列表
    filtered_fields = {
        "vmPlateNo": {"name": "车辆名称"},
        "vmDefaultType": {"name": "车辆类型", "value": {"TRUCK": "卡车", "SPECIAL": " đặc biệt"}},
        'vmUserCode': {"name": "车辆编码"},
    }
    
    # 调用通用工具方法获取并过滤数据

    return fetch_data("车辆表", url, data, access_token, filtered_fields) 

@admin_mcp.tool()
def find_all_supplier(access_token: str) -> str:
    """
    获取供应商列表，主表，字段为供应商名称、供应商编码、是否启用
    
    Args:
        access_token: 访问令牌
        
    Returns:
        table_token: 车辆表令牌
    """
    # 构建请求URL
    url = "/supplier/findList"
     
    # 构建请求体数据
    data = {"orderBys":[{"field":"supplierCreateTime","order":"DESC"}],"supplierClazz":"XY_USERCENTER_ORGANIZATION"}
    
    # 定义需要保留的字段列表
    filtered_fields = {
        "supplierName": {"name": "车辆名称"},
        'supplierShortName': {"name": "供应商简称"},
        'supplierUserCode': {"name": "供应商编码"},
        'supplierCurrencyId': {"name": "供应商货币"},
        'supplierDefaultInvoiceTypeTaxRate': {"name": "结算周期"},
    }
    
    # 调用通用工具方法获取并过滤数据

    return fetch_data("供应商表", url, data, access_token, filtered_fields) 