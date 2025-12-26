import json  # 导入json处理模块
import os  # 导入操作系统模块
from jinja2 import Template  # 导入Jinja2模板引擎

# 定义Jinja2模板字符串
TEMPLATE_STR = """from fastmcp import FastMCP  # 导入FastMCP框架
from services.tool import fetch_data  # 导入工具函数
from datetime import datetime, timedelta # 导入日期时间模块
import json  # 导入JSON库
{{ service_name }}_mcp = FastMCP(name="{{ service_name }}")  # 创建计算服务MCP实例

{% for tool in tools %}
@{{ service_name }}_mcp.tool()  # 注册工具
def {{ tool.function_name }}({{ tool.args_str }}) -> str:  # 定义工具函数
    \"\"\"
    {{ tool.alias_name }}，{{ tool.remark }}
    {% for assoc in tool.associated_tables %}
    {{ assoc.remark }},要调用csv_merge合并表，左表:{{ assoc.table_left }}，右表:{{ assoc.table_right }}，左键:{{ assoc.key_left }}，右键:{{ assoc.key_right }}
    {% endfor %}
    Args:
        access_token: 访问令牌
        {% for filter in tool.filters %}
        {{ filter.field }}: {{ filter.remark }}，格式为{{ filter.format }}
        {% endfor %}     
    Returns:
        成功返回：表访问令牌，有效字段说明，样本数据
        失败返回：错误原因
    \"\"\"
    # 构建请求URL
    url = "{{ tool.api_name }}"  # API地址

    {%- for filter in tool.filters %}
    {%- set has_default = false %}
    {%- if filter.remark is mapping %}
        {%- set has_default = true %}
    {%- elif "当天" in filter.remark or "30天前" in filter.remark or "一周前" in filter.remark %}
        {%- set has_default = true %}
    {%- endif %}
    {%- if has_default %}
    if {{ filter.field }} is None:  # 如果{{ filter.field }}为空
        {%- if filter.remark is mapping %}
        {{ filter.field }} = "{{ filter.format }}"  # 默认值为格式字符串
        {%- elif "当天" in filter.remark %}
        {{ filter.field }} = datetime.datetime.now().strftime("{{ filter.format }}")  # 默认为今天
        {%- elif "30天前" in filter.remark %}
        {{ filter.field }} = (datetime.datetime.now() - datetime.timedelta(days=30)).strftime("{{ filter.format }}")  # 默认为30天前
        {%- elif "一周前" in filter.remark %}
        {{ filter.field }} = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime("{{ filter.format }}")  # 默认为一周前
        {%- endif %}
    {%- endif %}
    {%- endfor %}
    # 构建请求体数据
    data = {
        {% for k, v in tool.request_fixed.items() %}
        "{{ k }}": "{{ v }}",  # 固定参数
        {% endfor %}
        {% for filter in tool.filters %}
        "{{ filter.field }}": {{ filter.field }},  # 动态参数
        {% endfor %}
        {% if tool.order_bys %}
        "orderBys": [  # 排序规则
            {% for order in tool.order_bys %}
            {{ order }}{{ "," if not loop.last else "" }}  # 排序项
            {% endfor %}
        ]  # 排序结束
        {% endif %}
    }  # 数据字典结束
    # 定义需要保留的字段列表
    filtered_fields = {
        {% for key, val in tool.response_items %}
        "{{ key }}": {{ val }}{{ "," if not loop.last else "" }}  # 字段映射
        {% endfor %}
    }  # 过滤字段字典结束
    meaning_list = {
        {% for key, val in tool.meaning_items %}
        "{{ key }}": "{{ val }}"{{ "," if not loop.last else "" }}  # 字段含义
        {% endfor %}
    }  # 含义字典结束
    # 调用通用工具方法获取并过滤数据
    return fetch_data("{{ tool.alias_name }}", url, data, access_token, filtered_fields, meaning_list)  # 返回数据  
{% endfor %}
"""

TEST_TEMPLATE_STR = """
import sys # 导入sys模块
import os # 导入os模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # 将上上级目录添加到系统路径
from datetime import datetime, timedelta # 导入日期时间模块
from services.auth_service import auth_login # 导入登录认证模块
from services.tool import fetch_data  # 导入工具函数
import json # 导入json模块

{% for tool in tools %}
def {{ tool.function_name }}_test(access_token: str):  # 定义测试函数
    \"\"\"
    测试 {{ tool.api_name }}
    \"\"\"
    # 构建请求URL
    url = "{{ tool.api_name }}"  # API地址

    {%- for filter in tool.filters %}
    {%- if "From" in filter.field or "start" in filter.field %}
    {{ filter.field }} = (datetime.now() - timedelta(days=30)).strftime("{{ filter.format }}")
    {%- elif "To" in filter.field or "end" in filter.field %}
    {{ filter.field }} = datetime.now().strftime("{{ filter.format }}")
    {%- else %}
    {{ filter.field }} = None # 需要用户提供默认值
    {%- endif %}
    {%- endfor %}

    # 构建请求体数据
    data = {
        {% for k, v in tool.request_fixed.items() %}
        "{{ k }}": "{{ v }}",  # 固定参数
        {% endfor %}
        {% for filter in tool.filters %}
        "{{ filter.field }}": {{ filter.field }},  # 动态参数
        {% endfor %}
        {% if tool.order_bys %}
        "orderBys": [  # 排序规则
            {% for order in tool.order_bys %}
            {{ order }}{{ "," if not loop.last else "" }}  # 排序项
            {% endfor %}
        ]  # 排序结束
        {% endif %}
    }  # 数据字典结束

    # 定义需要保留的字段列表
    filtered_fields = {
        {% for key, val in tool.response_items %}
        "{{ key }}": {{ val }}{{ "," if not loop.last else "" }}  # 字段映射
        {% endfor %}
    }  # 过滤字段字典结束

    meaning_list = {
        {% for key, val in tool.meaning_items %}
        "{{ key }}": "{{ val }}"{{ "," if not loop.last else "" }}  # 字段含义
        {% endfor %}
    }  # 含义字典结束

    # 调用通用工具方法获取并过滤数据
    fetch_data("{{ tool.alias_name }}", url, data, access_token, filtered_fields, meaning_list, debug_mode=True)
{% endfor %}

if __name__ == "__main__":
    access_token = auth_login()  # 获取访问令牌
    {% for tool in tools %}
    {{ tool.function_name }}_test(access_token)  # 调用测试函数
    {% endfor %}
"""

def generate_service_script(json_path: str):  # 定义生成服务脚本的函数
    """
    根据JSON配置文件生成Python服务脚本
    """
    # 读取JSON文件
    with open(json_path, 'r', encoding='utf-8') as f:  # 打开JSON文件
        config = json.load(f)  # 加载JSON内容

    # 获取mcp列表，如果不存在则尝试从根节点获取旧格式并包装成列表
    mcp_list = config.get("mcp", [])
    if not mcp_list:
        # 兼容旧格式，尝试直接获取service_name
        service_name = config.get("service_name")
        if service_name:
            mcp_list = [config]

    if not mcp_list:
        print("No mcp services found in JSON.")
        return

    # 遍历每个MCP服务配置
    for service_config in mcp_list:
        service_name = service_config.get("service_name", "default")  # 获取服务名称
        tools_data = service_config.get("tools", [])  # 获取工具列表
        relations_data = service_config.get("relations", [])  # 获取全局关联表信息

        if not tools_data:  # 如果没有工具定义
            print(f"No tools found for service {service_name}.")  # 打印提示
            continue  # 继续下一个服务

        output_dir = os.path.dirname(os.path.abspath(__file__)) # 默认为当前文件所在目录
        output_dir  = os.path.join(output_dir, "services")  # 拼接services目录
        output_path = os.path.join(output_dir, f"{service_name}_service.py")  # 拼接输出文件路径

        # 准备模板数据
        tools_context = []  # 初始化工具上下文列表

        for tool in tools_data:  # 遍历每一个工具定义
            api_name = tool.get("api_name", "")  # 获取API路径
            function_name = tool.get("function_name", api_name.strip("/").replace("/", "_"))  # 根据API路径生成函数名
            alias_name = tool.get("name", "")  # 获取别名
            remark = tool.get("remark", "")  # 获取备注
            filters = tool.get("filter", [])  # 获取过滤器配置
            request_config = tool.get("request", {})  # 获取请求配置
            order_bys = tool.get("orderBys", [])  # 获取排序配置
            response_config = tool.get("response", {})  # 获取响应配置

            # 处理参数字符串
            args_str_list = ["access_token: str"]  # 初始化参数列表
            for f in filters:  # 遍历过滤器
                field_name = f.get("field")  # 获取字段名
                if field_name:  # 如果字段名存在
                    args_str_list.append(f"{field_name}:str=None")  # 添加可选参数
            args_str = ",".join(args_str_list)  # 拼接参数字符串

            # 处理字段名列表字符串
            field_names = [v.get("name", "") for k, v in response_config.items() if v.get("name")]  # 获取所有字段名
            field_names_str = ",".join(field_names)  # 拼接字段名

            # 处理关联表信息
            associated_tables = []  # 初始化关联表列表
        

            for rel in relations_data:  # 遍历全局关联表
                # 只处理左表为当前工具别名的关联
                if rel.get("table_left") == alias_name or rel.get("table_right") == alias_name:
                    table_left = rel.get("table_left")
                    key_left = rel.get("key_left")               
                    # 处理右表字段名称
                    table_right = rel.get("table_right")
                    key_right = rel.get("key_right")

                    associated_tables.append({
                        "remark": rel.get("remark", "关联表"),  # 备注作为名称
                        "table_left": table_left,  # 左表名
                        "table_right": table_right,  # 右表名
                        "key_left": key_left,  # 左键（字段名）
                        "key_right": key_right  # 右键（字段名）
                    })



            # 处理过滤器格式
            processed_filters = []  # 初始化处理后的过滤器列表
            for f in filters:  # 遍历过滤器
                fmt = f.get("format", "").replace("yyyy", "%Y").replace("MM", "%m").replace("dd", "%d").replace("HH", "%H").replace("mm", "%M").replace("ss", "%S")  # 格式转换
                f_copy = f.copy()  # 复制字典
                f_copy["format"] = fmt  # 更新格式
                processed_filters.append(f_copy)  # 添加到列表

            # 处理Response Items
            response_items = []  # 初始化响应项列表
            meaning_items = []  # 初始化含义项列表
            for key, val in response_config.items():  # 遍历响应配置
                name = val.get("name")  # 获取中文名
                values = val.get("values")  # 获取枚举值
                
                val_dict = {"name": name}  # 构建值字典
                if values:  # 如果有枚举值
                    val_dict["values"] = values  # 添加枚举值
                
                response_items.append((key, json.dumps(val_dict, ensure_ascii=False)))  # 添加响应项
                meaning_items.append((name, val.get("remark", val.get("meaning", name))))  # 添加含义项

            # 处理Order Bys
            order_bys_json = [json.dumps(o) for o in order_bys]  # 转换为JSON字符串

            tools_context.append({
                "function_name": function_name,  # 函数名
                "args_str": args_str,  # 参数字符串
                "remark": remark,  # 备注
                "field_names_str": field_names_str,  # 字段名字符串
                "associated_tables": associated_tables,  # 关联表信息
                "filters": processed_filters,  # 过滤器信息
                "api_name": api_name,  # API路径
                "request_fixed": request_config,  # 固定请求参数
                "order_bys": order_bys_json,  # 排序规则
                "response_items": response_items,  # 响应项
                "meaning_items": meaning_items,  # 含义项
                "alias_name": alias_name  # 别名
            })  # 添加工具上下文

        # 渲染模板
        template = Template(TEMPLATE_STR)  # 创建模板对象
        rendered_code = template.render(service_name=service_name, tools=tools_context)  # 渲染代码

        # 写入文件
        os.makedirs(os.path.dirname(output_path), exist_ok=True) # 确保输出目录存在
        with open(output_path, 'w', encoding='utf-8') as f:  # 打开输出文件
            f.write(rendered_code)  # 写入代码内容
        
        print(f"Generated {output_path}")  # 打印成功信息

        # 渲染测试模板
        test_template = Template(TEST_TEMPLATE_STR)  # 创建测试模板对象
        rendered_test_code = test_template.render(service_name=service_name, tools=tools_context)  # 渲染测试代码

        # 写入测试文件
        test_output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "testcase") # 测试用例目录
        test_output_path = os.path.join(test_output_dir, f"testcase_{service_name}.py")  # 测试用例文件路径
        os.makedirs(os.path.dirname(test_output_path), exist_ok=True)  # 确保输出目录存在
        with open(test_output_path, 'w', encoding='utf-8') as f:  # 打开输出文件
            f.write(rendered_test_code)  # 写入代码内容
        
        print(f"Generated {test_output_path}")  # 打印成功信息

def rebulid_main_mcp():
    """
    重新构建主MCP脚本
    """
    import os # 导入os模块

    services_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "services") # 定义services目录路径
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "main_mcp.py") # 定义输出文件路径

    # 定义Jinja2模板
    main_mcp_template_str = """from fastmcp import FastMCP # 导入FastMCP
{% for prefix in prefixes %}
from services.{{ prefix }}_service import {{ prefix }}_mcp
{%- endfor %}

mcp = FastMCP("xy-erp-mcp") # 实例化FastMCP
{% for prefix in prefixes %}
mcp.mount({{ prefix }}_mcp, prefix="{{ prefix }}")
{%- endfor %}

def main(): # 定义主函数
    mcp.run(transport='sse', port=9050, host='0.0.0.0') # 运行MCP服务

if __name__ == "__main__": # 判断是否为主程序入口
    main() # 调用主函数
"""

    prefixes = [] # 初始化前缀列表
    for filename in os.listdir(services_dir): # 遍历services目录下的所有文件
        if filename.endswith("_service.py"): # 检查文件是否以_service.py结尾
            prefix = filename.replace("_service.py", "") # 提取文件名前缀
            if prefix: # 确保前缀不为空
                prefixes.append(prefix) # 将前缀添加到列表中
    
    template = Template(main_mcp_template_str) # 创建模板对象
    content = template.render(prefixes=sorted(prefixes)) # 渲染模板

    with open(output_path, 'w', encoding='utf-8') as f: # 打开输出文件
        f.write(content) # 写入生成的内容
        
    print(f"Generated {output_path}") # 打印生成成功信息

if __name__ == "__main__":  # 主程序入口
    import sys  # 导入系统模块
    # 如果提供了命令行参数
    if len(sys.argv) > 1:
        json_file = sys.argv[1]  # 获取JSON文件路径
        generate_service_script(json_file)  # 调用生成函数
    else:
        # 默认测试
        generate_service_script("e:/tx-erp/erp-service/mcp.json")  # 默认生成staff.json对应脚本
    rebulid_main_mcp()
