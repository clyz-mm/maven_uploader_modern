#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Maven JAR包上传工具 - 现代化版本
用于将本地jar包和pom文件上传到私有Maven仓库
使用CustomTkinter提供现代化的用户界面
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os
import sys
from pathlib import Path
import threading
import time

# 设置CustomTkinter主题
ctk.set_appearance_mode("system")  # 跟随系统主题
ctk.set_default_color_theme("blue")  # 蓝色主题


class ModernMavenUploader:
    def __init__(self):
        # 创建主窗口
        self.root = ctk.CTk()
        self.root.title("Maven JAR包上传工具 - 现代化版本")
        self.root.geometry("900x750")
        self.root.minsize(800, 650)
        
        # 设置窗口图标（如果有的话）
        try:
            self.root.iconbitmap("maven_icon.ico")
        except:
            pass
        
        # 窗口居中
        self.center_window()
        
        # 文件路径变量
        self.jar_file_path = ctk.StringVar()
        self.pom_file_path = ctk.StringVar()
        
        # Maven仓库配置变量
        self.repository_id = ctk.StringVar(value="releases")
        self.repository_url = ctk.StringVar()
        
        # Maven路径配置变量
        self.maven_path = ctk.StringVar()
        
        # 状态变量
        self.is_uploading = False
        
        self.setup_ui()
        
        # 启动时自动检测Maven
        self.auto_detect_maven()
        
    def setup_ui(self):
        """设置现代化用户界面"""
        # 主框架
        self.main_frame = ctk.CTkScrollableFrame(self.root, corner_radius=15)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # 标题区域
        self.create_header()
        
        # 文件选择区域
        self.create_file_selection_section()
        
        # Maven配置区域
        self.create_maven_config_section()
        
        # 仓库配置区域
        self.create_repository_section()
        
        # 操作按钮区域
        self.create_action_buttons()
        
        # 进度条
        self.create_progress_section()
        
        # 日志区域
        self.create_log_section()
        
    def create_header(self):
        """创建标题区域"""
        # 主标题
        title_label = ctk.CTkLabel(
            self.main_frame,
            text="🚀 Maven JAR包上传工具",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=("#1f538d", "#14375e")
        )
        title_label.pack(pady=(0, 10))
        
        # 副标题
        subtitle_label = ctk.CTkLabel(
            self.main_frame,
            text="现代化界面 · 智能检测 · 一键上传",
            font=ctk.CTkFont(size=14),
            text_color=("gray50", "gray40")
        )
        subtitle_label.pack(pady=(0, 30))
        
    def create_file_selection_section(self):
        """创建文件选择区域"""
        # 文件选择框架
        file_frame = ctk.CTkFrame(self.main_frame, corner_radius=10)
        file_frame.pack(fill="x", pady=(0, 20))
        
        # 标题
        file_title = ctk.CTkLabel(
            file_frame,
            text="📁 文件选择",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        file_title.pack(pady=(20, 15), padx=20, anchor="w")
        
        # JAR文件选择
        jar_frame = ctk.CTkFrame(file_frame, fg_color="transparent")
        jar_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        jar_label = ctk.CTkLabel(
            jar_frame,
            text="JAR文件:",
            font=ctk.CTkFont(size=14, weight="bold"),
            width=100
        )
        jar_label.pack(side="left", padx=(0, 10))
        
        self.jar_entry = ctk.CTkEntry(
            jar_frame,
            textvariable=self.jar_file_path,
            placeholder_text="选择要上传的JAR文件...",
            font=ctk.CTkFont(size=12),
            height=35
        )
        self.jar_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        jar_button = ctk.CTkButton(
            jar_frame,
            text="选择JAR",
            command=self.select_jar_file,
            width=100,
            height=35,
            font=ctk.CTkFont(size=12, weight="bold")
        )
        jar_button.pack(side="right")
        
        # POM文件选择
        pom_frame = ctk.CTkFrame(file_frame, fg_color="transparent")
        pom_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        pom_label = ctk.CTkLabel(
            pom_frame,
            text="POM文件:",
            font=ctk.CTkFont(size=14, weight="bold"),
            width=100
        )
        pom_label.pack(side="left", padx=(0, 10))
        
        self.pom_entry = ctk.CTkEntry(
            pom_frame,
            textvariable=self.pom_file_path,
            placeholder_text="选择对应的POM文件...",
            font=ctk.CTkFont(size=12),
            height=35
        )
        self.pom_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        pom_button = ctk.CTkButton(
            pom_frame,
            text="选择POM",
            command=self.select_pom_file,
            width=100,
            height=35,
            font=ctk.CTkFont(size=12, weight="bold")
        )
        pom_button.pack(side="right")
        
    def create_maven_config_section(self):
        """创建Maven配置区域"""
        # Maven配置框架
        maven_frame = ctk.CTkFrame(self.main_frame, corner_radius=10)
        maven_frame.pack(fill="x", pady=(0, 20))
        
        # 标题
        maven_title = ctk.CTkLabel(
            maven_frame,
            text="⚙️ Maven配置",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        maven_title.pack(pady=(20, 15), padx=20, anchor="w")
        
        # Maven路径配置
        maven_path_frame = ctk.CTkFrame(maven_frame, fg_color="transparent")
        maven_path_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        maven_label = ctk.CTkLabel(
            maven_path_frame,
            text="Maven路径:",
            font=ctk.CTkFont(size=14, weight="bold"),
            width=100
        )
        maven_label.pack(side="left", padx=(0, 10))
        
        self.maven_entry = ctk.CTkEntry(
            maven_path_frame,
            textvariable=self.maven_path,
            placeholder_text="Maven可执行文件路径...",
            font=ctk.CTkFont(size=12),
            height=35
        )
        self.maven_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        # Maven按钮框架
        maven_button_frame = ctk.CTkFrame(maven_path_frame, fg_color="transparent")
        maven_button_frame.pack(side="right")
        
        auto_detect_btn = ctk.CTkButton(
            maven_button_frame,
            text="自动检测",
            command=self.auto_detect_maven_manual,
            width=100,
            height=35,
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#2b5a87",
            hover_color="#1e3f5f"
        )
        auto_detect_btn.pack(side="left", padx=(0, 5))
        
        select_maven_btn = ctk.CTkButton(
            maven_button_frame,
            text="手动选择",
            command=self.select_maven_path,
            width=100,
            height=35,
            font=ctk.CTkFont(size=12, weight="bold")
        )
        select_maven_btn.pack(side="left")
        
        # Maven状态指示器
        self.maven_status_frame = ctk.CTkFrame(maven_frame, fg_color="transparent")
        self.maven_status_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        self.maven_status_label = ctk.CTkLabel(
            self.maven_status_frame,
            text="状态: 检测中...",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="blue"
        )
        self.maven_status_label.pack(anchor="w")
        
        # 帮助文本
        help_text = ctk.CTkLabel(
            self.maven_status_frame,
            text="💡 点击'自动检测'重新检测Maven，或手动选择maven可执行文件\n   例如：D:\\Maven\\apache-maven-3.9.10\\bin\\mvn.cmd",
            font=ctk.CTkFont(size=11),
            text_color=("gray50", "gray40"),
            justify="left"
        )
        help_text.pack(anchor="w", pady=(5, 0))
        
    def create_repository_section(self):
        """创建仓库配置区域"""
        # 仓库配置框架
        repo_frame = ctk.CTkFrame(self.main_frame, corner_radius=10)
        repo_frame.pack(fill="x", pady=(0, 20))
        
        # 标题
        repo_title = ctk.CTkLabel(
            repo_frame,
            text="🏪 仓库配置",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        repo_title.pack(pady=(20, 15), padx=20, anchor="w")
        
        # 仓库ID
        repo_id_frame = ctk.CTkFrame(repo_frame, fg_color="transparent")
        repo_id_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        repo_id_label = ctk.CTkLabel(
            repo_id_frame,
            text="仓库ID:",
            font=ctk.CTkFont(size=14, weight="bold"),
            width=100
        )
        repo_id_label.pack(side="left", padx=(0, 10))
        
        self.repo_id_entry = ctk.CTkEntry(
            repo_id_frame,
            textvariable=self.repository_id,
            placeholder_text="releases",
            font=ctk.CTkFont(size=12),
            height=35
        )
        self.repo_id_entry.pack(side="left", fill="x", expand=True)
        
        # 仓库URL
        repo_url_frame = ctk.CTkFrame(repo_frame, fg_color="transparent")
        repo_url_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        repo_url_label = ctk.CTkLabel(
            repo_url_frame,
            text="仓库URL:",
            font=ctk.CTkFont(size=14, weight="bold"),
            width=100
        )
        repo_url_label.pack(side="left", padx=(0, 10))
        
        self.repo_url_entry = ctk.CTkEntry(
            repo_url_frame,
            textvariable=self.repository_url,
            placeholder_text="http://10.0.129.11:8081/repository/maven-releases/",
            font=ctk.CTkFont(size=12),
            height=35
        )
        self.repo_url_entry.pack(side="left", fill="x", expand=True)
        
        # 示例URL
        example_label = ctk.CTkLabel(
            repo_frame,
            text="💡 示例: http://10.0.129.11:8081/repository/maven-releases/",
            font=ctk.CTkFont(size=11),
            text_color=("gray50", "gray40")
        )
        example_label.pack(pady=(0, 20), padx=20, anchor="w")
        
    def create_action_buttons(self):
        """创建操作按钮区域"""
        # 按钮框架
        button_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        button_frame.pack(fill="x", pady=(0, 20))
        
        # 按钮容器
        button_container = ctk.CTkFrame(button_frame, fg_color="transparent")
        button_container.pack(expand=True)
        
        # 上传按钮
        self.upload_button = ctk.CTkButton(
            button_container,
            text="🚀 上传到Maven仓库",
            command=self.upload_to_maven,
            width=200,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#2b5a87",
            hover_color="#1e3f5f"
        )
        self.upload_button.pack(side="left", padx=(0, 15))
        
        # 清空按钮
        clear_button = ctk.CTkButton(
            button_container,
            text="🗑️ 清空",
            command=self.clear_fields,
            width=120,
            height=50,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#d73527",
            hover_color="#b02a20"
        )
        clear_button.pack(side="left", padx=(0, 15))
        
        # 完全清空按钮
        clear_all_button = ctk.CTkButton(
            button_container,
            text="🔄 完全清空",
            command=self.clear_all_fields,
            width=120,
            height=50,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#6c757d",
            hover_color="#545b62"
        )
        clear_all_button.pack(side="left")
        
    def create_progress_section(self):
        """创建进度条区域"""
        # 进度条框架
        progress_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        progress_frame.pack(fill="x", pady=(0, 20))
        
        # 进度条
        self.progress_bar = ctk.CTkProgressBar(
            progress_frame,
            width=400,
            height=20,
            corner_radius=10
        )
        self.progress_bar.pack(pady=10)
        self.progress_bar.set(0)
        
        # 进度文本
        self.progress_label = ctk.CTkLabel(
            progress_frame,
            text="就绪",
            font=ctk.CTkFont(size=12),
            text_color=("gray50", "gray40")
        )
        self.progress_label.pack()
        
    def create_log_section(self):
        """创建日志区域"""
        # 日志框架
        log_frame = ctk.CTkFrame(self.main_frame, corner_radius=10)
        log_frame.pack(fill="both", expand=True, pady=(0, 20))
        
        # 日志标题
        log_title = ctk.CTkLabel(
            log_frame,
            text="📋 执行日志",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        log_title.pack(pady=(20, 15), padx=20, anchor="w")
        
        # 日志文本框
        self.log_text = ctk.CTkTextbox(
            log_frame,
            height=200,
            font=ctk.CTkFont(size=11, family="Consolas"),
            corner_radius=8
        )
        self.log_text.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # 设置日志文本的初始内容
        self.log_text.insert("1.0", "🚀 Maven JAR包上传工具启动\n")
        self.log_text.insert("end", "⏳ 正在初始化，请稍候...\n")
        self.log_text.insert("end", "\n")
        self.log_text.insert("end", "✨ 功能特性:\n")
        self.log_text.insert("end", "• 🎯 支持上传JAR包和POM文件到私有Maven仓库\n")
        self.log_text.insert("end", "• 🔍 智能检测Maven环境配置\n")
        self.log_text.insert("end", "• 📊 实时显示上传进度和结果\n")
        self.log_text.insert("end", "• 🛠️ 支持手动选择Maven路径\n")
        self.log_text.insert("end", "• 🎨 现代化用户界面\n")
        self.log_text.insert("end", "\n")
        
    def center_window(self):
        """窗口居中显示"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def auto_detect_maven(self):
        """启动时自动检测Maven"""
        # 延迟执行，确保界面完全加载后再开始检测
        self.root.after(100, self._perform_maven_detection)
        
    def _perform_maven_detection(self):
        """执行Maven检测"""
        # 清空初始内容，显示检测过程
        self.log_text.delete("1.0", "end")
        
        self.log_message("=" * 60)
        self.log_message("🚀 Maven JAR包上传工具启动")
        self.log_message("=" * 60)
        self.log_message("")
        self.log_message("🔍 正在自动检测Maven配置...")
        self.maven_status_label.configure(text="状态: 检测中...", text_color="blue")
        self.root.update_idletasks()
        
        # 显示环境变量信息
        self.log_message("📋 步骤1: 检查环境变量配置")
        maven_home = os.getenv('MAVEN_HOME')
        if maven_home:
            self.log_message(f"  ✅ 检测到MAVEN_HOME环境变量: {maven_home}")
        else:
            self.log_message("  ❌ 未检测到MAVEN_HOME环境变量")
        
        self.log_message("")
        self.log_message("🔍 步骤2: 查找Maven可执行文件")
        mvn_executable = self.find_maven_executable()
        
        if mvn_executable:
            self.maven_path.set(mvn_executable)
            self.maven_status_label.configure(text="状态: ✅ 已找到Maven", text_color="green")
            self.log_message(f"  ✅ 成功找到Maven: {mvn_executable}")
            self.log_message("")
            self.log_message("🎉 检测完成！Maven配置正常")
            self.log_message("")
            self.log_message("📝 下一步操作:")
            self.log_message("1. 点击'选择JAR'按钮选择要上传的JAR文件")
            self.log_message("2. 程序会自动查找对应的POM文件")
            self.log_message("3. 输入Maven仓库URL")
            self.log_message("4. 点击'上传到Maven仓库'开始上传")
        else:
            self.maven_status_label.configure(text="状态: ❌ 未找到Maven", text_color="red")
            self.log_message("  ❌ 未找到Maven可执行文件")
            self.log_message("")
            self.log_message("⚠️ 检测失败！需要手动配置Maven")
            self.log_message("")
            self.log_message("🛠️ 解决方案:")
            self.log_message("1. 点击'手动选择'按钮手动指定Maven路径")
            self.log_message("2. 检查Maven环境变量配置")
            self.log_message("3. 确保Maven已正确安装")
            self.log_message("4. 常见Maven路径:")
            self.log_message("   - D:\\Maven\\apache-maven-3.9.10\\bin\\mvn.cmd")
            self.log_message("   - C:\\Program Files\\Apache\\maven\\bin\\mvn.cmd")
        
        self.log_message("")
        self.log_message("=" * 60)
        # 确保日志滚动到最新内容
        self.log_text.see("end")
        self.root.update_idletasks()
        
    def auto_detect_maven_manual(self):
        """手动触发Maven自动检测"""
        self.log_message("")
        self.log_message("=" * 50)
        self.log_message("🔄 手动触发Maven自动检测")
        self.log_message("=" * 50)
        self.log_message("")
        self.log_message("🔍 正在重新检测Maven配置...")
        self.maven_status_label.configure(text="状态: 检测中...", text_color="blue")
        self.root.update_idletasks()
        
        # 显示环境变量信息
        self.log_message("📋 步骤1: 检查环境变量配置")
        maven_home = os.getenv('MAVEN_HOME')
        if maven_home:
            self.log_message(f"  ✅ 检测到MAVEN_HOME环境变量: {maven_home}")
        else:
            self.log_message("  ❌ 未检测到MAVEN_HOME环境变量")
        
        self.log_message("")
        self.log_message("🔍 步骤2: 查找Maven可执行文件")
        mvn_executable = self.find_maven_executable()
        
        if mvn_executable:
            self.maven_path.set(mvn_executable)
            self.maven_status_label.configure(text="状态: ✅ 已找到Maven", text_color="green")
            self.log_message(f"  ✅ 成功找到Maven: {mvn_executable}")
            self.log_message("")
            self.log_message("🎉 检测完成！Maven配置正常")
        else:
            self.maven_status_label.configure(text="状态: ❌ 未找到Maven", text_color="red")
            self.log_message("  ❌ 未找到Maven可执行文件")
            self.log_message("")
            self.log_message("⚠️ 检测失败！请尝试手动选择Maven路径")
            self.log_message("")
            self.log_message("🛠️ 解决方案:")
            self.log_message("1. 点击'手动选择'按钮手动指定Maven路径")
            self.log_message("2. 检查Maven环境变量配置")
            self.log_message("3. 确保Maven已正确安装")
        
        self.log_message("")
        self.log_message("=" * 50)
        # 确保日志滚动到最新内容
        self.log_text.see("end")
        self.root.update_idletasks()
        
    def select_jar_file(self):
        """选择JAR文件"""
        file_path = filedialog.askopenfilename(
            title="选择JAR文件",
            filetypes=[("JAR files", "*.jar"), ("All files", "*.*")]
        )
        if file_path:
            self.jar_file_path.set(file_path)
            self.log_message(f"📁 已选择JAR文件: {file_path}")
            
            # 自动查找对应的POM文件
            self.auto_find_pom_file(file_path)
    
    def select_pom_file(self):
        """选择POM文件"""
        file_path = filedialog.askopenfilename(
            title="选择POM文件",
            filetypes=[("POM files", "*.pom"), ("All files", "*.*")]
        )
        if file_path:
            self.pom_file_path.set(file_path)
            self.log_message(f"📄 已选择POM文件: {file_path}")
    
    def select_maven_path(self):
        """选择Maven可执行文件"""
        file_path = filedialog.askopenfilename(
            title="选择Maven可执行文件",
            filetypes=[("Maven executable", "mvn.cmd;mvn.bat;mvn"), ("All files", "*.*")]
        )
        if file_path:
            self.maven_path.set(file_path)
            if os.path.exists(file_path):
                self.maven_status_label.configure(text="状态: ✅ 已选择Maven", text_color="green")
                self.log_message(f"✅ 已选择Maven路径: {file_path}")
            else:
                self.maven_status_label.configure(text="状态: ❌ 路径不存在", text_color="red")
                self.log_message(f"❌ 选择的Maven路径不存在: {file_path}")
    
    def auto_find_pom_file(self, jar_path):
        """自动查找对应的POM文件"""
        jar_file = Path(jar_path)
        pom_file = jar_file.with_suffix('.pom')
        
        if pom_file.exists():
            self.pom_file_path.set(str(pom_file))
            self.log_message(f"🔍 自动找到POM文件: {pom_file}")
        else:
            self.log_message("⚠️ 未找到对应的POM文件，请手动选择")
    
    def clear_fields(self):
        """清空所有字段（保留Maven路径）"""
        self.jar_file_path.set("")
        self.pom_file_path.set("")
        self.repository_id.set("releases")
        self.repository_url.set("")
        self.log_text.delete("1.0", "end")
        self.log_message("🗑️ 已清空文件选择和仓库配置（保留Maven路径）")
        self.progress_bar.set(0)
        self.progress_label.configure(text="就绪")
    
    def clear_all_fields(self):
        """完全清空所有字段（包括Maven路径）"""
        result = messagebox.askyesno("确认清空", 
            "确定要完全清空所有字段吗？\n\n"
            "这将包括：\n"
            "• JAR文件路径\n"
            "• POM文件路径\n"
            "• Maven路径\n"
            "• 仓库配置\n\n"
            "点击'是'继续，点击'否'取消")
        
        if result:
            self.jar_file_path.set("")
            self.pom_file_path.set("")
            self.maven_path.set("")
            self.repository_id.set("releases")
            self.repository_url.set("")
            self.log_text.delete("1.0", "end")
            self.log_message("🗑️ 已完全清空所有字段")
            self.log_message("请重新选择Maven路径或等待自动检测")
            self.progress_bar.set(0)
            self.progress_label.configure(text="就绪")
    
    def log_message(self, message):
        """在日志区域添加消息"""
        self.log_text.insert("end", f"{message}\n")
        self.log_text.see("end")
        self.root.update_idletasks()
        
        # 强制刷新界面，确保日志立即显示
        self.log_text.update_idletasks()
    
    def validate_inputs(self):
        """验证输入参数"""
        if not self.jar_file_path.get():
            messagebox.showerror("错误", "请选择JAR文件")
            return False
        
        if not self.pom_file_path.get():
            messagebox.showerror("错误", "请选择POM文件")
            return False
        
        if not self.repository_id.get():
            messagebox.showerror("错误", "请输入仓库ID")
            return False
        
        if not self.repository_url.get():
            messagebox.showerror("错误", "请输入仓库URL")
            return False
        
        # 检查文件是否存在
        if not os.path.exists(self.jar_file_path.get()):
            messagebox.showerror("错误", "JAR文件不存在")
            return False
        
        if not os.path.exists(self.pom_file_path.get()):
            messagebox.showerror("错误", "POM文件不存在")
            return False
        
        return True
    
    def find_maven_executable(self):
        """查找Maven可执行文件"""
        import shutil
        
        self.log_message("🔍 正在查找Maven可执行文件...")
        
        # 如果用户手动指定了Maven路径，优先使用
        if self.maven_path.get():
            maven_path = self.maven_path.get()
            self.log_message(f"使用用户指定的Maven路径: {maven_path}")
            if os.path.exists(maven_path):
                self.log_message(f"✅ 找到Maven: {maven_path}")
                return maven_path
            else:
                self.log_message(f"❌ 指定的Maven路径不存在: {maven_path}")
        
        # 1. 检查环境变量中的MAVEN_HOME（优先级最高）
        maven_home = os.getenv('MAVEN_HOME')
        if maven_home:
            self.log_message(f"检测到MAVEN_HOME环境变量: {maven_home}")
            mvn_path = os.path.join(maven_home, 'bin', 'mvn.cmd')
            if os.path.exists(mvn_path):
                self.log_message(f"✅ 通过MAVEN_HOME找到Maven: {mvn_path}")
                return mvn_path
            else:
                self.log_message(f"❌ MAVEN_HOME路径下未找到mvn.cmd: {mvn_path}")
        
        # 2. 检查PATH中的mvn命令
        self.log_message("检查PATH环境变量中的mvn命令...")
        mvn_path = shutil.which("mvn")
        if mvn_path:
            self.log_message(f"✅ 通过PATH找到Maven: {mvn_path}")
            return mvn_path
        else:
            self.log_message("❌ PATH中未找到mvn命令")
        
        # 3. 检查常见的Maven安装目录
        self.log_message("检查常见的Maven安装目录...")
        common_maven_paths = [
            r"C:\Program Files\Apache\maven\bin\mvn.cmd",
            r"C:\Program Files (x86)\Apache\maven\bin\mvn.cmd",
            r"C:\apache-maven\bin\mvn.cmd",
            r"C:\maven\bin\mvn.cmd",
            r"D:\apache-maven\bin\mvn.cmd",
            r"D:\maven\bin\mvn.cmd",
            r"D:\Maven\bin\mvn.cmd",
            r"C:\Users\{}\apache-maven\bin\mvn.cmd".format(os.getenv('USERNAME', '')),
            r"C:\Users\{}\maven\bin\mvn.cmd".format(os.getenv('USERNAME', '')),
        ]
        
        for path in common_maven_paths:
            self.log_message(f"检查: {path}")
            if os.path.exists(path):
                self.log_message(f"✅ 在常见目录找到Maven: {path}")
                return path
            else:
                self.log_message(f"❌ 不存在")
        
        self.log_message("❌ 未找到Maven可执行文件")
        return None

    def upload_to_maven(self):
        """执行Maven上传"""
        if not self.validate_inputs():
            return
        
        if self.is_uploading:
            messagebox.showwarning("警告", "正在上传中，请稍候...")
            return
        
        # 禁用上传按钮，显示进度条
        self.upload_button.configure(state='disabled', text="⏳ 上传中...")
        self.progress_bar.set(0)
        self.progress_label.configure(text="准备上传...")
        self.is_uploading = True
        
        # 在新线程中执行上传
        upload_thread = threading.Thread(target=self._perform_upload)
        upload_thread.daemon = True
        upload_thread.start()
        
    def _perform_upload(self):
        """执行上传操作"""
        try:
            # 查找Maven可执行文件
            mvn_executable = self.find_maven_executable()
            if not mvn_executable:
                self.log_message("❌ 错误: 未找到Maven可执行文件")
                self.log_message("")
                self.log_message("🛠️ 解决方案:")
                self.log_message("1. 点击'手动选择'按钮手动指定Maven路径")
                self.log_message("2. 检查Maven环境变量配置:")
                self.log_message("   - MAVEN_HOME: " + str(os.getenv('MAVEN_HOME', '未设置')))
                self.log_message("   - PATH中是否包含: %MAVEN_HOME%\\bin")
                self.log_message("3. 常见Maven安装路径:")
                self.log_message("   - D:\\Maven\\bin\\mvn.cmd")
                self.log_message("   - C:\\Program Files\\Apache\\maven\\bin\\mvn.cmd")
                self.log_message("   - C:\\apache-maven\\bin\\mvn.cmd")
                
                # 提供选择Maven的选项
                self.root.after(0, lambda: messagebox.askyesno("Maven未找到", 
                    "未找到Maven可执行文件。\n\n"
                    "是否现在选择Maven路径？\n\n"
                    "点击'是'选择Maven路径\n"
                    "点击'否'取消上传"))
                
                return
            
            self.log_message(f"✅ 找到Maven可执行文件: {mvn_executable}")
            
            # 构建Maven命令
            maven_cmd = [
                mvn_executable, "deploy:deploy-file",
                f"-Dfile={self.jar_file_path.get()}",
                f"-DpomFile={self.pom_file_path.get()}",
                f"-DrepositoryId={self.repository_id.get()}",
                f"-Durl={self.repository_url.get()}"
            ]
            
            self.log_message("🚀 开始执行Maven上传命令...")
            self.log_message(f"命令: {' '.join(maven_cmd)}")
            
            # 更新进度
            self.root.after(0, lambda: self.progress_bar.set(0.3))
            self.root.after(0, lambda: self.progress_label.configure(text="正在执行Maven命令..."))
            
            # 执行Maven命令
            process = subprocess.Popen(
                maven_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding='utf-8',
                errors='replace',
                shell=True  # 在Windows上使用shell=True
            )
            
            # 实时显示输出
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    self.log_message(output.strip())
                    # 更新进度条
                    self.root.after(0, lambda: self.progress_bar.set(0.7))
            
            # 等待进程完成
            return_code = process.wait()
            
            # 更新进度条
            self.root.after(0, lambda: self.progress_bar.set(1.0))
            
            if return_code == 0:
                self.log_message("🎉 上传成功！")
                self.root.after(0, lambda: self.progress_label.configure(text="上传成功！"))
                self.root.after(0, lambda: messagebox.showinfo("成功", "JAR包已成功上传到Maven仓库！"))
            else:
                self.log_message("❌ 上传失败！")
                self.root.after(0, lambda: self.progress_label.configure(text="上传失败"))
                self.root.after(0, lambda: messagebox.showerror("错误", "上传失败，请检查日志信息"))
                
        except Exception as e:
            self.log_message(f"❌ 发生错误: {str(e)}")
            self.root.after(0, lambda: self.progress_label.configure(text="发生错误"))
            self.root.after(0, lambda: messagebox.showerror("错误", f"发生错误: {str(e)}"))
        finally:
            # 恢复界面状态
            self.root.after(0, lambda: self.upload_button.configure(state='normal', text="🚀 上传到Maven仓库"))
            self.root.after(0, lambda: self.progress_bar.set(0))
            self.root.after(0, lambda: self.progress_label.configure(text="就绪"))
            self.is_uploading = False

    def run(self):
        """运行应用"""
        self.root.mainloop()


def main():
    """主函数"""
    try:
        app = ModernMavenUploader()
        app.run()
    except ImportError as e:
        if "customtkinter" in str(e):
            print("❌ 错误: 缺少依赖库 customtkinter")
            print("")
            print("📦 请安装依赖库:")
            print("pip install customtkinter pillow")
            print("")
            print("或者运行:")
            print("pip install -r requirements.txt")
        else:
            print(f"❌ 导入错误: {e}")
    except Exception as e:
        print(f"❌ 启动错误: {e}")


if __name__ == "__main__":
    main()
