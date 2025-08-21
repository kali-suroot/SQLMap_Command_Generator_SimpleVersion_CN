import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import subprocess

def generate_sqlmap_command():
    """
    生成SQLMap命令的核心函数
    从GUI界面获取用户输入的各种参数，组合成完整的SQLMap命令
    """
    try:
        # 获取SQLMap路径
        sqlmap_path = sqlmap_path_entry.get().strip()
        if not sqlmap_path:
            messagebox.showerror("错误", "请先设置SQLMap路径！")
            return
            
        # 获取基本参数
        url = url_entry.get().strip()
        if not url:
            messagebox.showerror("错误", "URL不能为空！")
            return
            
        # 获取请求相关参数
        method = method_var.get()
        data = data_entry.get().strip()
        cookie = cookie_entry.get().strip()
        user_agent = user_agent_var.get()
        referer = referer_entry.get().strip()
        proxy = proxy_entry.get().strip()
        
        # 获取性能相关参数
        threads = threads_var.get()
        delay = delay_var.get()
        timeout = timeout_var.get()
        retries = retries_var.get()
        
        # 获取注入相关参数
        risk = risk_var.get() #风险等级
        level = level_var.get() #测试等级
        dbms = dbms_var.get() #数据库
        technique = technique_var.get().split(' ')[0]  # 提取技术代码（第一个字符）
        tamper = tamper_entry.get().strip()
        batch = batch_var.get()
        
        # 获取输出参数
        output = output_entry.get().strip()
        
        # 获取枚举相关参数
        enum_db = enum_db_var.get()
        enum_tables = enum_tables_var.get()
        enum_columns = enum_columns_var.get()
        enum_schema = enum_schema_var.get()
        enum_all = enum_all_var.get()
        exclude_db = exclude_entry.get().strip()
        dump = dump_var.get()
        dump_all = dump_all_var.get()
        where = where_entry.get().strip()
        start = start_var.get()
        stop = stop_var.get()
        
        # 获取爆破流程参数
        select_db = select_db_entry.get().strip()
        select_table = select_table_entry.get().strip()
        
        # 构建基本命令 - 使用配置的SQLMap路径
        command = f"python \"{sqlmap_path}\""
        
        # 目标设置（必需）
        command += f" -u \"{url}\""

        # 请求设置
        if method != "GET":
            command += f" --method={method}"
        if data:
            command += f" --data=\"{data}\""
        if cookie:
            command += f" --cookie=\"{cookie}\""
        if user_agent != "default":
            if user_agent == "random":
                command += " --random-agent"
            else:
                command += f" --user-agent=\"{user_agent}\""
        if referer:
            command += f" --referer=\"{referer}\""
        if proxy:
            command += f" --proxy=\"{proxy}\""
        
        # 性能设置
        if threads != "1":
            command += f" --threads={threads}"
        if delay != "0":
            command += f" --delay={delay}"
        if timeout != "30":
            command += f" --timeout={timeout}"
        if retries != "3":
            command += f" --retries={retries}"
        
        # 注入设置
        if risk != "1":
            command += f" --risk={risk}"
        if level != "1":
            command += f" --level={level}"
        if dbms != "auto":
            command += f" --dbms={dbms}"
        if technique != "BEUSTQ":
            command += f" --technique={technique}"
        if tamper:
            command += f" --tamper=\"{tamper}\""
        if batch:
            command += " --batch"
        
        # 枚举设置（数据库爆破流程）
        if enum_db:
            command += " --dbs"  # 获取数据库名称
            
        if enum_tables and select_db:
            command += f" -D {select_db} --tables"  # 获取表名
            
        if enum_columns and select_db and select_table:
            command += f" -D {select_db} -T {select_table} --columns"  # 获取列名
            
        if enum_schema:
            command += " --schema"  # 枚举数据库结构
            
        if enum_all:
            command += " --all"  # 枚举所有内容
            
        if exclude_db:
            command += f" --exclude-sysdbs={exclude_db}"  # 排除系统数据库
            
        if dump and select_db and select_table:
            command += f" -D {select_db} -T {select_table} --dump"  # 转储表数据
            
        if dump_all:
            command += " --dump-all"  # 转储所有数据
            
        if where:
            command += f" --where=\"{where}\""  # WHERE条件限制
            
        if start != "1":
            command += f" --start={start}"  # 起始行
            
        if stop != "100":
            command += f" --stop={stop}"  # 结束行
        
        # 输出设置
        if output:
            command += f" --output-dir={output}"  # 输出目录
        
        # 在文本框中显示生成的命令
        command_text.delete(1.0, tk.END)
        command_text.insert(tk.END, command)
        
    except Exception as e:
        messagebox.showerror("生成错误", f"生成命令时出错: {str(e)}")

def clear_fields():
    """
    清除所有输入字段的函数
    重置界面到初始状态
    """
    # 保存SQLMap路径
    saved_sqlmap_path = sqlmap_path_entry.get()
    
    # 清除所有输入框
    for entry in all_entries:
        if isinstance(entry, tk.Entry) or isinstance(entry, ttk.Entry):
            entry.delete(0, tk.END)
        elif isinstance(entry, ttk.Combobox):
            entry.set(entry['values'][0])
        elif isinstance(entry, tk.Text):
            entry.delete(1.0, tk.END)
    
    # 重置所有变量
    for var in all_vars:
        if isinstance(var, tk.BooleanVar):
            var.set(False)
        elif isinstance(var, tk.StringVar) and var not in default_vars:
            var.set("1")
    
    # 重置特殊控件到默认值
    method_var.set("GET")
    user_agent_var.set("default")
    dbms_var.set("auto")
    technique_var.set("BEUSTQ (全部)")
    threads_var.set("1")
    delay_var.set("0")
    timeout_var.set("30")
    retries_var.set("3")
    risk_var.set("1")
    level_var.set("1")
    start_var.set("1")
    stop_var.set("100")
    command_text.delete(1.0, tk.END)
    
    # 恢复SQLMap路径
    sqlmap_path_entry.delete(0, tk.END)
    sqlmap_path_entry.insert(0, saved_sqlmap_path)
    
    # 清除爆破结果区域
    db_name_text.delete(1.0, tk.END)
    table_name_text.delete(1.0, tk.END)
    columns_text.delete(1.0, tk.END)
    
    # 重置所有变量
    for var in all_vars:
        if isinstance(var, tk.BooleanVar):
            var.set(False)
        elif isinstance(var, tk.StringVar) and var not in default_vars:
            var.set("1")
    
    # 重置特殊控件到默认值
    method_var.set("GET")
    user_agent_var.set("default")
    dbms_var.set("auto")
    technique_var.set("BEUSTQ (全部)")
    threads_var.set("1")
    delay_var.set("0")
    timeout_var.set("30")
    retries_var.set("3")
    risk_var.set("1")
    level_var.set("1")
    start_var.set("1")
    stop_var.set("100")
    command_text.delete(1.0, tk.END)
    
    # 清除爆破结果区域
    db_name_text.delete(1.0, tk.END)
    table_name_text.delete(1.0, tk.END)
    columns_text.delete(1.0, tk.END)

def clear_sqlmap():
    """
    生成清除SQLMap缓存命令（不执行）
    """
    try:
        sqlmap_path = sqlmap_path_entry.get().strip()
        if not sqlmap_path:
            messagebox.showerror("错误", "请先设置SQLMap路径！")
            return
            
        command = f"python \"{sqlmap_path}\" --purge"
        
        # 只显示命令，不执行
        command_text.delete(1.0, tk.END)
        command_text.insert(tk.END, command)
        
    except Exception as e:
        messagebox.showerror("执行错误", f"生成清除缓存命令时出错: {str(e)}")

def sqlmap_path():
    """
    执行命令框中显示的命令
    """
    try:
        # 获取命令框中的命令
        command = command_text.get(1.0, tk.END).strip()
        if not command:
            messagebox.showerror("错误", "命令框中没有命令！")
            return
            
        # 直接在新窗口中执行命令，不提示
        subprocess.Popen(f'start cmd /k "{command}"', shell=True)
        
    except Exception as e:
        messagebox.showerror("执行错误", f"执行命令时出错: {str(e)}")

# 创建主窗口
root = tk.Tk()
root.title("SQLMap命令生成器 v3.1 by:kali-suroot")
root.geometry("670x670")  # 设置窗口尺寸

# 创建Notebook（选项卡容器）
notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True, padx=10, pady=10)

# 创建各个选项卡框架
basic_frame = ttk.Frame(notebook)        # 基本设置
injection_frame = ttk.Frame(notebook)    # 注入设置
enum_frame = ttk.Frame(notebook)         # 枚举设置
performance_frame = ttk.Frame(notebook)  # 性能设置
output_frame = ttk.Frame(notebook)       # 输出设置

# 添加选项卡到Notebook
notebook.add(basic_frame, text="基本设置")
notebook.add(injection_frame, text="注入设置")
notebook.add(enum_frame, text="枚举设置")
notebook.add(performance_frame, text="性能设置")
notebook.add(output_frame, text="输入输出设置")

# 存储所有输入控件的列表（用于清除功能）
all_entries = []
all_vars = []
default_vars = []

# ====================== 基本设置选项卡 ======================

"""URL填写"""
ttk.Label(basic_frame, text="目标URL (必填):").grid(row=0, column=0, padx=5, pady=5, sticky="e") # 创建"目标URL"标签
url_entry = ttk.Entry(basic_frame, width=60)  # 创建URL输入框（宽度60个字符）
url_entry.grid(row=0, column=1, columnspan=3, padx=5, pady=5, sticky="we") # 将URL输入框放置在网格的第0行第1列，跨3列，左右填充5像素，上下填充5像素，水平拉伸
all_entries.append(url_entry) # 将URL输入框添加到所有输入控件列表中（用于清除功能）

"""请求方法"""
ttk.Label(basic_frame, text="请求方法:").grid(row=1, column=0, padx=5, pady=5, sticky="e") # 创建"请求方法"标签，第1行第0列，左右填充5像素，上下填充5像素，水平拉伸
method_var = tk.StringVar(value="GET") # 创建请求方法变量，默认值为"GET"
method_combo = ttk.Combobox(basic_frame, textvariable=method_var, width=15) # 创建请求方法下拉框，宽度为15
method_combo['values'] = ("GET", "POST", "PUT", "HEAD") # 设置下拉框的选项值
method_combo.grid(row=1, column=1, padx=5, pady=5, sticky="w") # 将下拉框放置在网格的第1行第1列
all_entries.append(method_combo)  # 将下拉框添加到所有输入控件列表中
all_vars.append(method_var)  # 将变量添加到所有变量列表中

"""POST数据"""
ttk.Label(basic_frame, text="POST数据:").grid(row=2, column=0, padx=5, pady=5, sticky="e") # 创建"POST数据"标签
data_entry = ttk.Entry(basic_frame, width=60) # 创建POST数据输入框
data_entry.grid(row=2, column=1, columnspan=3, padx=5, pady=5, sticky="we") # 将输入框放置在网格的第2行第1列，跨3列
all_entries.append(data_entry)

"""cookie"""
ttk.Label(basic_frame, text="Cookie:").grid(row=3, column=0, padx=5, pady=5, sticky="e")# 创建"Cookie"标签
cookie_entry = ttk.Entry(basic_frame, width=60)# 创建Cookie输入框
cookie_entry.grid(row=3, column=1, columnspan=3, padx=5, pady=5, sticky="we")# 将输入框放置在网格的第3行第1列，跨3列
all_entries.append(cookie_entry)

"""UA"""
ttk.Label(basic_frame, text="User-Agent:").grid(row=4, column=0, padx=5, pady=5, sticky="e") # 创建"User-Agent"标签
user_agent_var = tk.StringVar(value="default") # 创建User-Agent变量，默认值为"default"
user_agent_combo = ttk.Combobox(basic_frame, textvariable=user_agent_var, width=20) # 创建User-Agent下拉框
user_agent_combo['values'] = ("default", "random", "Mozilla/5.0", "Googlebot/2.1") # 设置下拉框选项值
user_agent_combo.grid(row=4, column=1, padx=5, pady=5, sticky="w")
all_entries.append(user_agent_combo)
all_vars.append(user_agent_var)

"""Referer"""
ttk.Label(basic_frame, text="Referer:").grid(row=5, column=0, padx=5, pady=5, sticky="e") # 创建"Referer"标签
referer_entry = ttk.Entry(basic_frame, width=60) # 创建Referer输入框
referer_entry.grid(row=5, column=1, columnspan=3, padx=5, pady=5, sticky="we")
all_entries.append(referer_entry)

"""代理"""
ttk.Label(basic_frame, text="代理:").grid(row=6, column=0, padx=5, pady=5, sticky="e")# 创建"代理"标签
proxy_entry = ttk.Entry(basic_frame, width=60)# 创建代理输入框
proxy_entry.grid(row=6, column=1, columnspan=3, padx=5, pady=5, sticky="we")
all_entries.append(proxy_entry)

# ====================== 注入设置选项卡 ======================

"""风险等级"""
ttk.Label(injection_frame, text="风险等级 (1-3):").grid(row=0, column=0, padx=5, pady=5, sticky="e")# 创建"风险等级"标签
risk_var = tk.StringVar(value="1")# 创建风险等级变量，默认值"1"
risk_combo = ttk.Combobox(injection_frame, textvariable=risk_var, width=5)# 创建风险等级下拉框
risk_combo['values'] = ("1", "2", "3")# 设置下拉框选项值
risk_combo.grid(row=0, column=1, padx=5, pady=5, sticky="w")
all_entries.append(risk_combo)
all_vars.append(risk_var)
default_vars.append(risk_var)# 将风险变量添加到默认变量列表（用于重置时恢复默认值）

"""测试等级"""
ttk.Label(injection_frame, text="测试等级 (1-5):").grid(row=0, column=2, padx=5, pady=5, sticky="e")# 创建"测试等级"标签
level_var = tk.StringVar(value="1")# 创建测试等级变量，默认值"1"
level_combo = ttk.Combobox(injection_frame, textvariable=level_var, width=5)
level_combo['values'] = ("1", "2", "3", "4", "5")
level_combo.grid(row=0, column=3, padx=5, pady=5, sticky="w")
all_entries.append(level_combo)
all_vars.append(level_var)
default_vars.append(level_var)

"""数据库类型"""
ttk.Label(injection_frame, text="数据库类型:").grid(row=1, column=0, padx=5, pady=5, sticky="e")# 创建"数据库类型"标签
dbms_var = tk.StringVar(value="auto")# 创建数据库类型变量，默认值"auto"
dbms_combo = ttk.Combobox(injection_frame, textvariable=dbms_var, width=15)
dbms_combo['values'] = ("auto", "mysql", "oracle", "postgresql", "mssql", "sqlite")
dbms_combo.grid(row=1, column=1, padx=5, pady=5, sticky="w")
all_entries.append(dbms_combo)
all_vars.append(dbms_var)

"""注入技术"""
ttk.Label(injection_frame, text="注入技术:").grid(row=1, column=2, padx=5, pady=5, sticky="e")# 创建"注入技术"标签
technique_var = tk.StringVar(value="BEUSTQ (全部)")# 创建注入技术变量，默认值"BEUSTQ (全部)"
technique_combo = ttk.Combobox(injection_frame, textvariable=technique_var, width=15)
# 设置下拉框选项值（包含中文说明）
technique_combo['values'] = (
    "BEUSTQ (全部)",
    "B (布尔盲注)",
    "E (报错注入)",
    "U (联合查询)",
    "S (堆叠查询)",
    "T (时间盲注)",
    "Q (内联查询)"
)
technique_combo.grid(row=1, column=3, padx=5, pady=5, sticky="w")
all_entries.append(technique_combo)
all_vars.append(technique_var)

"""Tamper脚本"""
ttk.Label(injection_frame, text="Tamper脚本:").grid(row=2, column=0, padx=5, pady=5, sticky="e")# 创建"Tamper脚本"标签
tamper_entry = ttk.Entry(injection_frame, width=60)# 创建Tamper脚本输入框
tamper_entry.grid(row=2, column=1, columnspan=3, padx=5, pady=5, sticky="we")
all_entries.append(tamper_entry)

"""创建批处理模式"""
batch_var = tk.BooleanVar()  # 创建布尔变量
batch_check = ttk.Checkbutton(injection_frame, text="批处理模式（自动确认）", variable=batch_var)
batch_check.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="w")
all_vars.append(batch_var)

# ====================== 枚举设置选项卡 ======================

# 创建"爆破流程"标题（加粗）
ttk.Label(enum_frame, text="爆破流程:", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5, pady=5, sticky="w")

# 创建"获取数据库名称"复选框
enum_db_var = tk.BooleanVar()
enum_db_check = ttk.Checkbutton(enum_frame, text="1. 获取数据库名称", variable=enum_db_var)
enum_db_check.grid(row=1, column=0, padx=5, pady=5, sticky="w")
all_vars.append(enum_db_var)

# 创建"选择数据库"标签
ttk.Label(enum_frame, text="选择数据库:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
# 创建数据库选择输入框
select_db_entry = ttk.Entry(enum_frame, width=25)
select_db_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")
all_entries.append(select_db_entry)

# 创建"获取表名"复选框
enum_tables_var = tk.BooleanVar()
enum_tables_check = ttk.Checkbutton(enum_frame, text="2. 获取表名", variable=enum_tables_var)
enum_tables_check.grid(row=3, column=0, padx=5, pady=5, sticky="w")
all_vars.append(enum_tables_var)

# 创建"选择表"标签
ttk.Label(enum_frame, text="选择表:").grid(row=4, column=0, padx=5, pady=5, sticky="e")
# 创建表选择输入框
select_table_entry = ttk.Entry(enum_frame, width=25)
select_table_entry.grid(row=4, column=1, padx=5, pady=5, sticky="w")
all_entries.append(select_table_entry)

# 创建"获取列名"复选框
enum_columns_var = tk.BooleanVar()
enum_columns_check = ttk.Checkbutton(enum_frame, text="3. 获取列名", variable=enum_columns_var)
enum_columns_check.grid(row=5, column=0, padx=5, pady=5, sticky="w")
all_vars.append(enum_columns_var)

# 创建"高级选项"标题（加粗）
ttk.Label(enum_frame, text="高级选项:", font=("Arial", 10, "bold")).grid(row=0, column=2, padx=5, pady=5, sticky="w")

# 创建"枚举数据库结构"复选框
enum_schema_var = tk.BooleanVar()
enum_schema_check = ttk.Checkbutton(enum_frame, text="枚举数据库结构", variable=enum_schema_var)
enum_schema_check.grid(row=1, column=2, padx=5, pady=5, sticky="w")
all_vars.append(enum_schema_var)

# 创建"枚举所有内容"复选框
enum_all_var = tk.BooleanVar()
enum_all_check = ttk.Checkbutton(enum_frame, text="枚举所有内容", variable=enum_all_var)
enum_all_check.grid(row=2, column=2, padx=5, pady=5, sticky="w")
all_vars.append(enum_all_var)

# 创建"排除系统数据库"标签
ttk.Label(enum_frame, text="排除系统数据库:").grid(row=3, column=2, padx=5, pady=5, sticky="e")
# 创建排除数据库输入框
exclude_entry = ttk.Entry(enum_frame, width=25)
exclude_entry.grid(row=3, column=3, padx=5, pady=5, sticky="w")
all_entries.append(exclude_entry)

# 创建"转储表数据"复选框
dump_var = tk.BooleanVar()
dump_check = ttk.Checkbutton(enum_frame, text="转储表数据", variable=dump_var)
dump_check.grid(row=4, column=2, padx=5, pady=5, sticky="w")
all_vars.append(dump_var)

# 创建"转储所有数据"复选框
dump_all_var = tk.BooleanVar()
dump_all_check = ttk.Checkbutton(enum_frame, text="转储所有数据", variable=dump_all_var)
dump_all_check.grid(row=5, column=2, padx=5, pady=5, sticky="w")
all_vars.append(dump_all_var)

# 创建"WHERE条件"标签
ttk.Label(enum_frame, text="WHERE条件:").grid(row=6, column=2, padx=5, pady=5, sticky="e")
# 创建WHERE条件输入框
where_entry = ttk.Entry(enum_frame, width=25)
where_entry.grid(row=6, column=3, padx=5, pady=5, sticky="w")
all_entries.append(where_entry)

# 创建"起始行"标签
ttk.Label(enum_frame, text="起始行:").grid(row=7, column=2, padx=5, pady=5, sticky="e")
# 创建起始行变量，默认值"1"
start_var = tk.StringVar(value="1")
# 创建起始行输入框
start_entry = ttk.Entry(enum_frame, textvariable=start_var, width=5)
start_entry.grid(row=7, column=3, padx=5, pady=5, sticky="w")
all_entries.append(start_entry)
all_vars.append(start_var)
default_vars.append(start_var)  # 添加到默认变量列表

# 创建"结束行"标签
ttk.Label(enum_frame, text="结束行:").grid(row=8, column=2, padx=5, pady=5, sticky="e")
# 创建结束行变量，默认值"100"
stop_var = tk.StringVar(value="100")
# 创建结束行输入框
stop_entry = ttk.Entry(enum_frame, textvariable=stop_var, width=5)
stop_entry.grid(row=8, column=3, padx=5, pady=5, sticky="w")
all_entries.append(stop_entry)
all_vars.append(stop_var)
default_vars.append(stop_var)  # 添加到默认变量列表

# ====================== 性能设置选项卡 ======================

# 创建"线程数"标签
ttk.Label(performance_frame, text="线程数:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
# 创建线程数变量，默认值"1"
threads_var = tk.StringVar(value="1")
# 创建线程数下拉框
threads_combo = ttk.Combobox(performance_frame, textvariable=threads_var, width=5)
threads_combo['values'] = ("1", "2", "4", "8", "16")
threads_combo.grid(row=0, column=1, padx=5, pady=5, sticky="w")
all_entries.append(threads_combo)
all_vars.append(threads_var)

# 创建"请求延迟"标签
ttk.Label(performance_frame, text="请求延迟(秒):").grid(row=1, column=0, padx=5, pady=5, sticky="e")
# 创建请求延迟变量，默认值"0"
delay_var = tk.StringVar(value="0")
delay_combo = ttk.Combobox(performance_frame, textvariable=delay_var, width=5)
delay_combo['values'] = ("0", "0.5", "1", "2", "5")
delay_combo.grid(row=1, column=1, padx=5, pady=5, sticky="w")
all_entries.append(delay_combo)
all_vars.append(delay_var)

# 创建"超时时间"标签
ttk.Label(performance_frame, text="超时时间(秒):").grid(row=2, column=0, padx=5, pady=5, sticky="e")
# 创建超时时间变量，默认值"30"
timeout_var = tk.StringVar(value="30")
timeout_combo = ttk.Combobox(performance_frame, textvariable=timeout_var, width=5)
timeout_combo['values'] = ("10", "30", "60", "120")
timeout_combo.grid(row=2, column=1, padx=5, pady=5, sticky="w")
all_entries.append(timeout_combo)
all_vars.append(timeout_var)

# 创建"重试次数"标签
ttk.Label(performance_frame, text="重试次数:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
# 创建重试次数变量，默认值"3"
retries_var = tk.StringVar(value="3")
retries_combo = ttk.Combobox(performance_frame, textvariable=retries_var, width=5)
retries_combo['values'] = ("1", "2", "3", "5")
retries_combo.grid(row=3, column=1, padx=5, pady=5, sticky="w")
all_entries.append(retries_combo)
all_vars.append(retries_var)

# ====================== 输入输出设置选项卡 ======================
# 创建"SQLMap路径"标签
ttk.Label(output_frame, text="SQLMap路径:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
# 创建SQLMap路径输入框，设置默认值
sqlmap_path_entry = ttk.Entry(output_frame, width=60)
sqlmap_path_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

# 设置默认路径（你可以修改这个默认值）。硬编码的，自己改路径啊
sqlmap_path_entry.insert(0, "D:\\tools\\SQLMap\\sqlmap.py")

# 创建"输出目录"标签
ttk.Label(output_frame, text="输出目录:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
# 创建输出目录输入框
output_entry = ttk.Entry(output_frame, width=60)
output_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")
all_entries.append(output_entry)

# ====================== 爆破结果区域 ======================

# 创建爆破结果框架（带标题）
results_frame = ttk.LabelFrame(root, text="爆破结果")
# 将框架放置在主窗口中，水平填充，左右填充10像素，上下填充5像素
results_frame.pack(fill='x', padx=10, pady=5)

# 创建"数据库名称"标签
db_name_label = ttk.Label(results_frame, text="数据库名称")
# 将标签放置在结果框架的第0行第0列
db_name_label.grid(row=0, column=0, padx=5, pady=5)
# 创建数据库名称显示文本框（带滚动条），高度6行，宽度25字符
db_name_text = scrolledtext.ScrolledText(results_frame, height=6, width=25)
db_name_text.grid(row=1, column=0, padx=5, pady=5)

# 创建"表名"标签
table_name_label = ttk.Label(results_frame, text="表名")
table_name_label.grid(row=0, column=1, padx=5, pady=5)
# 创建表名显示文本框
table_name_text = scrolledtext.ScrolledText(results_frame, height=6, width=25)
table_name_text.grid(row=1, column=1, padx=5, pady=5)

# 创建"数据列"标签
columns_label = ttk.Label(results_frame, text="数据列")
columns_label.grid(row=0, column=2, padx=5, pady=5)
# 创建数据列显示文本框
columns_text = scrolledtext.ScrolledText(results_frame, height=6, width=25)
columns_text.grid(row=1, column=2, padx=5, pady=5)

# ====================== 命令显示区域 ======================

# 创建命令框架（带标题）
command_frame = ttk.LabelFrame(root, text="SQLMap命令")
command_frame.pack(fill='x', padx=10, pady=5)

# 创建命令显示文本框（带滚动条），高度5行，宽度100字符
command_text = scrolledtext.ScrolledText(command_frame, height=5, width=100)
command_text.pack(fill='both', expand=True, padx=5, pady=5)

# ====================== 按钮区域 ======================

# 创建按钮框架
button_frame = ttk.Frame(root)
button_frame.pack(fill='x', padx=10, pady=10)

# 创建"生成命令"按钮，点击时调用generate_sqlmap_command函数
generate_btn = ttk.Button(button_frame, text="生成命令", command=generate_sqlmap_command)
generate_btn.pack(side='left', padx=5)  # 靠左放置，左右填充5像素

# 创建"清除字段"按钮，点击时调用clear_fields函数
clear_btn = ttk.Button(button_frame, text="清除字段", command=clear_fields)
clear_btn.pack(side='left', padx=5)

# 创建"清除SQLMap缓存"按钮，点击时调用clear_sqlmap函数
purge_btn = ttk.Button(button_frame, text="清除SQLMap缓存", command=clear_sqlmap)
purge_btn.pack(side='left', padx=5)

# 创建"调用SQLMap启动"按钮，点击时调用sqlmap_path函数
purge_btn = ttk.Button(button_frame, text="调用SQLMap启动",command=sqlmap_path)
purge_btn.pack(side='left', padx=5)

# 创建"退出"按钮，点击时关闭主窗口
exit_btn = ttk.Button(button_frame, text="退出", command=root.destroy)
exit_btn.pack(side='right', padx=5)  # 靠右放置

# 启动主事件循环，显示GUI界面
root.mainloop()

#我想把我这个脚本给SQL map官方邮箱发一份，询问这个能不能作为官方半图形化界面使用。
#所以请你把我这个脚本先全面用英语给他写出来一份。然后。帮我写一封言辞恳切的邮箱信询问一下。


