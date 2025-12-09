# Maven JAR包上传工具

一个现代化的图形界面工具，用于将本地JAR包和POM文件快速上传到私有Maven仓库。

## 功能特性

- 现代化的用户界面设计
- 智能检测Maven环境配置
- 支持自动查找对应的POM文件
- 实时显示上传进度和日志
- 支持深色/浅色主题切换
- 一键上传到Maven仓库

## 快速开始

### 方式1：直接使用exe文件（推荐）

1. 打开 `dist` 目录
2. 双击运行 `Maven上传工具.exe`
3. 无需安装Python环境，开箱即用

### 方式2：运行Python源代码

#### 环境要求
- Python 3.7+
- Maven 3.6+

#### 安装依赖
```bash
pip install -r requirements.txt
```

#### 运行程序
```bash
python maven_uploader_modern.py
```

## 使用说明

1. **选择文件**
   - 点击"选择JAR"按钮选择要上传的JAR文件
   - 程序会自动查找同名的POM文件，或手动选择POM文件

2. **配置Maven**
   - 程序启动时会自动检测Maven环境
   - 如果检测失败，可点击"手动选择"指定Maven路径
   - 或点击"自动检测"重新检测

3. **配置仓库**
   - **仓库ID**: 输入Maven仓库ID（默认：releases）
   - **仓库URL**: 输入Maven仓库URL
   - 示例: `http://10.0.129.11:8081/repository/maven-releases/`

4. **开始上传**
   - 点击"上传到Maven仓库"按钮
   - 在日志区域查看上传进度和结果

## 项目文件说明

```
pythontool/
├── maven_uploader_modern.py   # 主程序源代码
├── requirements.txt            # Python依赖列表
├── README.md                   # 项目说明文档
├── dist/                       # 可执行文件目录
│   └── Maven上传工具.exe      # 打包好的exe文件
└── mqtool/                     # 其他工具（独立项目）
```

## 依赖库

- **customtkinter** (>=5.2.0) - 现代化UI组件库
- **pillow** (>=9.0.0) - 图像处理库

## 打包exe文件

如果需要重新打包exe文件：

```bash
# 安装PyInstaller
pip install pyinstaller

# 打包为单文件exe
python -m PyInstaller --onefile --windowed --name "Maven上传工具" --clean maven_uploader_modern.py
```

打包后的exe文件位于 `dist/` 目录。

## Maven环境配置

### 自动检测

程序会按以下顺序自动查找Maven：
1. 检查 `MAVEN_HOME` 环境变量
2. 检查 `PATH` 环境变量中的mvn命令
3. 检查常见的Maven安装目录

### 手动配置

如果自动检测失败：
1. 点击"手动选择"按钮
2. 选择Maven可执行文件（如：`D:\Maven\bin\mvn.cmd`）

### 环境变量设置

**Windows:**
```bash
set MAVEN_HOME=D:\Maven\apache-maven-3.9.10
set PATH=%PATH%;%MAVEN_HOME%\bin
```

**Linux/Mac:**
```bash
export MAVEN_HOME=/usr/local/apache-maven
export PATH=$PATH:$MAVEN_HOME/bin
```

## 故障排除

### Maven未找到

**问题**: 程序提示"未找到Maven可执行文件"

**解决方案**:
1. 确保Maven已正确安装
2. 配置 `MAVEN_HOME` 环境变量
3. 使用"手动选择"功能指定Maven路径

### 上传失败

**问题**: 上传时报错

**解决方案**:
1. 检查Maven仓库URL是否正确
2. 确认网络连接正常
3. 验证仓库ID配置正确
4. 查看日志区域的详细错误信息

### 依赖库错误

**问题**: `ImportError: No module named 'customtkinter'`

**解决方案**:
```bash
pip install customtkinter pillow
```

## 技术实现

- **GUI框架**: CustomTkinter（现代化UI）
- **Maven集成**: subprocess调用Maven命令
- **文件处理**: pathlib和os模块
- **打包工具**: PyInstaller

## 执行的Maven命令示例

```bash
mvn deploy:deploy-file \
  -Dfile=path/to/artifact.jar \
  -DpomFile=path/to/artifact.pom \
  -DrepositoryId=releases \
  -Durl=http://10.0.129.11:8081/repository/maven-releases/
```

## 许可证

MIT License

## 更新日志

### v2.0.0 (现代化版本)
- 全新的现代化用户界面
- 智能Maven环境检测
- 实时进度显示
- 改进的用户体验
- 支持打包为exe文件

---

**享受现代化的Maven上传体验！**
