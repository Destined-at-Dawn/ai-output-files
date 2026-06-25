import os
import shutil

def safe_copy(src, dst):
    if not os.path.exists(src):
        print(f"Source not found: {src}")
        return
    if os.path.isdir(src):
        if os.path.exists(dst):
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
        print(f"Copied directory: {src} -> {dst}")
    else:
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)
        print(f"Copied file: {src} -> {dst}")

# 定义同步任务
tasks = [
    # A 类核心资产
    (r"E:\ai产出文件\牛马\创作\创作\projects\20260609-小黎个人网站", r"F:\work\网页设计\A类-核心资产\20260609-小黎个人网站"),
    (r"E:\ai产出文件\牛马\创作\创作\projects\20260521-AI创作与视觉设计\outputs\web-design-kit", r"F:\work\网页设计\A类-核心资产\web-design-kit"),
    (r"E:\ai产出文件\牛马\创作\创作\projects\20260521-AI创作与视觉设计\outputs\website_materials", r"F:\work\网页设计\A类-核心资产\website_materials"),

    # B 类参考素材
    (r"E:\ai产出文件\牛马\html", r"F:\work\网页设计\B类-参考素材\通用HTML样板"),
    (r"E:\ai产出文件\牛马\创作\创作\projects\20260425-内容创作系统\讲座HTML", r"F:\work\网页设计\B类-参考素材\讲座HTML"),
    (r"E:\ai产出文件\牛马\创作\创作\projects\20260425-内容创作系统\社群运营\html", r"F:\work\网页设计\B类-参考素材\社群运营样板"),
    (r"E:\ai产出文件\牛马\创作\创作\讲座\html_output", r"F:\work\网页设计\B类-参考素材\讲座渲染样板"),

    # 提取 SOP
    (r"F:\work\网页设计\A类-核心资产\web-design-kit\CLAUDE-网页设计.md", r"F:\work\网页设计\SOPs\CLAUDE-网页设计.md"),
    (r"F:\work\网页设计\A类-核心资产\website_materials\12_网站与HTML生成SOP.md", r"F:\work\网页设计\SOPs\12_网站与HTML生成SOP.md"),
    (r"F:\work\网页设计\A类-核心资产\website_materials\13_多Agent并行迭代代码与文档生产SOP.md", r"F:\work\网页设计\SOPs\13_多Agent并行迭代代码与文档生产SOP.md")
]

for src, dst in tasks:
    safe_copy(src, dst)
