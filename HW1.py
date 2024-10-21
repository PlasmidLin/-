import tkinter as tk
from tkinter import messagebox

class Item:
    '''物品对象'''
    def __init__(self, name, description, contact):
        self.name = name
        self.description = description
        self.contact = contact

    def __str__(self):
        return f"物品名称: {self.name}\n描述: {self.description}\n联系人: {self.contact}\n"


class ReviveApp:
    def __init__(self, root):
        '''GUI布局与功能'''
        self.root = root
        self.root.title("物品复活程序")
        self.items = []

        
        self.name_label = tk.Label(root, text="物品名称:")
        self.name_label.grid(row=0, column=0)
        self.name_entry = tk.Entry(root)
        self.name_entry.grid(row=0, column=1)

        self.desc_label = tk.Label(root, text="描述:")
        self.desc_label.grid(row=1, column=0)
        self.desc_entry = tk.Entry(root)
        self.desc_entry.grid(row=1, column=1)

        self.contact_label = tk.Label(root, text="联系人信息:")
        self.contact_label.grid(row=2, column=0)
        self.contact_entry = tk.Entry(root)
        self.contact_entry.grid(row=2, column=1)

        self.add_button = tk.Button(root, text="添加物品", command=self.add_item)
        self.add_button.grid(row=3, column=0, columnspan=2)

        self.delete_button = tk.Button(root, text="删除物品", command=self.delete_item)
        self.delete_button.grid(row=4, column=0, columnspan=2)

        self.display_button = tk.Button(root, text="显示物品列表", command=self.display_items)
        self.display_button.grid(row=5, column=0, columnspan=2)

        self.search_button = tk.Button(root, text="查找物品", command=self.search_item)
        self.search_button.grid(row=6, column=0, columnspan=2)

    def add_item(self):
        '''
        功能：查找物品
        输入：完整的物品信息
        '''
        name = self.name_entry.get()
        description = self.desc_entry.get()
        contact = self.contact_entry.get()

        if name and description and contact:
            item = Item(name, description, contact)
            self.items.append(item)
            messagebox.showinfo("成功", f"物品 '{name}' 已添加！")
        else:
            messagebox.showwarning("警告", "请完整填写物品信息！")

    def delete_item(self):
        name = self.name_entry.get()
        for item in self.items:
            if item.name == name:
                self.items.remove(item)
                messagebox.showinfo("成功", f"物品 '{name}' 已删除！")
                return
        messagebox.showwarning("警告", f"未找到物品 '{name}'！")

    def display_items(self):
        '''
        功能：物品列表
        '''
        if not self.items:
            messagebox.showinfo("提示", "当前没有物品列表！")
        else:
            items_str = "\n".join(str(item) for item in self.items)
            messagebox.showinfo("物品列表", items_str)

    def search_item(self):
        '''
        功能：查找物品
        输入：物品名
        '''
        name = self.name_entry.get()
        for item in self.items:
            if item.name == name:
                messagebox.showinfo("找到的物品", str(item))
                return
        messagebox.showwarning("警告", f"未找到物品 '{name}'！")


if __name__ == "__main__":
    root = tk.Tk()
    app = ReviveApp(root)
    root.mainloop()
