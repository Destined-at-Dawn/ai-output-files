# TeXLive 安装配置指南（VS Code + LaTeX 科研写作环境）

> 基于四月学长视频教程，适配 2026 年最新版本
> 目标：离线编译 LaTeX 文档，配合 VS Code 实现代码↔PDF 双向定位

---

## 一、安装前检查

| 检查项 | 当前状态 |
|--------|---------|
| D 盘可用空间 | 75.8 GB ✅ |
| VS Code 已安装 | D:\Microsoft VS Code\bin\code ✅ |
| LaTeX Workshop 插件 | 待安装 |
| TeXLive | 待安装 |

---

## 二、安装 TeXLive

### 方法 A：清华镜像（推荐，速度快）

1. 打开清华大学镜像站：https://mirrors.tuna.tsinghua.edu.cn/CTAN/systems/texlive/Images/
2. 下载 `texlive.iso`（约 4.5 GB）
3. 双击 ISO 挂载（Win10/11 自带），或以管理员身份运行 `install-tl-windows.bat`
4. 在安装界面：
   - **安装根目录**：改盘符为 `D:\texlive\2026`（只改盘符 C→D，后面路径不动）
   - **取消勾选「安装 TeXworks 前端」**（用 VS Code 替代）
   - **高级 → 定制语言**：只选中英文（Chinese/English/Japanese），不选全语言（节省 2GB+）
   - 点击「安装」，等待 30-60 分钟

### 方法 B：命令行静默安装（适合无人值守）

```powershell
# 1. 挂载 ISO 到 E: 盘
# 2. 运行：
E:\install-tl-windows.bat --profile=texlive.profile
```

`texlive.profile` 内容：
```
selected_scheme scheme-basic
TEXDIR D:/texlive/2026
TEXMFCONFIG ~/.texlive2026/texmf-config
TEXMFHOME ~/texmf
TEXMFLOCAL D:/texlive/texmf-local
TEXMFSYSCONFIG D:/texlive/2026/texmf-config
TEXMFSYSVAR D:/texlive/2026/texmf-var
TEXMFVAR ~/.texlive2026/texmf-var
collection-langchinese 1
collection-langenglish 1
collection-latexextra 1
collection-mathscience 1
```

### 验证安装

```powershell
# 打开新的终端，输入：
xelatex --version
# 应该输出版本号
```

---

## 三、配置 VS Code

### 1. 安装 LaTeX Workshop 插件

1. VS Code → 扩展（Ctrl+Shift+X）
2. 搜索 `latex workshop`
3. 安装 **LaTeX Workshop**（作者：James Yu，下载量 1000 万+）
4. 不要装其他 LaTeX 相关插件（冲突）

### 2. 导入配置

将 `.vscode-settings.json` 的内容合并到你的 VS Code `settings.json`：

- **方法 1**：VS Code → Ctrl+Shift+P → `Preferences: Open User Settings (JSON)` → 粘贴
- **方法 2**：在科创目录创建 `.vscode/settings.json`，仅对该目录生效

---

## 四、编译测试

1. 在 VS Code 中打开 `research-writing-training.tex`
2. 按 `Ctrl+Alt+B` 编译
3. 左下角转圈 → 出现 ✅ = 编译成功
4. 点右上角绿色箭头查看 PDF

**如果编译失败**（常见情况）：

| 错误 | 原因 | 解决 |
|------|------|------|
| `ctexart.cls not found` | 缺少中文支持 | `tlmgr install ctex` |
| `biblatex.sty not found` | 缺少宏包 | `tlmgr install biblatex` |
| `amsmath.sty not found` | 缺少数学宏包 | `tlmgr install amsmath` |
| 路径含中文报错 | TeXLive 不支持中文路径 | 把 .tex 文件移到纯英文路径 |

---

## 五、不想装 TeXLive？用 Overleaf 立即开始

如果你现在就想编译 `research-writing-training.tex`：

1. 打开 https://www.overleaf.com（免费注册）
2. 新建项目 → 上传 `research-writing-training.tex` 和 `references.bib`
3. 编译器选 **XeLaTeX**
4. 点「重新编译」→ PDF 即刻生成

Overleaf 的好处：零安装、在线协作、模板丰富。缺点是网络依赖、免费版编译超时限制。
离线 VS Code + TeXLive 的好处：完全本地、AI 辅助（Copilot/Codex）、编译无限制。推荐长期使用组合：**本机写 → Overleaf 协作改 → 本机终稿**。

---

## 六、TeXLive 包管理速查

```powershell
# 搜索包
tlmgr search --global --name <关键词>

# 安装包
tlmgr install <包名>

# 列出已安装
tlmgr list --only-installed

# 更新全部包
tlmgr update --all --self
```

---

> 安装遇到问题？照视频里说的：找到四月学长帮解决。或者在 Overleaf 先写起来，环境慢慢配。
