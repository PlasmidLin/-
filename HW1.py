import tkinter as tk
from tkinter import messagebox, ttk

class ItemType:
    """物品类型类"""
    def __init__(self, name, attributes):
        self.name = name
        self.attributes = attributes  # 属性列表，例如：["保质期", "数量"]

class Item:
    """物品类，动态生成属性"""
    # 物品名称，物品说明，物品所在地址，联系人手机，邮箱
    def __init__(self, name, description, address, phone, email, item_type, **kwargs):
        self.name = name
        self.description = description
        self.address = address
        self.phone = phone
        self.email = email
        self.item_type = item_type
        self.attributes = kwargs

    def __str__(self):
        attrs = "\n".join(f"{k}: {v}" for k, v in self.attributes.items())
        return f'''
---------- 物品信息 ----------
[物品名称]：{self.name}
[物品说明]：{self.description}
[物品所在地址]：{self.address}
[联系人手机]：{self.phone}
[联系人邮箱]：{self.email}
[物品类型]：{self.item_type.name}
[物品属性]：
{attrs}
------------------------------
'''

class User:
    """用户类"""
    def __init__(self, username, password, address, phone, email, role="user", approved=False):
        self.username = username
        self.password = password
        self.address = address
        self.phone = phone
        self.email = email
        self.role = role  # "admin" 或 "user"
        self.approved = approved

class ReviveApp:
    def __init__(self, root):
        self.root = root
        self.root.title("物品复活系统")

        # 数据存储
        self.users = []  # 用户列表
        self.items = []  # 物品列表
        self.item_names = []
        self.item_types = []  # 物品类型列表
        self.item_type_names = []

        # 当前登录用户
        self.current_user = None

        # 默认管理员
        self.users.append(User("admin", "123456", "800 Dongchuan Road", "123456", "admin@sjtu.cn", role="admin", approved=True))

        self.login_screen()

    def login_screen(self):
        """登录界面"""
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="用户名:").grid(row=0, column=0)
        username_entry = tk.Entry(self.root)
        username_entry.grid(row=0, column=1)

        tk.Label(self.root, text="密码:").grid(row=1, column=0)
        password_entry = tk.Entry(self.root, show="*")
        password_entry.grid(row=1, column=1)

        tk.Button(self.root, text="登录", command=lambda: self.login(username_entry.get(), password_entry.get())).grid(row=2, column=0, columnspan=2)
        tk.Button(self.root, text="注册", command=self.register_screen).grid(row=3, column=0, columnspan=2)

    def register_screen(self):
        """注册界面"""
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="用户名:").grid(row=0, column=0)
        username_entry = tk.Entry(self.root)
        username_entry.grid(row=0, column=1)

        tk.Label(self.root, text="密码:").grid(row=1, column=0)
        password1_entry = tk.Entry(self.root, show='*')
        password1_entry.grid(row=1, column=1)

        tk.Label(self.root, text="确认密码:").grid(row=2, column=0)
        password2_entry = tk.Entry(self.root, show='*')
        password2_entry.grid(row=2, column=1)

        tk.Label(self.root, text="地址:").grid(row=3, column=0)
        address_entry = tk.Entry(self.root)
        address_entry.grid(row=3, column=1)

        tk.Label(self.root, text="手机号:").grid(row=4, column=0)
        phone_entry = tk.Entry(self.root)
        phone_entry.grid(row=4, column=1)

        tk.Label(self.root, text="邮箱:").grid(row=5, column=0)
        email_entry = tk.Entry(self.root)
        email_entry.grid(row=5, column=1)

        tk.Button(self.root, text="提交注册", command=lambda: self.register_user(
            username_entry.get(), password1_entry.get(), password2_entry.get(), address_entry.get(), phone_entry.get(), email_entry.get()
        )).grid(row=6, column=0, columnspan=2)
        tk.Button(self.root, text="返回登录", command=self.login_screen).grid(row=7, column=0, columnspan=2)

    def register_user(self, username, password1, password2, address, phone, email):
        if not all([username,password1, address, phone, email]):
            messagebox.showwarning("警告", "请完整填写注册信息！")
            return
        if password1 != password2:
            messagebox.showwarning("警告", "两次输入密码不一致！")
            return

        self.users.append(User(username, password1, address, phone, email))
        messagebox.showinfo("成功", "注册成功，请等待管理员审批！")
        self.login_screen()

    def login(self, username, password):
        for user in self.users:
            if user.username == username:
                if not user.approved:
                    messagebox.showwarning("警告", "您的账户尚未被管理员批准！")
                    return
                if user.password != password:
                    messagebox.showwarning("警告", "密码错误！")
                    return
                self.current_user = user
                if user.role == "admin":
                    self.admin_screen()
                else:
                    self.user_screen()
                return
        messagebox.showwarning("警告", "用户不存在！")

    def admin_screen(self):
        """管理员界面"""
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Button(self.root, text="审批用户", command=self.approve_users_screen).grid(row=0, column=0, columnspan=2)
        tk.Button(self.root, text="管理物品类型", command=self.manage_item_types_screen).grid(row=1, column=0, columnspan=2)
        tk.Button(self.root, text="退出登录", command=self.login_screen).grid(row=2, column=0, columnspan=2)

    def user_screen(self):
        """普通用户界面"""
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Button(self.root, text="添加物品", command=self.add_item_screen).grid(row=0, column=0, columnspan=2)
        tk.Button(self.root, text="删除物品", command=self.delete_item_screen).grid(row=1, column=0, columnspan=2)
        tk.Button(self.root, text="搜索物品", command=self.search_item_screen).grid(row=2, column=0, columnspan=2)
        tk.Button(self.root, text="退出登录", command=self.login_screen).grid(row=3, column=0, columnspan=2)

    def approve_users_screen(self):
        """管理员审批用户界面"""
        for widget in self.root.winfo_children():
            widget.destroy()

        for i, user in enumerate(self.users):
            if not user.approved:
                tk.Label(self.root, text=f"用户名: {user.username}, 邮箱: {user.email}").grid(row=i, column=0)
                tk.Button(self.root, text="批准", command=lambda u=user: self.approve_user(u)).grid(row=i, column=1)

        tk.Button(self.root, text="返回", command=self.admin_screen).grid(row=len(self.users), column=0, columnspan=2)

    def approve_user(self, user):
        user.approved = True
        messagebox.showinfo("成功", f"用户 {user.username} 已批准！")
        self.approve_users_screen()

    def manage_item_types_screen(self):
        """管理物品类型界面"""
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="物品类型名称:").grid(row=0, column=0)
        type_name_entry = tk.Entry(self.root)
        type_name_entry.grid(row=0, column=1)

        tk.Label(self.root, text="属性(英文逗号分隔):").grid(row=1, column=0)
        attributes_entry = tk.Entry(self.root)
        attributes_entry.grid(row=1, column=1)

        tk.Button(self.root, text="添加类型", command=lambda: self.add_item_type(
            type_name_entry.get(), attributes_entry.get()
        )).grid(row=2, column=0, columnspan=2)
        tk.Button(self.root, text="返回", command=self.admin_screen).grid(row=3, column=0, columnspan=2)

    def add_item_type(self, name, attributes):
        if not name or not attributes:
            messagebox.showwarning("警告", "请填写完整的物品类型信息！")
            return

        attributes_list = [attr.strip() for attr in attributes.split(",")]
        if name not in self.item_type_names:
            self.item_types.append(ItemType(name, attributes_list))
            messagebox.showinfo("成功", f"物品类型 {name} 已添加！")
            self.item_type_names.append(name)
        else:
            for item_type in self.item_types:
                if item_type.name == name:
                    item_type.attributes = attributes_list
            messagebox.showinfo("成功", f"已修改物品类型 {name} 的属性！")


    def add_item_screen(self):
        """普通用户添加物品界面"""
        for widget in self.root.winfo_children():
            widget.destroy()

        if not self.item_types:
            messagebox.showwarning("警告", "暂无可用物品类型，请联系管理员添加！")
            self.user_screen()
            return
        tk.Label(self.root, text="物品名:").grid(row=0, column=0)
        name_entry = tk.Entry(self.root)
        name_entry.grid(row=0, column=1)

        tk.Label(self.root, text="物品说明:").grid(row=1, column=0)
        description_entry = tk.Entry(self.root)
        description_entry.grid(row=1, column=1)

        tk.Label(self.root, text="物品所在地址:").grid(row=2, column=0)
        address_entry = tk.Entry(self.root)
        address_entry.grid(row=2, column=1)

        tk.Label(self.root, text="联系人手机:").grid(row=3, column=0)
        phone_entry = tk.Entry(self.root)
        phone_entry.grid(row=3, column=1)

        tk.Label(self.root, text="联系人邮箱:").grid(row=5, column=0)
        email_entry = tk.Entry(self.root)
        email_entry.grid(row=5, column=1)

        tk.Label(self.root, text="选择物品类型:").grid(row=6, column=0)
        type_var = tk.StringVar()
        type_menu = ttk.Combobox(self.root, textvariable=type_var, values=[t.name for t in self.item_types])
        type_menu.grid(row=6, column=1)

        def populate_fields():
            """动态生成字段"""
            for widget in self.root.grid_slaves():
                if int(widget.grid_info()["row"]) > 6:
                    widget.destroy()

            selected_type = next((t for t in self.item_types if t.name == type_var.get()), None)
            if not selected_type:
                return

            entries = {}
            for i, attr in enumerate(selected_type.attributes):
                tk.Label(self.root, text=attr + ":").grid(row=i + 7, column=0)
                entry = tk.Entry(self.root)
                entry.grid(row=i + 7, column=1)
                entries[attr] = entry

            tk.Button(self.root, text="提交", command=lambda: self.add_item(
                name_entry.get(), description_entry.get(), address_entry.get(), phone_entry.get(), email_entry.get(), 
                selected_type, entries)).grid(row=len(selected_type.attributes) + 7, column=0, columnspan=2)
            tk.Button(self.root, text="返回", command=self.user_screen).grid(row=len(selected_type.attributes) + 8, column=0, columnspan=2)

        type_menu.bind("<<ComboboxSelected>>", lambda e: populate_fields())
        tk.Button(self.root, text="返回", command=self.user_screen).grid(row = 7, column=0, columnspan=2)

    def add_item(self,  name, description, address, phone, email, item_type, entries):
        attributes = {attr: entry.get() for attr, entry in entries.items() if entry.get()}
        if name == '/':
            messagebox.showwarning("警告", "抱歉，物品名称不能为“/”！")
            return
        if len(attributes) != len(item_type.attributes) or not all([name, description, address, phone, email]):
            messagebox.showwarning("警告", "请填写所有字段！")
            return
        if name in self.item_names:
            messagebox.showwarning("警告", "已有同名物品存在！")
            return
        self.items.append(Item(name, description, address, phone, email, item_type, **attributes))
        self.item_names.append(name)
        messagebox.showinfo("成功", "物品已添加！")
        self.user_screen()
    
    def delete_item_screen(self):
        """普通用户删除物品界面"""
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="物品名称").grid(row=0, column=0)
        name_entry = tk.Entry(self.root)
        name_entry.grid(row=0, column=1)
        
        tk.Button(self.root, text="显示物品信息", command=lambda: self.show_item(name_entry.get())).grid(row=1, column=0, columnspan=2)
        tk.Button(self.root, text="确认删除", command=lambda: self.delete_item(name_entry.get())).grid(row=2, column=0, columnspan=2)


        tk.Button(self.root, text="返回", command=self.user_screen).grid(row=3, column=0, columnspan=2)

    def show_item(self, name):
        item = [v for v in self.items if v.name == name]
        if len(item) == 0:
            messagebox.showwarning("警告", "该物品不存在！")
            return
        if len(item) > 1:
            messagebox.showwarning("警告", "ERROR！")
            return
        item = item[0]
        result_str = str(item)
        messagebox.showinfo("提示",result_str)
    

    def delete_item(self, name):
        flag = False
        for i, item in enumerate(self.items):
            if item.name == name:
                del self.items[i]
                del self.item_names[i]
                flag = True
        if not flag:
            messagebox.showwarning("警告","该物品不存在！")
            return
        messagebox.showinfo("成功","删除成功！")


    def search_item_screen(self):
        """普通用户搜索物品界面"""
        for widget in self.root.winfo_children():
            widget.destroy()

        if not self.item_types:
            messagebox.showwarning("警告", "暂无可用物品类型！")
            self.user_screen()
            return

        tk.Label(self.root, text="选择物品类型:").grid(row=0, column=0)
        type_var = tk.StringVar()
        type_menu = ttk.Combobox(self.root, textvariable=type_var, values=[t.name for t in self.item_types])
        type_menu.grid(row=0, column=1)

        tk.Label(self.root, text="关键字（物品名称/说明）:").grid(row=1, column=0)
        keyword_entry = tk.Entry(self.root)
        keyword_entry.grid(row=1, column=1)
        tk.Label(self.root, text="【温馨提示：使用关键字“/”查看该类型下所有的物品】").grid(row=2, column=0, columnspan=2)

        tk.Button(self.root, text="搜索", command=lambda: self.search_item(type_var.get(), keyword_entry.get())).grid(row=3, column=0, columnspan=2)
        tk.Button(self.root, text="返回", command=self.user_screen).grid(row=4, column=0, columnspan=2)

    def search_item(self, type_name, keyword):
        selected_type = next((t for t in self.item_types if t.name == type_name), None)
        if not selected_type:
            messagebox.showwarning("警告", "请选择有效的物品类型！")
            return
        if keyword == '/':
            results = [item for item in self.items if item.item_type == selected_type]
        else:
            results = [item for item in self.items if item.item_type == selected_type and 
                    (any(v.lower() in str(item.name).lower() for v in keyword)
                     or any(v.lower() in str(item.description).lower() for v in keyword))]


        if not results:
            messagebox.showinfo("结果", "未找到匹配的物品！")
        else:
            result_str = "\n".join(str(item) for item in results)
            messagebox.showinfo("搜索结果", result_str)

if __name__ == "__main__":
    root = tk.Tk()
    app = ReviveApp(root)
    root.mainloop()
