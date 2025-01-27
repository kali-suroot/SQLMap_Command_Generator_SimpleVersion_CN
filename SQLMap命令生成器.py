import tkinter as tk

def generate_sqlmap_command():
    # 获取用户输入的参数
    url = url_entry.get()
    db_name = db_name_text.get("1.0", tk.END).strip()  # 获取数据库名称输入框的内容
    risk = risk_var.get()
    level = level_var.get()
    output = output_entry.get()
    risk_checked = risk_checkbox_var.get()
    level_checked = level_checkbox_var.get()
    batch_checked = batch_var.get()  # 获取批处理 复选框的状态
    current_db_checked = current_db_var.get()  # 获取数据库名 的状态
    select_db = select_db_entry.get().strip()  # 选择数据库 输入框的内容
    get_tables_checked = get_tables_checkbox_var.get()  # 获取表名 复选框的状态
    select_table = select_table_entry.get().strip()  # 选择表 输入框的内容
    get_columns_checked = get_columns_checkbox_var.get()  # 获取列名 复选框的状态

    # 构建基本的 sqlmap 命令
    command = f"python sqlmap.py -u {url}"

    # 根据复选框状态添加风险、等级和批处理参数
    if level_checked:
        command += f" --level={level}"
    if risk_checked:
        command += f" --risk={risk}"
    if batch_checked:
        command += " -batch"
    if current_db_checked:
        command += " --dbs"  # 添加显示数据库参数
    if get_tables_checked:
        command += f" -D {select_db} --tables"  # 添加获取表名参数
    if get_columns_checked:
        command += f" -D {select_db} -T {select_table} --columns"  # 添加获取列名参数

    # 如果用户输入了输出文件路径，则添加到命令中
    if output:
        command += f" --output-dir={output}"

    # 显示生成的命令在文本框中
    command_text.delete(1.0, tk.END)  # 清空文本框
    command_text.insert(tk.END, command)  # 插入生成的命令

def clear_sqlmap():
    # 显示清除命令
    command_text.delete(1.0, tk.END)  # 清空文本框
    command_text.insert(tk.END, "python sqlmap.py --purge")  # 插入清除命令

# 创建主窗口
root = tk.Tk()
root.title("SQLMap命令生成器    by:kali-suroot")

# 创建左侧输入框和标签
db_name_label = tk.Label(root, text="数据库名称")
db_name_label.grid(row=0, column=0, padx=10, pady=10)
db_name_text = tk.Text(root, width=30, height=20)
db_name_text.grid(row=1, column=0,rowspan=6, padx=10, pady=10)

# 创建右侧输入框和标签
table_name_label = tk.Label(root, text="表名")
table_name_label.grid(row=0, column=4, padx=10, pady=10)
table_name_text = tk.Text(root, width=50, height=20)
table_name_text.grid(row=1, column=4,rowspan=6, padx=10, pady=10)

# 创建输入框和标签
tk.Label(root, text="URL:").grid(row=0, column=1)
url_entry = tk.Entry(root)
url_entry.grid(row=0, column=2)

tk.Label(root, text="风险 (1-3):").grid(row=1, column=1)
risk_var = tk.IntVar(value=1)
risk_entry = tk.Spinbox(root, from_=1, to=3, textvariable=risk_var)
risk_entry.grid(row=1, column=2)
risk_checkbox_var = tk.BooleanVar()
risk_checkbox = tk.Checkbutton(root, text="包含风险参数", variable=risk_checkbox_var)
risk_checkbox.grid(row=1, column=3)

tk.Label(root, text="等级 (1-5):").grid(row=2, column=1)
level_var = tk.IntVar(value=1)
level_entry = tk.Spinbox(root, from_=1, to=5, textvariable=level_var)
level_entry.grid(row=2, column=2)
level_checkbox_var = tk.BooleanVar()
level_checkbox = tk.Checkbutton(root, text="包含等级参数", variable=level_checkbox_var)
level_checkbox.grid(row=2, column=3)

tk.Label(root, text="Output File (optional):").grid(row=3, column=1)
output_entry = tk.Entry(root)
output_entry.grid(row=3, column=2)

# 创建批处理复选框
batch_var = tk.BooleanVar()
batch_checkbox = tk.Checkbutton(root, text="批处理（自动爆破）", variable=batch_var)
batch_checkbox.grid(row=4, column=1, sticky="w")

# 创建显示数据库复选框
current_db_var = tk.BooleanVar()
current_db_checkbox = tk.Checkbutton(root, text="获取数据库名", variable=current_db_var)
current_db_checkbox.grid(row=4, column=2, sticky="w")

# 创建选择数据库输入框
tk.Label(root, text="选择数据库:").grid(row=5, column=1)
select_db_entry = tk.Entry(root)
select_db_entry.grid(row=5, column=2)

# 创建获取表名复选框
get_tables_checkbox_var = tk.BooleanVar()
get_tables_checkbox = tk.Checkbutton(root, text="获取表名", variable=get_tables_checkbox_var)
get_tables_checkbox.grid(row=5, column=3, sticky="w")

# 创建"选择表:" 输入框
tk.Label(root, text="选择表:").grid(row=6, column=1)
select_table_entry = tk.Entry(root)
select_table_entry.grid(row=6, column=2)

# 创建"获取列名"复选框
get_columns_checkbox_var = tk.BooleanVar()
get_columns_checkbox = tk.Checkbutton(root, text="获取列名", variable=get_columns_checkbox_var)
get_columns_checkbox.grid(row=6, column=3, sticky="w")

# 创建文本框显示命令
command_text = tk.Text(root, height=5, width=50)
command_text.grid(row=8, column=1, columnspan=3, padx=10, pady=10)

# 创建按钮
generate_button = tk.Button(root, text="生成命令", command=generate_sqlmap_command)
generate_button.grid(row=9, column=1, padx=10, pady=10)

clear_button = tk.Button(root, text="清除 Sqlmap", command=clear_sqlmap)
clear_button.grid(row=9, column=2, padx=10, pady=10)

# 运行主循环
root.mainloop()