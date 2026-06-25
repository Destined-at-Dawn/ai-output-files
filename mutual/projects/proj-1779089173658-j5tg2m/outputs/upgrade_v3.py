"""lilanyuan-cn-v2 → v3：基于实际 JS 渲染结构的精确替换"""
import base64, io, os
from PIL import Image

OUT_DIR = r"E:\ai产出文件\牛马\mutual\mutual\projects\proj-1779089173658-j5tg2m\outputs"
SRC = f"{OUT_DIR}\\lilanyuan-cn-v2.html"
DST = f"{OUT_DIR}\\lilanyuan-cn-v3.html"

with open(SRC, encoding="utf-8") as f:
    html = f.read()

# ============================================================
# 编码图片
# ============================================================
def encode_poster():
    img = Image.open(r"E:\personal_information\海报\OPC海报png.png").convert("RGB")
    w, h = img.size
    if w > 800:
        ratio = 800 / w
        img = img.resize((800, int(h * ratio)), Image.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=75)
    return base64.b64encode(buf.getvalue()).decode()

def encode_qr():
    with open(r"E:\personal_information\二维码\小黎的微信.jpg", "rb") as f:
        return base64.b64encode(f.read()).decode()

poster_b64 = encode_poster()
qr_b64 = encode_qr()
print(f"Poster base64: {len(poster_b64)//1024} KB, QR base64: {len(qr_b64)//1024} KB")

# ============================================================
# 改动 1：Track A 卡片 — 去掉"常州电网 保底目标"
# ============================================================
old_track_metrics = """              <li><b>皮赛仪器</b><span>AI 流程工程师</span></li>
              <li><b>GPA 3.9</b><span>电气工程专精</span></li>
              <li><b>常州电网</b><span>保底目标</span></li>"""
new_track_metrics = """              <li><b>皮赛仪器</b><span>AI 流程工程师</span></li>
              <li><b>GPA 3.9</b><span>电气工程专精</span></li>
              <li><b>Loop Engineering</b><span>写循环 · 工业落地</span></li>"""
html = html.replace(old_track_metrics, new_track_metrics)
print("✓ 改动1: Track A 卡片指标")

# ============================================================
# 改动 2：Section heading — 去掉"电网保底"
# ============================================================
html = html.replace(
    "从电网保底到具身智能前沿，从企业 AI 改造到个人知识系统——这里只保留能证明执行力的证据。",
    "从企业 AI 改造到具身智能前沿，从个人知识系统到社群互助——这里只保留能证明执行力的证据。"
)
print("✓ 改动2: 证据区副标题")

# ============================================================
# 改动 3：工业流程 JS detail modal — 去掉"常州电网市局为保底目标"
# ============================================================
html = html.replace(
    "同时以上海电力大学电气工程专业（GPA 3.9）为基础，常州电网市局为保底目标。",
    "以上海电力大学电气工程专业（GPA 3.9）为学术底座，将 Loop Engineering 从个人效率工具升级为工业级自动化系统。"
)
print("✓ 改动3: 工业流程详情弹窗")

# ============================================================
# 改动 4：具身智能 proof card — 补充蓓伟完整描述
# ============================================================
html = html.replace(
    "<p>在威裕新能源旗下蓓伟机器人参与底盘控制与 AI 工作流编排，由企业董事长直接面试通过。企业拥有 31 项专利、18 项商标。</p>",
    "<p>在威裕新能源旗下蓓伟机器人参与具身智能研发，由企业董事长直接面试通过。企业注册资本 1500 万，31 项专利，18 项商标。这不仅是实习——这是我从电气工程跨越到具身智能前沿的关键桥梁。</p>"
)
print("✓ 改动4: 蓓伟实习证据卡")

# ============================================================
# 改动 5：具身智能 detail modal — 补充完整描述
# ============================================================
html = html.replace(
    "在威裕新能源旗下蓓伟机器人科技（上海）有限公司参与具身智能研发。</p><ul><li>由企业董事长直接面试，获具身智能（Embodied AI）方向实习机会。</li>",
    "在威裕新能源旗下蓓伟机器人科技（上海）有限公司参与具身智能研发。企业注册资本 1500 万，31 项专利，18 项商标。这不仅是实习——这是我从电气工程跨越到具身智能前沿的关键桥梁。</p><ul><li>由企业董事长直接面试，获具身智能（Embodied AI）方向实习机会。</li>"
)
print("✓ 改动5: 具身智能详情弹窗")

# ============================================================
# 改动 6：OPC 海报图片嵌入（替换外部引用）
# ============================================================
html = html.replace(
    'src="assets/xiaoli-opc-poster.png"',
    f'src="data:image/jpeg;base64,{poster_b64}"'
)
print("✓ 改动6: OPC 海报 base64 嵌入")

# ============================================================
# 改动 7：微信二维码图片嵌入（替换外部引用）
# ============================================================
html = html.replace(
    'src="assets/xiaoli-wechat-qr.jpg"',
    f'src="data:image/jpeg;base64,{qr_b64}"'
)
print("✓ 改动7: 微信二维码 base64 嵌入")

# ============================================================
# 改动 8：联系入口区域 — 加入双线叙事 + 社群 + 7-9月开班 + 微信号
# ============================================================
old_contact_heading = """            <h2 id="contact-title">加我微信，说明你想聊哪件事。</h2>
          </div>
          <p>这里放个人微信，不放过期社群码。备注越具体，我越容易判断怎么接住你的需求。</p>"""

new_contact_heading = """            <h2 id="contact-title">两条线，一个社群，一个入口。</h2>
          </div>
          <p><strong>第一条线（个人发展）</strong>：我把 Loop Engineering、具身智能、电气化三条技术线拧成一条面向未来国家发展的科技赛道。<strong>第二条线（互助社群）</strong>：我把踩过的坑总结成避坑指南——AI 工程、OPC 实战、大学迷茫期，都可以来聊。两条线在社群里交汇：一边小白入门指南，一边老手交流技术。</p>"""

html = html.replace(old_contact_heading, new_contact_heading)
print("✓ 改动8: 联系区域标题+双线叙事")

# ============================================================
# 改动 9：在 contact-notes 区域加入社群信息 + 7-9月开班 + 微信号
# ============================================================
old_contact_notes = """            <div class="contact-notes">
              <article class="contact-note glow-card">
                <b>我的飞书知识库</b>
                <span>这是我持续更新的个人知识大脑，包含 AI 工程、电气笔记、竞赛 SOP、百大认知等。👉 <a href="https://vcnogbywj044.feishu.cn/wiki/G49awLm91i2ZObkWXBmcLnmFncf" target="_blank" rel="noopener noreferrer">点击访问飞书文档</a></span>
              </article>
              <article class="contact-note glow-card">
                <b>想做付费咨询</b>
                <span>备注"咨询 + 具体问题"。我会先判断适合轻量解答、系统诊断，还是暂时给免费资料。</span>
              </article>
              <article class="contact-note glow-card">
                <b>想聊合作（企业 / 工业 AI）</b>
                <span>备注"合作 + 企业名/场景"。适合聊工业 AI 流程改造、电气设备智能化、企业 AI 培训。</span>
              </article>
            </div>"""

new_contact_notes = f"""            <div class="contact-notes">
              <article class="contact-note glow-card">
                <b>📚 飞书知识库（持续更新）</b>
                <span>AI 工程、电气笔记、竞赛 SOP、百大认知——我的个人知识大脑。👉 <a href="https://vcnogbywj044.feishu.cn/wiki/G49awLm91i2ZObkWXBmcLnmFncf" target="_blank" rel="noopener noreferrer">点击访问飞书文档</a></span>
              </article>
              <article class="contact-note glow-card">
                <b>🔰 小白入门指南</b>
                <span>不管你是想学 AI 工程、用 AI 辅助 OPC，还是大学迷茫不知道怎么开始——先看这份指南。👉 <a href="https://vcnogbywj044.feishu.cn/wiki/V6Mpwjv8IiCuMVkslmGctxWinFg" target="_blank" rel="noopener noreferrer">点击查看入门指南</a></span>
              </article>
              <article class="contact-note glow-card">
                <b>📅 2026 年 7-9 月 · 大学生 AI 实战营</b>
                <span>教大学生快速使用 AI 帮自己搞定：日常学习、打竞赛、写论文、线上社交。从"知道 AI"到"用 AI 拿结果"。名额有限，备注"实战营"提前锁定。</span>
              </article>
              <article class="contact-note glow-card">
                <b>💬 微信号：a3061918593</b>
                <span>扫码添加或直接搜索微信号。建议备注来意，不要只发"你好"。聊 AI 工程、具身智能、电气求职、OPC、咨询合作都可以。</span>
              </article>
              <article class="contact-note glow-card">
                <b>想做付费咨询</b>
                <span>备注"咨询 + 具体问题"。我会先判断适合轻量解答、系统诊断，还是暂时给免费资料。</span>
              </article>
              <article class="contact-note glow-card">
                <b>想聊合作（企业 / 工业 AI）</b>
                <span>备注"合作 + 企业名/场景"。适合聊工业 AI 流程改造、电气设备智能化、企业 AI 培训。</span>
              </article>
            </div>"""

html = html.replace(old_contact_notes, new_contact_notes)
print("✓ 改动9: 社群+实战营+微信号")

# ============================================================
# 改动 10：Hero lead 微调 — 加入"三条线拧成一条"
# ============================================================
html = html.replace(
    "我把工程经验沉淀为可复用的 SOP 和 AI 循环——不写步骤，写循环；不给指令，给目标。",
    "我把 Loop Engineering、具身智能、电气化三条技术线拧成一条赛道——不写步骤，写循环；不给指令，给目标。"
)
print("✓ 改动10: Hero lead 文案")

# ============================================================
# 改动 11：联系区高手交流备注 — 加入更多方向
# ============================================================
html = html.replace(
    'data-copy="你好李兰源，我想和你聊工业 AI 流程改造 / 具身智能 / 电网求职。我的背景是：___，想解决的问题是：___。"',
    'data-copy="你好李兰源，我想和你聊 Loop Engineering / 具身智能 / 电气化 / 电网求职 / AI 实战营。我的背景是：___，想解决的问题是：___。"'
)
print("✓ 改动11: 高手交流备注")

# ============================================================
# 写入 v3
# ============================================================
with open(DST, "w", encoding="utf-8") as f:
    f.write(html)

print(f"\n✅ v3 已生成: {DST}")
print(f"   文件大小: {os.path.getsize(DST) / 1024:.1f} KB")

# 验证关键改动
for check, label in [
    ("data:image/jpeg;base64,", "图片 base64 嵌入"),
    ("两条线", "双线叙事"),
    ("实战营", "7-9月开班"),
    ("a3061918593", "微信号"),
    ("小白入门指南", "小白指南链接"),
    ("Loop Engineering", "Loop Engineering"),
]:
    found = check in html
    status = "✅" if found else "❌"
    print(f"   {status} {label}: {found}")

# 验证"保底"已清除
count = html.count("保底")
print(f"   {'✅' if count == 0 else '❌'} '保底'出现次数: {count}")
