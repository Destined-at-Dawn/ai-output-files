# 跨区教训：R16 落地过程中的编码问题

> 日期：2026-05-25

## 问题

Python 在 Windows 上处理中文路径时，print 输出会显示乱码（如 `����`），但实际文件操作是正确的。

## 原因

Windows cmd/terminal 的编码设置与 Python 默认编码不一致。

## 解决

- 文件写入使用 `encoding='utf-8'`
- 不依赖终端输出判断文件是否创建成功
- 使用 `os.path.exists()` 验证文件存在

## 退出判据

只要 `os.path.exists()` 返回 True 且文件内容正确，终端乱码不影响功能。
