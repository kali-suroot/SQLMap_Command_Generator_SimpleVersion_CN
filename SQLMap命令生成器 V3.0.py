import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox

def generate_sqlmap_command():
    try:
        # 获取基本参数
        url = url_entry.get().strip()
        if not url:
            messagebox.showerror("错误", "URL不能为空！")
            return
            
        method = method_var.get()
        data = data_entry.get().strip()
        cookie = cookie_entry.get().strip()
        user_agent = user_agent_var.get()
        referer = referer_entry.get().strip()
        proxy = proxy_entry.get().strip()
        threads = threads_var.get()
        delay = delay_var.get()
        timeout = timeout_var.get()
        retries = retries_var.get()
        risk = risk_var.get()
        level = level_var.get()
        dbms = dbms_var.get()
        technique = technique_var.get().split(' ')[0]  # 提取技术代码
        tamper = tamper_entry.get().strip()
        batch = batch_var.get()
        output = output_entry.get().strip()
        
        # 获取枚举参数
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
        
        # 构建基本命令
        command = "python sqlmap.py"
        
        # 目标设置
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
        
        # 枚举设置
        if enum_db:
            command += " --dbs"  # 获取数据库名称
            
        if enum_tables and select_db:
            command += f" -D {select_db} --tables"  # 获取表名
            
        if enum_columns and select_db and select_table:
            command += f" -D {select_db} -T {select_table} --columns"  # 获取列名
            
        if enum_schema:
            command += " --schema"
            
        if enum_all:
            command += " --all"
            
        if exclude_db:
            command += f" --exclude-sysdbs={exclude_db}"
            
        if dump and select_db and select_table:
            command += f" -D {select_db} -T {select_table} --dump"
            
        if dump_all:
            command += " --dump-all"
            
        if where:
            command += f" --where=\"{where}\""
            
        if start != "1":
            command += f" --start={start}"
            
        if stop != "100":
            command += f" --stop={stop}"
        
        # 输出设置
        if output:
            command += f" --output-dir={output}"
        
        # 显示生成的命令
        command_text.delete(1.0, tk.END)
        command_text.insert(tk.END, command)
        
    except Exception as e:
        messagebox.showerror("生成错误", f"生成命令时出错: {str(e)}")

def clear_fields():
    for entry in all_entries:
        if isinstance(entry, tk.Entry) or isinstance(entry, ttk.Entry):
            entry.delete(0, tk.END)
        elif isinstance(entry, ttk.Combobox):
            entry.set(entry['values'][0])
        elif isinstance(entry, tk.Text):
            entry.delete(1.0, tk.END)
    
    for var in all_vars:
        if isinstance(var, tk.BooleanVar):
            var.set(False)
        elif isinstance(var, tk.StringVar) and var not in default_vars:
            var.set("1")
    
    # 重置特殊控件
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
    
    # 清除爆破结果
    db_name_text.delete(1.0, tk.END)
    table_name_text.delete(1.0, tk.END)
    columns_text.delete(1.0, tk.END)

def clear_sqlmap():
    command_text.delete(1.0, tk.END)
    command_text.insert(tk.END, "python sqlmap.py --purge")

# 创建主窗口
root = tk.Tk()
root.title("SQLMap命令生成器 v3.0 by:kali-suroot")
root.geometry("670x670")  # 更紧凑的尺寸

# 创建Notebook（选项卡）
notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True, padx=10, pady=10)

# 创建选项卡框架
basic_frame = ttk.Frame(notebook)
injection_frame = ttk.Frame(notebook)
enum_frame = ttk.Frame(notebook)
performance_frame = ttk.Frame(notebook)
output_frame = ttk.Frame(notebook)

notebook.add(basic_frame, text="基本设置")
notebook.add(injection_frame, text="注入设置")
notebook.add(enum_frame, text="枚举设置")
notebook.add(performance_frame, text="性能设置")
notebook.add(output_frame, text="输出设置")

# 存储所有输入控件
all_entries = []
all_vars = []
default_vars = []

# 基本设置选项卡 - 使用网格布局
ttk.Label(basic_frame, text="目标URL (必填):").grid(row=0, column=0, padx=5, pady=5, sticky="e")
url_entry = ttk.Entry(basic_frame, width=60)
url_entry.grid(row=0, column=1, columnspan=3, padx=5, pady=5, sticky="we")
all_entries.append(url_entry)

ttk.Label(basic_frame, text="请求方法:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
method_var = tk.StringVar(value="GET")
method_combo = ttk.Combobox(basic_frame, textvariable=method_var, width=15)
method_combo['values'] = ("GET", "POST", "PUT", "HEAD")
method_combo.grid(row=1, column=1, padx=5, pady=5, sticky="w")
all_entries.append(method_combo)
all_vars.append(method_var)

ttk.Label(basic_frame, text="POST数据:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
data_entry = ttk.Entry(basic_frame, width=60)
data_entry.grid(row=2, column=1, columnspan=3, padx=5, pady=5, sticky="we")
all_entries.append(data_entry)

ttk.Label(basic_frame, text="Cookie:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
cookie_entry = ttk.Entry(basic_frame, width=60)
cookie_entry.grid(row=3, column=1, columnspan=3, padx=5, pady=5, sticky="we")
all_entries.append(cookie_entry)

ttk.Label(basic_frame, text="User-Agent:").grid(row=4, column=0, padx=5, pady=5, sticky="e")
user_agent_var = tk.StringVar(value="default")
user_agent_combo = ttk.Combobox(basic_frame, textvariable=user_agent_var, width=20)
user_agent_combo['values'] = ("default", "random", "Mozilla/5.0", "Googlebot/2.1")
user_agent_combo.grid(row=4, column=1, padx=5, pady=5, sticky="w")
all_entries.append(user_agent_combo)
all_vars.append(user_agent_var)

ttk.Label(basic_frame, text="Referer:").grid(row=5, column=0, padx=5, pady=5, sticky="e")
referer_entry = ttk.Entry(basic_frame, width=60)
referer_entry.grid(row=5, column=1, columnspan=3, padx=5, pady=5, sticky="we")
all_entries.append(referer_entry)

ttk.Label(basic_frame, text="代理:").grid(row=6, column=0, padx=5, pady=5, sticky="e")
proxy_entry = ttk.Entry(basic_frame, width=60)
proxy_entry.grid(row=6, column=1, columnspan=3, padx=5, pady=5, sticky="we")
all_entries.append(proxy_entry)

# 注入设置选项卡
ttk.Label(injection_frame, text="风险等级 (1-3):").grid(row=0, column=0, padx=5, pady=5, sticky="e")
risk_var = tk.StringVar(value="1")
risk_combo = ttk.Combobox(injection_frame, textvariable=risk_var, width=5)
risk_combo['values'] = ("1", "2", "3")
risk_combo.grid(row=0, column=1, padx=5, pady=5, sticky="w")
all_entries.append(risk_combo)
all_vars.append(risk_var)
default_vars.append(risk_var)

ttk.Label(injection_frame, text="测试等级 (1-5):").grid(row=0, column=2, padx=5, pady=5, sticky="e")
level_var = tk.StringVar(value="1")
level_combo = ttk.Combobox(injection_frame, textvariable=level_var, width=5)
level_combo['values'] = ("1", "2", "3", "4", "5")
level_combo.grid(row=0, column=3, padx=5, pady=5, sticky="w")
all_entries.append(level_combo)
all_vars.append(level_var)
default_vars.append(level_var)

ttk.Label(injection_frame, text="数据库类型:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
dbms_var = tk.StringVar(value="auto")
dbms_combo = ttk.Combobox(injection_frame, textvariable=dbms_var, width=15)
dbms_combo['values'] = ("auto", "mysql", "oracle", "postgresql", "mssql", "sqlite")
dbms_combo.grid(row=1, column=1, padx=5, pady=5, sticky="w")
all_entries.append(dbms_combo)
all_vars.append(dbms_var)

# 修改注入技术选项，添加中文说明
ttk.Label(injection_frame, text="注入技术:").grid(row=1, column=2, padx=5, pady=5, sticky="e")
technique_var = tk.StringVar(value="BEUSTQ (全部)")
technique_combo = ttk.Combobox(injection_frame, textvariable=technique_var, width=15)
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

ttk.Label(injection_frame, text="Tamper脚本:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
tamper_entry = ttk.Entry(injection_frame, width=60)
tamper_entry.grid(row=2, column=1, columnspan=3, padx=5, pady=5, sticky="we")
all_entries.append(tamper_entry)

batch_var = tk.BooleanVar()
batch_check = ttk.Checkbutton(injection_frame, text="批处理模式（自动确认）", variable=batch_var)
batch_check.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="w")
all_vars.append(batch_var)

# 枚举设置选项卡 - 优化布局
# 左侧：爆破流程
ttk.Label(enum_frame, text="爆破流程:", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5, pady=5, sticky="w")

enum_db_var = tk.BooleanVar()
enum_db_check = ttk.Checkbutton(enum_frame, text="1. 获取数据库名称", variable=enum_db_var)
enum_db_check.grid(row=1, column=0, padx=5, pady=5, sticky="w")
all_vars.append(enum_db_var)

ttk.Label(enum_frame, text="选择数据库:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
select_db_entry = ttk.Entry(enum_frame, width=25)
select_db_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")
all_entries.append(select_db_entry)

enum_tables_var = tk.BooleanVar()
enum_tables_check = ttk.Checkbutton(enum_frame, text="2. 获取表名", variable=enum_tables_var)
enum_tables_check.grid(row=3, column=0, padx=5, pady=5, sticky="w")
all_vars.append(enum_tables_var)

ttk.Label(enum_frame, text="选择表:").grid(row=4, column=0, padx=5, pady=5, sticky="e")
select_table_entry = ttk.Entry(enum_frame, width=25)
select_table_entry.grid(row=4, column=1, padx=5, pady=5, sticky="w")
all_entries.append(select_table_entry)

enum_columns_var = tk.BooleanVar()
enum_columns_check = ttk.Checkbutton(enum_frame, text="3. 获取列名", variable=enum_columns_var)
enum_columns_check.grid(row=5, column=0, padx=5, pady=5, sticky="w")
all_vars.append(enum_columns_var)

# 右侧：高级选项
ttk.Label(enum_frame, text="高级选项:", font=("Arial", 10, "bold")).grid(row=0, column=2, padx=5, pady=5, sticky="w")

enum_schema_var = tk.BooleanVar()
enum_schema_check = ttk.Checkbutton(enum_frame, text="枚举数据库结构", variable=enum_schema_var)
enum_schema_check.grid(row=1, column=2, padx=5, pady=5, sticky="w")
all_vars.append(enum_schema_var)

enum_all_var = tk.BooleanVar()
enum_all_check = ttk.Checkbutton(enum_frame, text="枚举所有内容", variable=enum_all_var)
enum_all_check.grid(row=2, column=2, padx=5, pady=5, sticky="w")
all_vars.append(enum_all_var)

ttk.Label(enum_frame, text="排除系统数据库:").grid(row=3, column=2, padx=5, pady=5, sticky="e")
exclude_entry = ttk.Entry(enum_frame, width=25)
exclude_entry.grid(row=3, column=3, padx=5, pady=5, sticky="w")
all_entries.append(exclude_entry)

dump_var = tk.BooleanVar()
dump_check = ttk.Checkbutton(enum_frame, text="转储表数据", variable=dump_var)
dump_check.grid(row=4, column=2, padx=5, pady=5, sticky="w")
all_vars.append(dump_var)


# by:kali-suroot

dump_all_var = tk.BooleanVar()
dump_all_check = ttk.Checkbutton(enum_frame, text="转储所有数据", variable=dump_all_var)
dump_all_check.grid(row=5, column=2, padx=5, pady=5, sticky="w")
all_vars.append(dump_all_var)

ttk.Label(enum_frame, text="WHERE条件:").grid(row=6, column=2, padx=5, pady=5, sticky="e")
where_entry = ttk.Entry(enum_frame, width=25)
where_entry.grid(row=6, column=3, padx=5, pady=5, sticky="w")
all_entries.append(where_entry)

ttk.Label(enum_frame, text="起始行:").grid(row=7, column=2, padx=5, pady=5, sticky="e")
start_var = tk.StringVar(value="1")
start_entry = ttk.Entry(enum_frame, textvariable=start_var, width=5)
start_entry.grid(row=7, column=3, padx=5, pady=5, sticky="w")
all_entries.append(start_entry)
all_vars.append(start_var)
default_vars.append(start_var)

ttk.Label(enum_frame, text="结束行:").grid(row=8, column=2, padx=5, pady=5, sticky="e")
stop_var = tk.StringVar(value="100")
stop_entry = ttk.Entry(enum_frame, textvariable=stop_var, width=5)
stop_entry.grid(row=8, column=3, padx=5, pady=5, sticky="w")
all_entries.append(stop_entry)
all_vars.append(stop_var)
default_vars.append(stop_var)

# 性能设置选项卡
ttk.Label(performance_frame, text="线程数:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
threads_var = tk.StringVar(value="1")
threads_combo = ttk.Combobox(performance_frame, textvariable=threads_var, width=5)
threads_combo['values'] = ("1", "2", "4", "8", "16")
threads_combo.grid(row=0, column=1, padx=5, pady=5, sticky="w")
all_entries.append(threads_combo)
all_vars.append(threads_var)

ttk.Label(performance_frame, text="请求延迟(秒):").grid(row=1, column=0, padx=5, pady=5, sticky="e")
delay_var = tk.StringVar(value="0")
delay_combo = ttk.Combobox(performance_frame, textvariable=delay_var, width=5)
delay_combo['values'] = ("0", "0.5", "1", "2", "5")
delay_combo.grid(row=1, column=1, padx=5, pady=5, sticky="w")
all_entries.append(delay_combo)
all_vars.append(delay_var)

ttk.Label(performance_frame, text="超时时间(秒):").grid(row=2, column=0, padx=5, pady=5, sticky="e")
timeout_var = tk.StringVar(value="30")
timeout_combo = ttk.Combobox(performance_frame, textvariable=timeout_var, width=5)
timeout_combo['values'] = ("10", "30", "60", "120")
timeout_combo.grid(row=2, column=1, padx=5, pady=5, sticky="w")
all_entries.append(timeout_combo)
all_vars.append(timeout_var)

ttk.Label(performance_frame, text="重试次数:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
retries_var = tk.StringVar(value="3")
retries_combo = ttk.Combobox(performance_frame, textvariable=retries_var, width=5)
retries_combo['values'] = ("1", "2", "3", "5")
retries_combo.grid(row=3, column=1, padx=5, pady=5, sticky="w")
all_entries.append(retries_combo)
all_vars.append(retries_var)

# 输出设置选项卡
ttk.Label(output_frame, text="输出目录:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
output_entry = ttk.Entry(output_frame, width=60)
output_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
all_entries.append(output_entry)

# 爆破结果区域（永久显示在所有标签页下方）
results_frame = ttk.LabelFrame(root, text="爆破结果")
results_frame.pack(fill='x', padx=10, pady=5)

# 使用网格布局使三个文本框并排显示
db_name_label = ttk.Label(results_frame, text="数据库名称")
db_name_label.grid(row=0, column=0, padx=5, pady=5)
db_name_text = scrolledtext.ScrolledText(results_frame, height=6, width=25)
db_name_text.grid(row=1, column=0, padx=5, pady=5)

table_name_label = ttk.Label(results_frame, text="表名")
table_name_label.grid(row=0, column=1, padx=5, pady=5)
table_name_text = scrolledtext.ScrolledText(results_frame, height=6, width=25)
table_name_text.grid(row=1, column=1, padx=5, pady=5)

columns_label = ttk.Label(results_frame, text="数据列")
columns_label.grid(row=0, column=2, padx=5, pady=5)
columns_text = scrolledtext.ScrolledText(results_frame, height=6, width=25)
columns_text.grid(row=1, column=2, padx=5, pady=5)

# 命令生成区域
command_frame = ttk.LabelFrame(root, text="SQLMap命令")
command_frame.pack(fill='x', padx=10, pady=5)

command_text = scrolledtext.ScrolledText(command_frame, height=5, width=100)
command_text.pack(fill='both', expand=True, padx=5, pady=5)

# 按钮区域
button_frame = ttk.Frame(root)
button_frame.pack(fill='x', padx=10, pady=10)

generate_btn = ttk.Button(button_frame, text="生成命令", command=generate_sqlmap_command)
generate_btn.pack(side='left', padx=5)

clear_btn = ttk.Button(button_frame, text="清除字段", command=clear_fields)
clear_btn.pack(side='left', padx=5)

purge_btn = ttk.Button(button_frame, text="清除SQLMap缓存", command=clear_sqlmap)
purge_btn.pack(side='left', padx=5)

exit_btn = ttk.Button(button_frame, text="退出", command=root.destroy)
exit_btn.pack(side='right', padx=5)

# 运行主循环
root.mainloop()
