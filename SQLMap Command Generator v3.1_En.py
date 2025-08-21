import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import subprocess

def generate_sqlmap_command():
    """
    Core function to generate SQLMap command
    Gets various parameters from GUI interface and combines them into a complete SQLMap command
    """
    try:
        # Get SQLMap path
        sqlmap_path = sqlmap_path_entry.get().strip()
        if not sqlmap_path:
            messagebox.showerror("Error", "Please set SQLMap path first!")
            return
            
        # Get basic parameters
        url = url_entry.get().strip()
        if not url:
            messagebox.showerror("Error", "URL cannot be empty!")
            return
            
        # Get request-related parameters
        method = method_var.get()
        data = data_entry.get().strip()
        cookie = cookie_entry.get().strip()
        user_agent = user_agent_var.get()
        referer = referer_entry.get().strip()
        proxy = proxy_entry.get().strip()
        
        # Get performance-related parameters
        threads = threads_var.get()
        delay = delay_var.get()
        timeout = timeout_var.get()
        retries = retries_var.get()
        
        # Get injection-related parameters
        risk = risk_var.get()  # Risk level
        level = level_var.get()  # Test level
        dbms = dbms_var.get()  # Database
        technique = technique_var.get().split(' ')[0]  # Extract technique code (first character)
        tamper = tamper_entry.get().strip()
        batch = batch_var.get()
        
        # Get output parameters
        output = output_entry.get().strip()
        
        # Get enumeration-related parameters
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
        
        # Get brute force process parameters
        select_db = select_db_entry.get().strip()
        select_table = select_table_entry.get().strip()
        
        # Build basic command - use configured SQLMap path
        command = f"python \"{sqlmap_path}\""
        
        # Target settings (required)
        command += f" -u \"{url}\""

        # Request settings
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
        
        # Performance settings
        if threads != "1":
            command += f" --threads={threads}"
        if delay != "0":
            command += f" --delay={delay}"
        if timeout != "30":
            command += f" --timeout={timeout}"
        if retries != "3":
            command += f" --retries={retries}"
        
        # Injection settings
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
        
        # Enumeration settings (database brute force process)
        if enum_db:
            command += " --dbs"  # Get database names
            
        if enum_tables and select_db:
            command += f" -D {select_db} --tables"  # Get table names
            
        if enum_columns and select_db and select_table:
            command += f" -D {select_db} -T {select_table} --columns"  # Get column names
            
        if enum_schema:
            command += " --schema"  # Enumerate database structure
            
        if enum_all:
            command += " --all"  # Enumerate all content
            
        if exclude_db:
            command += f" --exclude-sysdbs={exclude_db}"  # Exclude system databases
            
        if dump and select_db and select_table:
            command += f" -D {select_db} -T {select_table} --dump"  # Dump table data
            
        if dump_all:
            command += " --dump-all"  # Dump all data
            
        if where:
            command += f" --where=\"{where}\""  # WHERE condition restriction
            
        if start != "1":
            command += f" --start={start}"  # Start row
            
        if stop != "100":
            command += f" --stop={stop}"  # End row
        
        # Output settings
        if output:
            command += f" --output-dir={output}"  # Output directory
        
        # Display generated command in text box
        command_text.delete(1.0, tk.END)
        command_text.insert(tk.END, command)
        
    except Exception as e:
        messagebox.showerror("Generation Error", f"Error generating command: {str(e)}")

def clear_fields():
    """
    Function to clear all input fields
    Reset interface to initial state
    """
    # Save SQLMap path
    saved_sqlmap_path = sqlmap_path_entry.get()
    
    # Clear all input fields
    for entry in all_entries:
        if isinstance(entry, tk.Entry) or isinstance(entry, ttk.Entry):
            entry.delete(0, tk.END)
        elif isinstance(entry, ttk.Combobox):
            entry.set(entry['values'][0])
        elif isinstance(entry, tk.Text):
            entry.delete(1.0, tk.END)
    
    # Reset all variables
    for var in all_vars:
        if isinstance(var, tk.BooleanVar):
            var.set(False)
        elif isinstance(var, tk.StringVar) and var not in default_vars:
            var.set("1")
    
    # Reset special controls to default values
    method_var.set("GET")
    user_agent_var.set("default")
    dbms_var.set("auto")
    technique_var.set("BEUSTQ (All)")
    threads_var.set("1")
    delay_var.set("0")
    timeout_var.set("30")
    retries_var.set("3")
    risk_var.set("1")
    level_var.set("1")
    start_var.set("1")
    stop_var.set("100")
    command_text.delete(1.0, tk.END)
    
    # Restore SQLMap path
    sqlmap_path_entry.delete(0, tk.END)
    sqlmap_path_entry.insert(0, saved_sqlmap_path)
    
    # Clear brute force result area
    db_name_text.delete(1.0, tk.END)
    table_name_text.delete(1.0, tk.END)
    columns_text.delete(1.0, tk.END)

def clear_sqlmap():
    """
    Generate SQLMap cache clearing command (does not execute)
    """
    try:
        sqlmap_path = sqlmap_path_entry.get().strip()
        if not sqlmap_path:
            messagebox.showerror("Error", "Please set SQLMap path first!")
            return
            
        command = f"python \"{sqlmap_path}\" --purge"
        
        # Only display command, do not execute
        command_text.delete(1.0, tk.END)
        command_text.insert(tk.END, command)
        
    except Exception as e:
        messagebox.showerror("Execution Error", f"Error generating cache clearing command: {str(e)}")

def execute_sqlmap():
    """
    Execute the command displayed in the command box
    """
    try:
        # Get command from command box
        command = command_text.get(1.0, tk.END).strip()
        if not command:
            messagebox.showerror("Error", "No command in command box!")
            return
            
        # Execute command directly in new window, no prompt
        subprocess.Popen(f'start cmd /k "{command}"', shell=True)
        
    except Exception as e:
        messagebox.showerror("Execution Error", f"Error executing command: {str(e)}")

# Create main window
root = tk.Tk()
root.title("SQLMap Command Generator v3.1_En by:kali-suroot")
root.geometry("670x670")  # Set window size

# Create Notebook (tab container)
notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True, padx=10, pady=10)

# Create tab frames
basic_frame = ttk.Frame(notebook)        # Basic settings
injection_frame = ttk.Frame(notebook)    # Injection settings
enum_frame = ttk.Frame(notebook)         # Enumeration settings
performance_frame = ttk.Frame(notebook)  # Performance settings
output_frame = ttk.Frame(notebook)       # Input/Output settings

# Add tabs to Notebook
notebook.add(basic_frame, text="Basic Settings")
notebook.add(injection_frame, text="Injection Settings")
notebook.add(enum_frame, text="Enumeration Settings")
notebook.add(performance_frame, text="Performance Settings")
notebook.add(output_frame, text="Input/Output Settings")

# Store all input controls list (for clear function)
all_entries = []
all_vars = []
default_vars = []

# ====================== Basic Settings Tab ======================

"""URL Input"""
ttk.Label(basic_frame, text="Target URL (Required):").grid(row=0, column=0, padx=5, pady=5, sticky="e") # Create "Target URL" label
url_entry = ttk.Entry(basic_frame, width=60)  # Create URL input field (width 60 characters)
url_entry.grid(row=0, column=1, columnspan=3, padx=5, pady=5, sticky="we") # Place URL input field at row 0, column 1, span 3 columns
all_entries.append(url_entry) # Add URL input field to all input controls list

"""Request Method"""
ttk.Label(basic_frame, text="Request Method:").grid(row=1, column=0, padx=5, pady=5, sticky="e") # Create "Request Method" label
method_var = tk.StringVar(value="GET") # Create request method variable, default "GET"
method_combo = ttk.Combobox(basic_frame, textvariable=method_var, width=15) # Create request method dropdown
method_combo['values'] = ("GET", "POST", "PUT", "HEAD") # Set dropdown options
method_combo.grid(row=1, column=1, padx=5, pady=5, sticky="w") # Place dropdown
all_entries.append(method_combo)  # Add dropdown to input controls list
all_vars.append(method_var)  # Add variable to variables list

"""POST Data"""
ttk.Label(basic_frame, text="POST Data:").grid(row=2, column=0, padx=5, pady=5, sticky="e") # Create "POST Data" label
data_entry = ttk.Entry(basic_frame, width=60) # Create POST data input field
data_entry.grid(row=2, column=1, columnspan=3, padx=5, pady=5, sticky="we") # Place input field
all_entries.append(data_entry)

"""Cookie"""
ttk.Label(basic_frame, text="Cookie:").grid(row=3, column=0, padx=5, pady=5, sticky="e") # Create "Cookie" label
cookie_entry = ttk.Entry(basic_frame, width=60) # Create Cookie input field
cookie_entry.grid(row=3, column=1, columnspan=3, padx=5, pady=5, sticky="we") # Place input field
all_entries.append(cookie_entry)

"""User-Agent"""
ttk.Label(basic_frame, text="User-Agent:").grid(row=4, column=0, padx=5, pady=5, sticky="e") # Create "User-Agent" label
user_agent_var = tk.StringVar(value="default") # Create User-Agent variable, default "default"
user_agent_combo = ttk.Combobox(basic_frame, textvariable=user_agent_var, width=20) # Create User-Agent dropdown
user_agent_combo['values'] = ("default", "random", "Mozilla/5.0", "Googlebot/2.1") # Set dropdown options
user_agent_combo.grid(row=4, column=1, padx=5, pady=5, sticky="w") # Place dropdown
all_entries.append(user_agent_combo)
all_vars.append(user_agent_var)

"""Referer"""
ttk.Label(basic_frame, text="Referer:").grid(row=5, column=0, padx=5, pady=5, sticky="e") # Create "Referer" label
referer_entry = ttk.Entry(basic_frame, width=60) # Create Referer input field
referer_entry.grid(row=5, column=1, columnspan=3, padx=5, pady=5, sticky="we") # Place input field
all_entries.append(referer_entry)

"""Proxy"""
ttk.Label(basic_frame, text="Proxy:").grid(row=6, column=0, padx=5, pady=5, sticky="e") # Create "Proxy" label
proxy_entry = ttk.Entry(basic_frame, width=60) # Create Proxy input field
proxy_entry.grid(row=6, column=1, columnspan=3, padx=5, pady=5, sticky="we") # Place input field
all_entries.append(proxy_entry)

# ====================== Injection Settings Tab ======================

"""Risk Level"""
ttk.Label(injection_frame, text="Risk Level (1-3):").grid(row=0, column=0, padx=5, pady=5, sticky="e") # Create "Risk Level" label
risk_var = tk.StringVar(value="1") # Create risk level variable, default "1"
risk_combo = ttk.Combobox(injection_frame, textvariable=risk_var, width=5) # Create risk level dropdown
risk_combo['values'] = ("1", "2", "3") # Set dropdown options
risk_combo.grid(row=0, column=1, padx=5, pady=5, sticky="w") # Place dropdown
all_entries.append(risk_combo)
all_vars.append(risk_var)
default_vars.append(risk_var) # Add to default variables list

"""Test Level"""
ttk.Label(injection_frame, text="Test Level (1-5):").grid(row=0, column=2, padx=5, pady=5, sticky="e") # Create "Test Level" label
level_var = tk.StringVar(value="1") # Create test level variable, default "1"
level_combo = ttk.Combobox(injection_frame, textvariable=level_var, width=5) # Create test level dropdown
level_combo['values'] = ("1", "2", "3", "4", "5") # Set dropdown options
level_combo.grid(row=0, column=3, padx=5, pady=5, sticky="w") # Place dropdown
all_entries.append(level_combo)
all_vars.append(level_var)
default_vars.append(level_var)

"""Database Type"""
ttk.Label(injection_frame, text="Database Type:").grid(row=1, column=0, padx=5, pady=5, sticky="e") # Create "Database Type" label
dbms_var = tk.StringVar(value="auto") # Create database type variable, default "auto"
dbms_combo = ttk.Combobox(injection_frame, textvariable=dbms_var, width=15) # Create database type dropdown
dbms_combo['values'] = ("auto", "mysql", "oracle", "postgresql", "mssql", "sqlite") # Set dropdown options
dbms_combo.grid(row=1, column=1, padx=5, pady=5, sticky="w") # Place dropdown
all_entries.append(dbms_combo)
all_vars.append(dbms_var)

"""Injection Technique"""
ttk.Label(injection_frame, text="Injection Technique:").grid(row=1, column=2, padx=5, pady=5, sticky="e") # Create "Injection Technique" label
technique_var = tk.StringVar(value="BEUSTQ (All)") # Create technique variable, default "BEUSTQ (All)"
technique_combo = ttk.Combobox(injection_frame, textvariable=technique_var, width=15) # Create technique dropdown
# Set dropdown options (with English descriptions)
technique_combo['values'] = (
    "BEUSTQ (All)",
    "B (Boolean-based blind)",
    "E (Error-based)",
    "U (Union query-based)",
    "S (Stacked queries)",
    "T (Time-based blind)",
    "Q (Inline queries)"
)
technique_combo.grid(row=1, column=3, padx=5, pady=5, sticky="w") # Place dropdown
all_entries.append(technique_combo)
all_vars.append(technique_var)

"""Tamper Script"""
ttk.Label(injection_frame, text="Tamper Script:").grid(row=2, column=0, padx=5, pady=5, sticky="e") # Create "Tamper Script" label
tamper_entry = ttk.Entry(injection_frame, width=60) # Create Tamper script input field
tamper_entry.grid(row=2, column=1, columnspan=3, padx=5, pady=5, sticky="we") # Place input field
all_entries.append(tamper_entry)

"""Batch Mode"""
batch_var = tk.BooleanVar()  # Create boolean variable
batch_check = ttk.Checkbutton(injection_frame, text="Batch Mode (Auto-confirm)", variable=batch_var) # Create batch mode checkbox
batch_check.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="w") # Place checkbox
all_vars.append(batch_var)

# ====================== Enumeration Settings Tab ======================

# Create "Brute Force Process" title (bold)
ttk.Label(enum_frame, text="Brute Force Process:", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5, pady=5, sticky="w")

# Create "Get Database Names" checkbox
enum_db_var = tk.BooleanVar()
enum_db_check = ttk.Checkbutton(enum_frame, text="1. Get Database Names", variable=enum_db_var)
enum_db_check.grid(row=1, column=0, padx=5, pady=5, sticky="w")
all_vars.append(enum_db_var)

# Create "Select Database" label
ttk.Label(enum_frame, text="Select Database:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
# Create database selection input field
select_db_entry = ttk.Entry(enum_frame, width=25)
select_db_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")
all_entries.append(select_db_entry)

# Create "Get Table Names" checkbox
enum_tables_var = tk.BooleanVar()
enum_tables_check = ttk.Checkbutton(enum_frame, text="2. Get Table Names", variable=enum_tables_var)
enum_tables_check.grid(row=3, column=0, padx=5, pady=5, sticky="w")
all_vars.append(enum_tables_var)

# Create "Select Table" label
ttk.Label(enum_frame, text="Select Table:").grid(row=4, column=0, padx=5, pady=5, sticky="e")
# Create table selection input field
select_table_entry = ttk.Entry(enum_frame, width=25)
select_table_entry.grid(row=4, column=1, padx=5, pady=5, sticky="w")
all_entries.append(select_table_entry)

# Create "Get Column Names" checkbox
enum_columns_var = tk.BooleanVar()
enum_columns_check = ttk.Checkbutton(enum_frame, text="3. Get Column Names", variable=enum_columns_var)
enum_columns_check.grid(row=5, column=0, padx=5, pady=5, sticky="w")
all_vars.append(enum_columns_var)

# Create "Advanced Options" title (bold)
ttk.Label(enum_frame, text="Advanced Options:", font=("Arial", 10, "bold")).grid(row=0, column=2, padx=5, pady=5, sticky="w")

# Create "Enumerate Database Structure" checkbox
enum_schema_var = tk.BooleanVar()
enum_schema_check = ttk.Checkbutton(enum_frame, text="Enumerate DB Structure", variable=enum_schema_var)
enum_schema_check.grid(row=1, column=2, padx=5, pady=5, sticky="w")
all_vars.append(enum_schema_var)

# Create "Enumerate Everything" checkbox
enum_all_var = tk.BooleanVar()
enum_all_check = ttk.Checkbutton(enum_frame, text="Enumerate Everything", variable=enum_all_var)
enum_all_check.grid(row=2, column=2, padx=5, pady=5, sticky="w")
all_vars.append(enum_all_var)

# Create "Exclude System Databases" label
ttk.Label(enum_frame, text="Exclude System DBs:").grid(row=3, column=2, padx=5, pady=5, sticky="e")
# Create exclude databases input field
exclude_entry = ttk.Entry(enum_frame, width=25)
exclude_entry.grid(row=3, column=3, padx=5, pady=5, sticky="w")
all_entries.append(exclude_entry)

# Create "Dump Table Data" checkbox
dump_var = tk.BooleanVar()
dump_check = ttk.Checkbutton(enum_frame, text="Dump Table Data", variable=dump_var)
dump_check.grid(row=4, column=2, padx=5, pady=5, sticky="w")
all_vars.append(dump_var)

# Create "Dump All Data" checkbox
dump_all_var = tk.BooleanVar()
dump_all_check = ttk.Checkbutton(enum_frame, text="Dump All Data", variable=dump_all_var)
dump_all_check.grid(row=5, column=2, padx=5, pady=5, sticky="w")
all_vars.append(dump_all_var)

# Create "WHERE Condition" label
ttk.Label(enum_frame, text="WHERE Condition:").grid(row=6, column=2, padx=5, pady=5, sticky="e")
# Create WHERE condition input field
where_entry = ttk.Entry(enum_frame, width=25)
where_entry.grid(row=6, column=3, padx=5, pady=5, sticky="w")
all_entries.append(where_entry)

# Create "Start Row" label
ttk.Label(enum_frame, text="Start Row:").grid(row=7, column=2, padx=5, pady=5, sticky="e")
# Create start row variable, default "1"
start_var = tk.StringVar(value="1")
# Create start row input field
start_entry = ttk.Entry(enum_frame, textvariable=start_var, width=5)
start_entry.grid(row=7, column=3, padx=5, pady=5, sticky="w")
all_entries.append(start_entry)
all_vars.append(start_var)
default_vars.append(start_var)  # Add to default variables list

# Create "End Row" label
ttk.Label(enum_frame, text="End Row:").grid(row=8, column=2, padx=5, pady=5, sticky="e")
# Create end row variable, default "100"
stop_var = tk.StringVar(value="100")
# Create end row input field
stop_entry = ttk.Entry(enum_frame, textvariable=stop_var, width=5)
stop_entry.grid(row=8, column=3, padx=5, pady=5, sticky="w")
all_entries.append(stop_entry)
all_vars.append(stop_var)
default_vars.append(stop_var)  # Add to default variables list

# ====================== Performance Settings Tab ======================

# Create "Threads" label
ttk.Label(performance_frame, text="Threads:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
# Create threads variable, default "1"
threads_var = tk.StringVar(value="1")
# Create threads dropdown
threads_combo = ttk.Combobox(performance_frame, textvariable=threads_var, width=5)
threads_combo['values'] = ("1", "2", "4", "8", "16")
threads_combo.grid(row=0, column=1, padx=5, pady=5, sticky="w")
all_entries.append(threads_combo)
all_vars.append(threads_var)

# Create "Request Delay" label
ttk.Label(performance_frame, text="Request Delay (sec):").grid(row=1, column=0, padx=5, pady=5, sticky="e")
# Create delay variable, default "0"
delay_var = tk.StringVar(value="0")
delay_combo = ttk.Combobox(performance_frame, textvariable=delay_var, width=5)
delay_combo['values'] = ("0", "0.5", "1", "2", "5")
delay_combo.grid(row=1, column=1, padx=5, pady=5, sticky="w")
all_entries.append(delay_combo)
all_vars.append(delay_var)

# Create "Timeout" label
ttk.Label(performance_frame, text="Timeout (sec):").grid(row=2, column=0, padx=5, pady=5, sticky="e")
# Create timeout variable, default "30"
timeout_var = tk.StringVar(value="30")
timeout_combo = ttk.Combobox(performance_frame, textvariable=timeout_var, width=5)
timeout_combo['values'] = ("10", "30", "60", "120")
timeout_combo.grid(row=2, column=1, padx=5, pady=5, sticky="w")
all_entries.append(timeout_combo)
all_vars.append(timeout_var)

# Create "Retries" label
ttk.Label(performance_frame, text="Retries:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
# Create retries variable, default "3"
retries_var = tk.StringVar(value="3")
retries_combo = ttk.Combobox(performance_frame, textvariable=retries_var, width=5)
retries_combo['values'] = ("1", "2", "3", "5")
retries_combo.grid(row=3, column=1, padx=5, pady=5, sticky="w")
all_entries.append(retries_combo)
all_vars.append(retries_var)

# ====================== Input/Output Settings Tab ======================
# Create "SQLMap Path" label
ttk.Label(output_frame, text="SQLMap Path:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
# Create SQLMap path input field, set default value
sqlmap_path_entry = ttk.Entry(output_frame, width=60)
sqlmap_path_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

# Set default path (you can modify this default value)
sqlmap_path_entry.insert(0, "D:\\tools\\SQLMap\\sqlmap.py")

# Create "Output Directory" label
ttk.Label(output_frame, text="Output Directory:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
# Create output directory input field
output_entry = ttk.Entry(output_frame, width=60)
output_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")
all_entries.append(output_entry)

# ====================== Brute Force Results Area ======================

# Create brute force results frame (with title)
results_frame = ttk.LabelFrame(root, text="Brute Force Results")
# Place frame in main window, horizontal fill
results_frame.pack(fill='x', padx=10, pady=5)

# Create "Database Names" label
db_name_label = ttk.Label(results_frame, text="Database Names")
# Place label in results frame at row 0, column 0
db_name_label.grid(row=0, column=0, padx=5, pady=5)
# Create database names display text box (with scrollbar)
db_name_text = scrolledtext.ScrolledText(results_frame, height=6, width=25)
db_name_text.grid(row=1, column=0, padx=5, pady=5)

# Create "Table Names" label
table_name_label = ttk.Label(results_frame, text="Table Names")
table_name_label.grid(row=0, column=1, padx=5, pady=5)
# Create table names display text box
table_name_text = scrolledtext.ScrolledText(results_frame, height=6, width=25)
table_name_text.grid(row=1, column=1, padx=5, pady=5)

# Create "Data Columns" label
columns_label = ttk.Label(results_frame, text="Data Columns")
columns_label.grid(row=0, column=2, padx=5, pady=5)
# Create data columns display text box
columns_text = scrolledtext.ScrolledText(results_frame, height=6, width=25)
columns_text.grid(row=1, column=2, padx=5, pady=5)

# ====================== Command Display Area ======================

# Create command frame (with title)
command_frame = ttk.LabelFrame(root, text="SQLMap Command")
command_frame.pack(fill='x', padx=10, pady=5)

# Create command display text box (with scrollbar)
command_text = scrolledtext.ScrolledText(command_frame, height=5, width=100)
command_text.pack(fill='both', expand=True, padx=5, pady=5)

# ====================== Button Area ======================

# Create button frame
button_frame = ttk.Frame(root)
button_frame.pack(fill='x', padx=10, pady=10)

# Create "Generate Command" button
generate_btn = ttk.Button(button_frame, text="Generate Command", command=generate_sqlmap_command)
generate_btn.pack(side='left', padx=5)  # Place button (left side)

# Create "Clear Fields" button
clear_btn = ttk.Button(button_frame, text="Clear Fields", command=clear_fields)
clear_btn.pack(side='left', padx=5)

# Create "Clear SQLMap Cache" button
purge_btn = ttk.Button(button_frame, text="Clear SQLMap Cache", command=clear_sqlmap)
purge_btn.pack(side='left', padx=5)

# Create "Execute SQLMap" button
execute_btn = ttk.Button(button_frame, text="Execute SQLMap", command=execute_sqlmap)
execute_btn.pack(side='left', padx=5)

# Create "Exit" button
exit_btn = ttk.Button(button_frame, text="Exit", command=root.destroy)
exit_btn.pack(side='right', padx=5)  # Place button (right side)

# Start main event loop, display GUI interface
root.mainloop()

