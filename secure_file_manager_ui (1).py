
# # secure_file_manager_ui.py
# #second code

# import tkinter as tk
# from tkinter import ttk, messagebox, filedialog, simpledialog
# import os
# import time

# # In-memory user database and permissions
# users = {}
# permissions = {}

# # --- Authentication Module ---
# def register_user(username, password):
#     if username in users:
#         return False
#     users[username] = password
#     return True

# def authenticate_user(username, password):
#     return users.get(username) == password

# def generate_static_otp():
#     return "123456"  # Simulated OTP for demo

# # --- File Operations Module ---
# def encrypt_file(file_path, user):
#     with open(file_path, 'rb') as f:
#         data = f.read()
#     encrypted_path = file_path + ".enc"
#     with open(encrypted_path, 'wb') as f:
#         f.write(data[::-1])  # Simple reverse encryption
#     return encrypted_path

# def decrypt_file(file_path, user):
#     with open(file_path, 'rb') as f:
#         data = f.read()
#     if file_path.endswith(".enc"):
#         output = file_path.replace(".enc", "_decrypted")
#         with open(output, 'wb') as f:
#             f.write(data[::-1])
#         return output
#     return None

# def get_file_metadata(file_path):
#     stats = os.stat(file_path)
#     return {
#         "name": os.path.basename(file_path),
#         "size": stats.st_size,
#         "creator": "unknown",
#         "created": time.ctime(stats.st_ctime),
#         "modified": time.ctime(stats.st_mtime)
#     }

# # --- Threat Detection Module ---
# def validate_input(file_path):
#     return len(file_path) < 255  # Dummy check

# def detect_malware(file_path):
#     return False  # No malware in demo

# def log_threat(user, file_path, reason):
#     print(f"[THREAT] {user} -> {file_path} : {reason}")

# # --- Access Control Module ---
# def set_initial_permissions(file_path, user):
#     permissions[file_path] = {"read": [user], "write": [user]}

# def get_permissions(file_path):
#     return permissions.get(file_path, {"read": [], "write": []})

# def add_permission(file_path, user, perm):
#     perms = permissions.setdefault(file_path, {"read": [], "write": []})
#     if user not in perms[perm]:
#         perms[perm].append(user)
#     return True

# def remove_permission(file_path, user, perm):
#     perms = permissions.get(file_path, {})
#     if user in perms.get(perm, []):
#         perms[perm].remove(user)
#         return True
#     return False

# def has_permission(file_path, user, perm):
#     return user in permissions.get(file_path, {}).get(perm, [])

# # --- Main Application ---
# logged_in_user = None

# def check_login_required():
#     global logged_in_user
#     if not logged_in_user:
#         messagebox.showerror("Access Denied", "You must log in first!")
#         return False
#     return True

# # Authentication Handlers
# def handle_register():
#     user = username_var.get().strip()
#     pwd = password_var.get().strip()
#     if not user or not pwd:
#         messagebox.showwarning("Input Required", "Please enter both username and password.")
#         return
#     if register_user(user, pwd):
#         messagebox.showinfo("Success", "Registration successful!")
#     else:
#         messagebox.showerror("Error", "Username already exists!")


# def handle_login():
#     global logged_in_user
#     user = username_var.get().strip()
#     pwd = password_var.get().strip()
#     if authenticate_user(user, pwd):
#         otp = generate_static_otp()
#         entry = simpledialog.askstring("OTP Verification", f"Enter OTP (demo: {otp}):")
#         if entry == otp:
#             logged_in_user = user
#             status_var.set(f"Logged in as: {user}")
#             messagebox.showinfo("Success", "Login successful!")
#         else:
#             messagebox.showerror("Error", "Invalid OTP.")
#     else:
#         messagebox.showerror("Error", "Invalid credentials.")

# # File Operation Handlers
# def handle_encrypt():
#     if not check_login_required(): return
#     path = filedialog.askopenfilename(title="Select File to Encrypt")
#     if path:
#         if not validate_input(path):
#             log_threat(logged_in_user, path, "Invalid input")
#             messagebox.showerror("Error", "Invalid file path.")
#             return
#         if detect_malware(path):
#             log_threat(logged_in_user, path, "Malware detected")
#             messagebox.showerror("Threat", "Malware detected. Aborting.")
#             return
#         enc = encrypt_file(path, logged_in_user)
#         set_initial_permissions(enc, logged_in_user)
#         messagebox.showinfo("Encrypted", f"File encrypted:\n{enc}")


# def handle_decrypt():
#     if not check_login_required(): return
#     path = filedialog.askopenfilename(title="Select File to Decrypt")
#     if path and has_permission(path, logged_in_user, "read"):
#         out = decrypt_file(path, logged_in_user)
#         if out:
#             messagebox.showinfo("Decrypted", f"File decrypted to:\n{out}")
#         else:
#             messagebox.showwarning("Warning", "Not a valid encrypted file.")
#     else:
#         messagebox.showerror("Access Denied", "No read permission.")


# def handle_metadata():
#     if not check_login_required(): return
#     path = filedialog.askopenfilename(title="Select File for Metadata")
#     if path:
#         meta = get_file_metadata(path)
#         info = (f"Name: {meta['name']}\nSize: {meta['size']} bytes"
#                 f"\nCreated: {meta['created']}\nModified: {meta['modified']}")
#         messagebox.showinfo("Metadata", info)


# def handle_permissions():
#     if not check_login_required(): return
#     path = filedialog.askopenfilename(title="Select File to Manage Permissions")
#     if not path: return
#     perms = get_permissions(path)
#     top = tk.Toplevel(root)
#     top.title(f"Permissions: {os.path.basename(path)}")
#     top.geometry("400x300")

#     # Reader frame
#     rf = ttk.LabelFrame(top, text="Readers")
#     rf.pack(side="left", fill="both", expand=True, padx=5, pady=5)
#     rb = tk.Listbox(rf)
#     rb.pack(fill="both", expand=True, padx=5, pady=5)
#     for u in perms.get("read", []): rb.insert(tk.END, u)

#     # Writer frame
#     wf = ttk.LabelFrame(top, text="Writers")
#     wf.pack(side="right", fill="both", expand=True, padx=5, pady=5)
#     wb = tk.Listbox(wf)
#     wb.pack(fill="both", expand=True, padx=5, pady=5)
#     for u in perms.get("write", []): wb.insert(tk.END, u)

#     # Buttons
#     btn_frame = ttk.Frame(top)
#     btn_frame.pack(fill="x", pady=5)
#     ttk.Button(btn_frame, text="Add Reader", command=lambda: modify_perm(path, "read", rb)).pack(side="left", expand=True)
#     ttk.Button(btn_frame, text="Remove Reader", command=lambda: modify_perm(path, "read", rb, remove=True)).pack(side="left", expand=True)
#     ttk.Button(btn_frame, text="Add Writer", command=lambda: modify_perm(path, "write", wb)).pack(side="left", expand=True)
#     ttk.Button(btn_frame, text="Remove Writer", command=lambda: modify_perm(path, "write", wb, remove=True)).pack(side="left", expand=True)

#     def modify_perm(file, perm_type, listbox, remove=False):
#         ans = simpledialog.askstring("User", f"Enter username:")
#         if ans and ans in users:
#             if remove:
#                 remove_permission(file, ans, perm_type)
#             else:
#                 add_permission(file, ans, perm_type)
#             # Refresh
#             listbox.delete(0, tk.END)
#             for u in get_permissions(file)[perm_type]:
#                 listbox.insert(tk.END, u)

# # --- GUI Setup ---
# root = tk.Tk()
# root.title("Secure File Manager")
# root.geometry("500x600")

# # Styles
# style = ttk.Style()
# style.configure("TButton", padding=6)
# style.configure("Header.TLabel", font=(None, 16, "bold"))

# # Variables
# username_var = tk.StringVar()
# password_var = tk.StringVar()
# status_var = tk.StringVar(value="Not logged in")

# # Layout
# header = ttk.Label(root, text="Secure File Manager", style="Header.TLabel")
# header.pack(pady=10)

# # Auth Frame
# auth_frame = ttk.LabelFrame(root, text="Authentication")
# auth_frame.pack(fill="x", padx=20, pady=10)

# tk.Label(auth_frame, text="Username:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
# username_entry = ttk.Entry(auth_frame, textvariable=username_var)
# username_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

# tk.Label(auth_frame, text="Password:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
# password_entry = ttk.Entry(auth_frame, textvariable=password_var, show="*")
# password_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

# btns = ttk.Frame(auth_frame)
# btns.grid(row=2, column=0, columnspan=2, pady=10)

# ttk.Button(btns, text="Register", command=handle_register).pack(side="left", padx=5)
# ttk.Button(btns, text="Login", command=handle_login).pack(side="right", padx=5)

# # Status Bar
# status = ttk.Label(root, textvariable=status_var, relief="sunken", anchor="w")
# status.pack(fill="x", side="bottom")

# # Operations Frame
# ops_frame = ttk.LabelFrame(root, text="File Operations")
# ops_frame.pack(fill="both", expand=True, padx=20, pady=10)

# ttk.Button(ops_frame, text="Encrypt File", command=handle_encrypt).pack(fill="x", pady=5, padx=10)
# ttk.Button(ops_frame, text="Decrypt File", command=handle_decrypt).pack(fill="x", pady=5, padx=10)
# ttk.Button(ops_frame, text="View Metadata", command=handle_metadata).pack(fill="x", pady=5, padx=10)
# ttk.Button(ops_frame, text="Manage Permissions", command=handle_permissions).pack(fill="x", pady=5, padx=10)

# root.mainloop()






import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Virtual Memory Manager", layout="centered")

class MemoryManager:
    def __init__(self, frames):
        self.frames = frames
        self.reset()

    def reset(self):
        self.memory = []
        self.page_faults = 0
        self.history = []

    def simulate_lru(self, pages):
        self.reset()
        recent = []
        for i, page in enumerate(pages):
            if page in self.memory:
                recent.remove(page)
                recent.append(page)
                self.history.append((i + 1, page, list(self.memory), "Hit", self.page_faults))
            else:
                self.page_faults += 1
                if len(self.memory) < self.frames:
                    self.memory.append(page)
                else:
                    lru = recent.pop(0)
                    self.memory.remove(lru)
                    self.memory.append(page)
                recent.append(page)
                self.history.append((i + 1, page, list(self.memory), "Miss", self.page_faults))
        return self.page_faults, self.history

    def simulate_optimal(self, pages):
        self.reset()
        for i in range(len(pages)):
            page = pages[i]
            if page in self.memory:
                self.history.append((i + 1, page, list(self.memory), "Hit", self.page_faults))
                continue
            self.page_faults += 1
            if len(self.memory) < self.frames:
                self.memory.append(page)
            else:
                future = pages[i+1:]
                idx = []
                for mem_page in self.memory:
                    if mem_page in future:
                        idx.append(future.index(mem_page))
                    else:
                        idx.append(float('inf'))
                self.memory[idx.index(max(idx))] = page
            self.history.append((i + 1, page, list(self.memory), "Miss", self.page_faults))
        return self.page_faults, self.history

    def simulate_fifo(self, pages):
        self.reset()
        queue = []
        for i, page in enumerate(pages):
            if page in self.memory:
                self.history.append((i + 1, page, list(self.memory), "Hit", self.page_faults))
            else:
                self.page_faults += 1
                if len(self.memory) < self.frames:
                    self.memory.append(page)
                    queue.append(page)
                else:
                    out = queue.pop(0)
                    self.memory.remove(out)
                    self.memory.append(page)
                    queue.append(page)
                self.history.append((i + 1, page, list(self.memory), "Miss", self.page_faults))
        return self.page_faults, self.history


# Streamlit UI
st.title("📊 Virtual Memory Management Tool")
st.markdown("Simulate **Paging**, **Page Faults**, and Replacement Algorithms: **LRU**, **FIFO**, **Optimal**")

frames = st.number_input("🔢 Number of Memory Frames:", min_value=1, max_value=20, value=3)
page_input = st.text_input("📥 Page Reference String (space-separated):", "7 0 1 2 0 3 0 4 2 3 0 3 2")
algo = st.selectbox("🧠 Choose Replacement Algorithm:", ["LRU", "FIFO", "Optimal"])
simulate_btn = st.button("🚀 Run Simulation")

if simulate_btn:
    try:
        pages = list(map(int, page_input.strip().split()))
        manager = MemoryManager(frames)

        if algo == "LRU":
            faults, history = manager.simulate_lru(pages)
        elif algo == "FIFO":
            faults, history = manager.simulate_fifo(pages)
        else:
            faults, history = manager.simulate_optimal(pages)

        st.success(f"✅ Total Page Faults using {algo}: **{faults}**")
        st.write("---")
        st.subheader("📋 Simulation Steps")

        # Show table
        table_data = {
            "Step": [step for step, _, _, _, _ in history],
            "Page": [page for _, page, _, _, _ in history],
            "Memory State": [mem for _, _, mem, _, _ in history],
            "Status": [status for _, _, _, status, _ in history],
            "Cumulative Faults": [fault for _, _, _, _, fault in history],
        }
        st.dataframe(table_data, use_container_width=True)

        # Plot graph
        st.subheader("📈 Page Fault Trend")
        plt.figure(figsize=(10, 4))
        steps = [step for step, _, _, _, _ in history]
        faults_over_time = [fault for _, _, _, _, fault in history]
        plt.plot(steps, faults_over_time, marker='o', color='royalblue', linewidth=2)
        plt.xlabel("Step")
        plt.ylabel("Cumulative Page Faults")
        plt.title(f"Page Faults Over Time ({algo})")
        plt.grid(True)
        st.pyplot(plt)

    except Exception as e:
        st.error(f"❌ Error: {e}")