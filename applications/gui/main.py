import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os


class HTCMigrationGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("HTC Database Migration Tool")
        self.root.geometry("700x600")
        self.root.resizable(True, True)
        
        # Configure grid weights for responsive design
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # Variables for form data
        self.htc_apps_path = tk.StringVar(value="")
        self.conversion_type = tk.StringVar(value="migrate")
        self.driver_type = tk.StringVar(value="ODBC Driver 17 for SQL Server")
        self.thread_count = tk.IntVar(value=self.get_default_threads())
        self.database_name = tk.StringVar(value="HTC_Migration")
        self.overwrite_database = tk.BooleanVar(value=False)
        
        # Create the main interface
        self.create_widgets()
        
    def get_default_threads(self):
        """Get default thread count (half of available CPUs, minimum 1)"""
        cpu_count = os.cpu_count() or 1
        return max(1, cpu_count // 2)
    
    def get_max_threads(self):
        """Get maximum available threads"""
        return os.cpu_count() or 1
    
    def create_widgets(self):
        # Main container with padding
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="HTC Database Migration Tool", 
                               font=("Arial", 18, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 30), sticky="w")
        
        current_row = 1
        
        # HTC Apps File Location
        current_row = self.create_file_location_section(main_frame, current_row)
        
        # Conversion Type
        current_row = self.create_conversion_type_section(main_frame, current_row)
        
        # Driver Type
        current_row = self.create_driver_type_section(main_frame, current_row)
        
        # Thread Count
        current_row = self.create_thread_count_section(main_frame, current_row)
        
        # Database Options
        current_row = self.create_database_options_section(main_frame, current_row)
        
        # Control Buttons
        current_row = self.create_control_buttons_section(main_frame, current_row)
        
        # Status/Info Section
        self.create_status_section(main_frame, current_row)
    
    def create_file_location_section(self, parent, row):
        """Create HTC Apps file location selection section"""
        # Label
        ttk.Label(parent, text="HTC Apps Location:", 
                 font=("Arial", 10, "bold")).grid(row=row, column=0, sticky="w", pady=(0, 5))
        
        # File path frame
        path_frame = ttk.Frame(parent)
        path_frame.grid(row=row+1, column=0, columnspan=3, sticky="ew", pady=(0, 20))
        path_frame.columnconfigure(0, weight=1)
        
        # Entry for path
        self.path_entry = ttk.Entry(path_frame, textvariable=self.htc_apps_path, 
                                   font=("Arial", 9), width=60)
        self.path_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        
        # Browse button
        browse_btn = ttk.Button(path_frame, text="Browse...", 
                               command=self.browse_htc_apps_location)
        browse_btn.grid(row=0, column=1)
        
        return row + 2
    
    def create_conversion_type_section(self, parent, row):
        """Create conversion type selection section"""
        ttk.Label(parent, text="Conversion Type:", 
                 font=("Arial", 10, "bold")).grid(row=row, column=0, sticky="w", pady=(0, 5))
        
        # Radio buttons frame
        conversion_frame = ttk.Frame(parent)
        conversion_frame.grid(row=row+1, column=0, columnspan=3, sticky="w", pady=(0, 20))
        
        # Migrate option
        migrate_radio = ttk.Radiobutton(conversion_frame, text="Migrate", 
                                       variable=self.conversion_type, value="migrate")
        migrate_radio.grid(row=0, column=0, sticky="w", padx=(0, 20))
        
        # Normalize option  
        normalize_radio = ttk.Radiobutton(conversion_frame, text="Normalize", 
                                         variable=self.conversion_type, value="normalize")
        normalize_radio.grid(row=0, column=1, sticky="w")
        
        return row + 2
    
    def create_driver_type_section(self, parent, row):
        """Create driver type selection section"""
        ttk.Label(parent, text="SQL Server Driver:", 
                 font=("Arial", 10, "bold")).grid(row=row, column=0, sticky="w", pady=(0, 5))
        
        # Driver dropdown
        driver_combo = ttk.Combobox(parent, textvariable=self.driver_type, 
                                   state="readonly", width=40, font=("Arial", 9))
        driver_combo['values'] = [
            "ODBC Driver 17 for SQL Server",
            "ODBC Driver 18 for SQL Server", 
            "ODBC Driver 13 for SQL Server",
            "SQL Server Native Client 11.0",
            "SQL Server"
        ]
        driver_combo.grid(row=row+1, column=0, columnspan=3, sticky="w", pady=(0, 20))
        
        return row + 2
    
    def create_thread_count_section(self, parent, row):
        """Create thread count selection section"""
        ttk.Label(parent, text="Number of Threads:", 
                 font=("Arial", 10, "bold")).grid(row=row, column=0, sticky="w", pady=(0, 5))
        
        # Thread count frame
        thread_frame = ttk.Frame(parent)
        thread_frame.grid(row=row+1, column=0, columnspan=3, sticky="ew", pady=(0, 20))
        thread_frame.columnconfigure(0, weight=1)
        
        # Scale for thread selection
        max_threads = self.get_max_threads()
        thread_scale = ttk.Scale(thread_frame, from_=1, to=max_threads, 
                               orient=tk.HORIZONTAL, variable=self.thread_count,
                               command=self.update_thread_label)
        thread_scale.grid(row=0, column=0, sticky="ew", padx=(0, 15))
        
        # Thread count label
        self.thread_label = ttk.Label(thread_frame, text=f"{self.thread_count.get()} threads")
        self.thread_label.grid(row=0, column=1)
        
        # CPU info label
        cpu_info = ttk.Label(thread_frame, text=f"(Max available: {max_threads})", 
                           font=("Arial", 8), foreground="gray")
        cpu_info.grid(row=1, column=0, columnspan=2, sticky="w", pady=(5, 0))
        
        return row + 2
    
    def create_database_options_section(self, parent, row):
        """Create database name and overwrite options section"""
        ttk.Label(parent, text="Database Options:", 
                 font=("Arial", 10, "bold")).grid(row=row, column=0, sticky="w", pady=(0, 5))
        
        # Database name
        db_frame = ttk.Frame(parent)
        db_frame.grid(row=row+1, column=0, columnspan=3, sticky="ew", pady=(0, 10))
        db_frame.columnconfigure(1, weight=1)
        
        ttk.Label(db_frame, text="Database Name:").grid(row=0, column=0, sticky="w", padx=(0, 10))
        db_entry = ttk.Entry(db_frame, textvariable=self.database_name, 
                            font=("Arial", 9), width=25)
        db_entry.grid(row=0, column=1, sticky="ew")
        
        # Overwrite checkbox
        overwrite_check = ttk.Checkbutton(parent, text="Overwrite existing database", 
                                         variable=self.overwrite_database)
        overwrite_check.grid(row=row+2, column=0, columnspan=3, sticky="w", pady=(0, 20))
        
        return row + 3
    
    def create_control_buttons_section(self, parent, row):
        """Create control buttons section"""
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=row, column=0, columnspan=3, pady=(10, 20))
        
        # Validate Settings button
        validate_btn = ttk.Button(button_frame, text="Validate Settings", 
                                 command=self.validate_settings)
        validate_btn.grid(row=0, column=0, padx=(0, 10))
        
        # Start Migration button (placeholder)
        start_btn = ttk.Button(button_frame, text="Start Migration", 
                              command=self.start_migration_placeholder,
                              style="Accent.TButton")
        start_btn.grid(row=0, column=1, padx=(0, 10))
        
        # Reset button
        reset_btn = ttk.Button(button_frame, text="Reset", 
                              command=self.reset_form)
        reset_btn.grid(row=0, column=2)
        
        return row + 1
    
    def create_status_section(self, parent, row):
        """Create status/information display section"""
        # Status frame
        status_frame = ttk.LabelFrame(parent, text="Status & Information", padding="10")
        status_frame.grid(row=row, column=0, columnspan=3, sticky="nsew", pady=(10, 0))
        status_frame.columnconfigure(0, weight=1)
        status_frame.rowconfigure(0, weight=1)
        
        # Text widget for status messages
        self.status_text = tk.Text(status_frame, height=8, width=70, wrap=tk.WORD,
                                  font=("Courier", 9), state=tk.DISABLED)
        self.status_text.grid(row=0, column=0, sticky="nsew")
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(status_frame, orient=tk.VERTICAL, 
                                 command=self.status_text.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.status_text.configure(yscrollcommand=scrollbar.set)
        
        # Initial welcome message
        self.log_message("Welcome to HTC Database Migration Tool")
        self.log_message("Please configure your settings above and click 'Validate Settings' to begin")
    
    def browse_htc_apps_location(self):
        """Open file dialog to browse for HTC Apps location"""
        folder_path = filedialog.askdirectory(
            title="Select HTC Apps Folder",
            initialdir=self.htc_apps_path.get() or os.path.expanduser("~")
        )
        if folder_path:
            self.htc_apps_path.set(folder_path)
            self.log_message(f"Selected HTC Apps location: {folder_path}")
    
    def update_thread_label(self, value):
        """Update thread count label when scale changes"""
        thread_count = int(float(value))
        self.thread_label.config(text=f"{thread_count} threads")
    
    def validate_settings(self):
        """Validate current settings"""
        self.log_message("Validating settings...")
        
        # Check HTC Apps path
        htc_path = self.htc_apps_path.get().strip()
        if not htc_path:
            self.log_message("❌ ERROR: HTC Apps location is required")
            messagebox.showerror("Validation Error", "Please select HTC Apps location")
            return False
        
        if not os.path.exists(htc_path):
            self.log_message(f"❌ ERROR: HTC Apps location does not exist: {htc_path}")
            messagebox.showerror("Validation Error", "HTC Apps location does not exist")
            return False
        
        self.log_message(f"✅ HTC Apps location: {htc_path}")
        
        # Check database name
        db_name = self.database_name.get().strip()
        if not db_name:
            self.log_message("❌ ERROR: Database name is required")
            messagebox.showerror("Validation Error", "Please enter a database name")
            return False
        
        self.log_message(f"✅ Database name: {db_name}")
        
        # Log other settings
        self.log_message(f"✅ Conversion type: {self.conversion_type.get()}")
        self.log_message(f"✅ SQL Driver: {self.driver_type.get()}")
        self.log_message(f"✅ Thread count: {self.thread_count.get()}")
        self.log_message(f"✅ Overwrite database: {self.overwrite_database.get()}")
        
        self.log_message("🎉 All settings validated successfully!")
        messagebox.showinfo("Validation Success", "All settings are valid. Ready to start migration!")
        return True
    
    def start_migration_placeholder(self):
        """Placeholder for migration start functionality"""
        if self.validate_settings():
            self.log_message("🚀 Migration would start here...")
            self.log_message("(Migration functionality will be implemented later)")
            messagebox.showinfo("Migration Ready", 
                               "Settings validated! Migration functionality will be implemented in the next phase.")
    
    def reset_form(self):
        """Reset all form fields to defaults"""
        self.htc_apps_path.set("")
        self.conversion_type.set("migrate")
        self.driver_type.set("ODBC Driver 17 for SQL Server")
        self.thread_count.set(self.get_default_threads())
        self.database_name.set("HTC_Migration")
        self.overwrite_database.set(False)
        
        # Clear status
        self.status_text.config(state=tk.NORMAL)
        self.status_text.delete(1.0, tk.END)
        self.status_text.config(state=tk.DISABLED)
        
        self.log_message("Form reset to defaults")
        self.log_message("Please configure your settings and click 'Validate Settings'")
    
    def log_message(self, message):
        """Add a message to the status log"""
        self.status_text.config(state=tk.NORMAL)
        self.status_text.insert(tk.END, message + "\n")
        self.status_text.see(tk.END)
        self.status_text.config(state=tk.DISABLED)
        self.root.update_idletasks()


def main():
    """Main entry point for the GUI application"""
    root = tk.Tk()
    app = HTCMigrationGUI(root)
    
    # Center the window on screen
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()


if __name__ == "__main__":
    main()