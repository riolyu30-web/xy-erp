import services.tool as tool  # 导入工具模块
from dotenv import load_dotenv  # 导入环境变量加载器
import base64  # 导入base64编码模块
import io  # 导入IO模块
import matplotlib.font_manager as fm  # 导入字体管理器
import matplotlib.pyplot as plt  # 导入matplotlib绘图库
from fastmcp import FastMCP  # 导入FastMCP框架
import matplotlib  # 导入matplotlib库
matplotlib.use('Agg')  # 设置matplotlib后端为Agg，避免GUI依赖

# 加载环境变量
load_dotenv()  # 加载.env文件中的环境变量

chart_mcp = FastMCP(name="chart")  # 创建图表服务MCP实例


@chart_mcp.tool()
def create_bar(data: str, x_axis: str, y_label: str = "数值") -> str:
    """
    生成柱状图并返回图片链接，前提是已 csv_get_data 获得数据
    Args:
        data (str): 数据，用分号分隔，例如"4;1;1;1"
        x_axis (str): X轴标签，用分号分隔，例如"中粮集团;广州希音;新明珠集团;海天味业"
        y_label (str): Y轴标签，默认为"数值"
    Returns:
        str: 图片链接
    """
    chart_data = to_bar_chart(
        data=data,
        x_axis=x_axis,
        y_label=y_label
    )
    # 上传到七牛云
    # result = tool.send_qiniu(chart_data)  # 上传图片
    result = tool.send_supubase(chart_data, bucket="xy-erp") # 上传图片
    if result:  # 上传成功
        return result  # 打印图片URL
    else:  # 上传失败
        return "上传失败"


@chart_mcp.tool()
def create_pie(data: str, x_axis: str, y_label: str = "占比") -> str:
    """
    生成饼图并返回图片链接,数据和标签数量必须匹配
    Args:
        data (str): 数据，用;分号分隔，例如"60%;20%;10%;10%"
        x_axis (str): 标签，用;分号分隔，例如"中粮集团;广州希音;新明珠集团;海天味业"
        y_label (str): 图表标题，默认为"占比"
    Returns:
        str: 图片链接
    """
    chart_data = to_pie_chart(
        data=data,
        x_axis=x_axis,
        y_label=y_label
    )
    # 上传到七牛云
    # result = tool.send_qiniu(chart_data)  # 上传图片

    result = tool.send_supubase(chart_data, bucket="xy-erp") # 上传图片
    if result:  # 上传成功
        return result  # 打印图片URL
    else:  # 上传失败
        return "上传失败"


@chart_mcp.tool()
def create_line(data: str, x_axis: str, line_labels: str, colors: str = "red;blue;green", y_label: str = "数值") -> str:
    """
    生成多条折线图并返回图片链接
    Args:
        data (str): 多组数据，用"|"分隔不同线条，";"分隔数值，例如"4;1;1;1|2;3;4;5|1;2;3;4"
        x_axis (str): X轴标签，用分号分隔，例如"中粮集团;广州希音;新明珠集团;海天味业"
        line_labels (str): 线条标签，用分号分隔，例如"订单数量;销售额;利润"
        colors (str): 颜色设置，用分号分隔，例如"red;blue;green"
        y_label (str): Y轴标签，默认为"数值"
    Returns:
        str: 图片链接
    """
    chart_data = to_line_chart(
        data=data,
        x_axis=x_axis,
        line_labels=line_labels,
        colors=colors,
        y_label=y_label
    )
    # 上传到七牛云
    # result = tool.send_qiniu(chart_data)  # 上传图片

    result = tool.send_supubase(chart_data, bucket="xy-erp") # 上传图片
    if result:  # 上传成功
        return result  # 打印图片URL
    else:  # 上传失败
        return "上传失败"

# 设置中文字体 - 改进版本


def setup_chinese_font():
    """设置中文字体，包含多种fallback选项"""
    # 强制刷新matplotlib字体缓存
    try:
        import matplotlib
        matplotlib.font_manager._rebuild()  # 重建字体缓存
        print("已刷新matplotlib字体缓存")  # 打印刷新信息
    except Exception as e:
        try:
            # 尝试另一种方法清除缓存
            fm.fontManager.__init__()  # 重新初始化字体管理器
            print("已重新初始化字体管理器")  # 打印重新初始化信息
        except Exception as e2:
            print(f"字体缓存刷新失败: {e}, {e2}")  # 打印刷新失败信息

    # 尝试多种中文字体（根据服务器实际安装的字体调整）
    chinese_fonts = [
        'Noto Sans CJK SC',     # Google Noto简体中文字体
        'WenQuanYi Micro Hei',  # 文泉驿微米黑
        'Droid Sans Fallback',  # Droid Sans Fallback（支持中文）
        'SimHei',               # Windows黑体
        'Microsoft YaHei',      # 微软雅黑
        'PingFang SC',          # macOS苹方
        'Hiragino Sans GB',     # macOS冬青黑体
        'Source Han Sans SC',   # 思源黑体
        'DejaVu Sans'           # 最后的fallback
    ]

    # 获取系统可用字体（刷新后）
    available_fonts = [
        f.name for f in fm.fontManager.ttflist]  # 获取系统字体列表

    # 调试信息：打印所有字体（用于调试）
    print(f"matplotlib检测到的字体总数: {len(available_fonts)}")  # 打印字体总数

    # 调试信息：打印找到的真正中文相关字体
    chinese_keywords = ['CJK SC', 'CJK JP', 'CJK TC', 'CJK HK', 'WenQuanYi', 'Micro Hei',
                        'SimHei', 'YaHei', 'PingFang', 'Hiragino', 'Source Han', 'Fallback']  # 中文字体关键词
    real_chinese_fonts = []  # 真正的中文字体列表
    for font in available_fonts:  # 遍历所有字体
        for keyword in chinese_keywords:  # 检查每个中文关键词
            if keyword in font:  # 如果字体名包含中文关键词
                real_chinese_fonts.append(font)  # 添加到中文字体列表
                break  # 找到一个关键词就跳出内层循环

    if real_chinese_fonts:  # 如果找到真正的中文字体
        print(f"找到的中文字体: {real_chinese_fonts[:5]}")  # 打印前5个找到的中文字体
    else:
        print("matplotlib未检测到中文字体，尝试强制指定字体")  # 打印未找到中文字体

    # 寻找第一个可用的中文字体
    selected_font = None  # 初始化选中的字体
    for font in chinese_fonts:  # 遍历中文字体列表
        if font in available_fonts:  # 检查字体是否可用
            selected_font = font  # 记录选中的字体
            plt.rcParams['font.sans-serif'] = [font]  # 设置字体
            print(f"使用预设字体: {font}")  # 打印使用的字体
            break  # 找到可用字体后退出循环

    if not selected_font:  # 如果没有找到预设的中文字体
        # 尝试直接使用检测到的真正中文字体
        if real_chinese_fonts:  # 如果有真正的中文字体
            selected_font = real_chinese_fonts[0]  # 选择第一个中文字体
            plt.rcParams['font.sans-serif'] = [selected_font]  # 设置字体
            print(f"使用检测到的中文字体: {selected_font}")  # 打印使用的字体
        else:
            # 强制指定中文字体名称，即使matplotlib未检测到
            plt.rcParams['font.sans-serif'] = ['Noto Sans CJK SC', 'WenQuanYi Micro Hei',
                                               'Droid Sans Fallback', 'DejaVu Sans']  # 设置多个fallback字体
            print("强制指定中文字体列表，matplotlib将尝试查找这些字体")  # 打印强制指定信息

    plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题


def to_bar_chart(data: str, x_axis: str, y_label: str = "数值") -> str:

    try:
        # 解析数据
        data_values = [float(x.strip())
                       for x in data.split(';')]  # 分割并转换数据为浮点数
        x_labels = [x.strip() for x in x_axis.split(';')]  # 分割X轴标签

        # 检查数据长度是否匹配
        if len(data_values) != len(x_labels):  # 验证数据和标签长度一致
            return "错误：数据和标签数量不匹配"  # 返回错误信息

        # 应用字体设置
        setup_chinese_font()  # 调用字体设置函数

        # 创建图表
        fig, ax = plt.subplots(figsize=(10, 6))  # 创建图表对象，设置尺寸

        # 绘制柱状图
        bars = ax.bar(x_labels, data_values, color=[
                      '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'])  # 绘制柱状图并设置颜色

        # 设置图表属性
        ax.set_ylabel(y_label, fontsize=24)  # 设置Y轴标签，字体大小增大1倍

        # 在柱子上显示数值
        for bar, value in zip(bars, data_values):  # 遍历柱子和数值
            height = bar.get_height()  # 获取柱子高度
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.05,  # 设置文本位置
                    # 添加数值标签，字体大小增大1倍
                    f'{value}', ha='center', va='bottom', fontsize=20)

        # 设置网格
        ax.grid(True, alpha=0.3, axis='y')  # 添加Y轴网格

        # 调整布局
        plt.xticks(rotation=45, ha='right', fontsize=24)  # 旋转X轴标签，设置字体大小
        plt.tight_layout()  # 自动调整布局

        # 保存图片到内存
        img_buffer = io.BytesIO()  # 创建内存缓冲区
        plt.savefig(img_buffer, format='png', dpi=300,
                    bbox_inches='tight')  # 保存图片到缓冲区
        img_buffer.seek(0)  # 重置缓冲区指针

        # 转换为base64编码
        img_base64 = base64.b64encode(
            img_buffer.getvalue()).decode('utf-8')  # 编码为base64字符串

        # 清理资源
        plt.close(fig)  # 关闭图表
        img_buffer.close()  # 关闭缓冲区

        # 返回base64编码的图片数据
        return f"data:image/png;base64,{img_base64}"  # 返回完整的data URL格式

    except Exception as e:  # 捕获异常
        return f"生成图表失败: {str(e)}"  # 返回错误信息


def to_pie_chart(data: str, x_axis: str, y_label: str = "占比") -> str:
    """
    生成饼图的具体实现
    Args:
        data (str): 数据，用分号分隔，例如"60%;20%;10%;10%"
        x_axis (str): 标签，用分号分隔，例如"中粮集团;广州希音;新明珠集团;海天味业"
        y_label (str): 图表标题，默认为"占比"
    Returns:
        str: base64编码的图片数据
    """
    try:
        # 解析数据 - 处理百分比格式
        data_values = []  # 初始化数据值列表
        for x in data.split(';'):  # 分割数据字符串
            value_str = x.strip().replace('%', '')  # 去除空格和百分号
            data_values.append(float(value_str))  # 转换为浮点数并添加到列表

        x_labels = [x.strip() for x in x_axis.split(';')]  # 分割标签字符串

        # 检查数据长度是否匹配
        if len(data_values) != len(x_labels):  # 验证数据和标签长度一致
            return "错误：数据和标签数量不匹配"  # 返回错误信息

        # 应用字体设置
        setup_chinese_font()  # 调用字体设置函数

        # 创建图表
        fig, ax = plt.subplots(figsize=(10, 8))  # 创建图表对象，设置尺寸

        # 定义颜色
        colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99',
                  '#ff99cc', '#c2c2f0', '#ffb3e6']  # 饼图颜色列表

        # 绘制饼图
        wedges, texts, autotexts = ax.pie(data_values, labels=x_labels, colors=colors[:len(data_values)],
                                          # 绘制饼图
                                          # 字体大小增大1倍
                                          autopct='%1.1f%%', startangle=90, textprops={'fontsize': 20})

        # 设置标签字体大小
        for text in texts:  # 遍历标签文本对象
            text.set_fontsize(24)  # 设置标签字体大小

        # 设置图表标题
        ax.set_title(y_label, fontsize=28, fontweight='bold',
                     pad=20)  # 设置标题，字体大小增大1倍

        # 确保饼图是圆形
        ax.axis('equal')  # 设置坐标轴比例相等

        # 调整布局
        plt.tight_layout()  # 自动调整布局

        # 保存图片到内存
        img_buffer = io.BytesIO()  # 创建内存缓冲区
        plt.savefig(img_buffer, format='png', dpi=300,
                    bbox_inches='tight')  # 保存图片到缓冲区
        img_buffer.seek(0)  # 重置缓冲区指针

        # 转换为base64编码
        img_base64 = base64.b64encode(
            img_buffer.getvalue()).decode('utf-8')  # 编码为base64字符串

        # 清理资源
        plt.close(fig)  # 关闭图表
        img_buffer.close()  # 关闭缓冲区

        # 返回base64编码的图片数据
        return f"data:image/png;base64,{img_base64}"  # 返回完整的data URL格式

    except Exception as e:  # 捕获异常
        return f"生成饼图失败: {str(e)}"  # 返回错误信息


def to_line_chart(data: str, x_axis: str, line_labels: str, colors: str = "red;blue;green", y_label: str = "数值") -> str:
    """
    生成多条折线图的具体实现
    Args:
        data (str): 多组数据，用"|"分隔不同线条，";"分隔数值，例如"4;1;1;1|2;3;4;5|1;2;3;4"
        x_axis (str): X轴标签，用分号分隔，例如"中粮集团;广州希音;新明珠集团;海天味业"
        line_labels (str): 线条标签，用分号分隔，例如"订单数量;销售额;利润"
        colors (str): 颜色设置，用分号分隔，例如"red;blue;green"
        y_label (str): Y轴标签，默认为"数值"
    Returns:
        str: base64编码的图片数据
    """
    try:
        # 解析多组数据
        data_lines = data.split('|')  # 按"|"分割不同线条的数据
        all_line_data = []  # 存储所有线条的数据
        for line_data in data_lines:  # 遍历每条线的数据
            line_values = [float(x.strip())
                           for x in line_data.split(';')]  # 分割并转换为浮点数
            all_line_data.append(line_values)  # 添加到总数据列表

        # 解析X轴标签
        x_labels = [x.strip() for x in x_axis.split(';')]  # 分割X轴标签

        # 解析线条标签
        labels = [x.strip() for x in line_labels.split(';')]  # 分割线条标签

        # 解析颜色
        color_list = [x.strip() for x in colors.split(';')]  # 分割颜色列表

        # 检查数据一致性
        if not all(len(line) == len(x_labels) for line in all_line_data):  # 检查每条线的数据长度是否与X轴标签一致
            return "错误：数据长度与X轴标签数量不匹配"  # 返回错误信息

        if len(all_line_data) != len(labels):  # 检查线条数量与标签数量是否一致
            return "错误：线条数量与标签数量不匹配"  # 返回错误信息

        # 应用字体设置
        setup_chinese_font()  # 调用字体设置函数

        # 创建图表
        fig, ax = plt.subplots(figsize=(12, 8))  # 创建图表对象，设置尺寸

        # 绘制多条折线
        for i, (line_data, label) in enumerate(zip(all_line_data, labels)):  # 遍历每条线的数据和标签
            color = color_list[i % len(color_list)]  # 循环使用颜色列表
            ax.plot(x_labels, line_data, marker='o', linewidth=2, markersize=6,  # 绘制折线图
                    label=label, color=color)  # 设置标签和颜色

        # 设置图表属性
        ax.set_ylabel(y_label, fontsize=24)  # 设置Y轴标签，字体大小增大1倍
        ax.set_xlabel('', fontsize=24)  # 设置X轴标签为空，字体大小增大1倍

        # 添加图例
        ax.legend(loc='upper right', fontsize=20)  # 添加图例，字体大小增大1倍

        # 设置网格
        ax.grid(True, alpha=0.3)  # 添加网格

        # 在数据点上显示数值
        for i, (line_data, label) in enumerate(zip(all_line_data, labels)):  # 遍历每条线的数据
            for j, value in enumerate(line_data):  # 遍历每个数据点
                ax.annotate(f'{value}', (j, value), textcoords="offset points",  # 添加数值标注
                            # 设置标注位置和样式，字体大小增大1倍
                            xytext=(0, 10), ha='center', fontsize=16)

        # 调整布局
        plt.xticks(rotation=45, ha='right', fontsize=24)  # 旋转X轴标签，设置字体大小
        plt.tight_layout()  # 自动调整布局

        # 保存图片到内存
        img_buffer = io.BytesIO()  # 创建内存缓冲区
        plt.savefig(img_buffer, format='png', dpi=300,
                    bbox_inches='tight')  # 保存图片到缓冲区
        img_buffer.seek(0)  # 重置缓冲区指针

        # 转换为base64编码
        img_base64 = base64.b64encode(
            img_buffer.getvalue()).decode('utf-8')  # 编码为base64字符串

        # 清理资源
        plt.close(fig)  # 关闭图表
        img_buffer.close()  # 关闭缓冲区

        # 返回base64编码的图片数据
        return f"data:image/png;base64,{img_base64}"  # 返回完整的data URL格式

    except Exception as e:  # 捕获异常
        return f"生成折线图失败: {str(e)}"  # 返回错误信息
