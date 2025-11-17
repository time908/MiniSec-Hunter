#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图形化关键词扫描器
value = 关键词 + 其后50字符
"""
import re, csv, datetime, threading, os, sys
from pathlib import Path
from tkinter import *
from tkinter import ttk, filedialog, messagebox

NOW = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
text_suffix = {".js", ".json", ".ts", ".wxml", ".wxss", ".xml",
               ".html", ".css", ".scss", ".less", ".vue"}

# ---------- 工具 ----------
def load_keywords(kw_path):
    with open(kw_path, encoding="utf-8") as f:
        return [l.strip() for l in f if l.strip() and not l.startswith("#")]

def scan_file(fp, kw_re, out_list):
    try:
        txt = fp.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return
    for idx, line in enumerate(txt.splitlines(), 1):
        m = kw_re.search(line)
        if not m:
            continue
        kw = m.group(0)
        start, _ = m.span()
        value = line[start:start+50]        # 关键词+后50字符
        out_list.append([kw, str(fp), idx, value, line.strip()])

# ---------- GUI ----------
class App:
    def __init__(self, root):
        self.root = root
        root.title("关键词-50字符 扫描器")
        root.geometry("1000x600")
        # 顶部
        frm = Frame(root)
        frm.pack(pady=5, padx=10, fill=X)
        Label(frm, text="目标文件夹:").grid(row=0, column=0, sticky=W)
        self.folder_var = StringVar()
        Entry(frm, textvariable=self.folder_var, width=60).grid(row=0, column=1, padx=5)
        Button(frm, text="浏览", command=self.choose_folder).grid(row=0, column=2)
        Label(frm, text="字典文件:").grid(row=1, column=0, sticky=W)
        self.dict_var = StringVar()
        Entry(frm, textvariable=self.dict_var, width=60).grid(row=1, column=1, padx=5)
        Button(frm, text="浏览", command=self.choose_dict).grid(row=1, column=2)
        self.run_btn = Button(frm, text="开始扫描", command=self.thread_run, width=12)
        self.run_btn.grid(row=0, column=3, rowspan=2, padx=10)
        # 结果表格
        self.tree = ttk.Treeview(root, columns=("kw", "file", "line", "value"), show="headings")
        self.tree.pack(expand=True, fill=BOTH, padx=10, pady=5)
        for col, text, w in zip(("kw", "file", "line", "value"),
                                ("关键词", "文件", "行号", "取值(50char)"),
                                (120, 450, 60, 250)):
            self.tree.heading(col, text=text)
            self.tree.column(col, width=w, anchor=W)
        # 底部
        bottom = Frame(root)
        bottom.pack(fill=X, padx=10, pady=5)
        Button(bottom, text="导出CSV", command=self.export_csv).pack(side=RIGHT)
        self.status = Label(bottom, text="就绪")
        self.status.pack(side=LEFT)
        self.data = []

    # ------ 选择路径 ------
    def choose_folder(self):
        d = filedialog.askdirectory()
        if d:
            self.folder_var.set(d)
    def choose_dict(self):
        f = filedialog.askopenfilename(filetypes=[("Text", "*.txt"), ("All", "*.*")])
        if f:
            self.dict_var.set(f)

    # ------ 扫描 ------
    def thread_run(self):
        if not self.folder_var.get() or not self.dict_var.get():
            messagebox.showwarning("提示", "请先选择文件夹和字典")
            return
        self.run_btn.config(state=DISABLED)
        self.status.config(text="扫描中…")
        threading.Thread(target=self.run_scan, daemon=True).start()

    def run_scan(self):
        folder = Path(self.folder_var.get())
        try:
            kws = load_keywords(self.dict_var.get())
            kw_re = re.compile("|".join(map(re.escape, kws)), re.I)
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("错误", str(e)))
            self.root.after(0, lambda: self.run_btn.config(state=NORMAL))
            return
        hits = []
        for fp in folder.rglob("*"):
            if fp.is_file() and fp.suffix.lower() in text_suffix:
                scan_file(fp, kw_re, hits)
        self.root.after(0, lambda: self.fill_table(hits))

    def fill_table(self, hits):
        for i in self.tree.get_children():
            self.tree.delete(i)
        self.data = hits
        for kw, file, line, value, raw in hits:
            self.tree.insert("", END, values=(kw, file, line, value))
        self.status.config(text=f"共 {len(hits)} 条结果")
        self.run_btn.config(state=NORMAL)

    # ------ 导出 ------
    def export_csv(self):
        if not self.data:
            messagebox.showinfo("提示", "暂无结果可导出")
            return
        fpath = filedialog.asksaveasfilename(defaultextension=".csv",
                                           filetypes=[("CSV", "*.csv")],
                                           initialfile=f"result_{NOW}.csv")
        if not fpath:
            return
        with open(fpath, "w", newline="", encoding="utf8") as f:
            cw = csv.writer(f)
            cw.writerow(["关键词", "文件", "行号", "取值", "原行"])
            cw.writerows(self.data)
        messagebox.showinfo("完成", f"已导出 {len(self.data)} 条 → {fpath}")

# ---------- main ----------
if __name__ == "__main__":
    root = Tk()
    App(root)
    root.mainloop()