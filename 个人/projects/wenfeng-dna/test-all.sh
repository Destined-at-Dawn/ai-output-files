#!/bin/bash
echo "=== 文风DNA技能测试 ===\n"

echo "1. 列出词汇库:"
node dist/index.js list-vocab
echo ""

echo "2. 分析文本:"
node dist/index.js analyze -t "我试过很多护肤方法，效果真的惊艳。如果你是油皮，这个方法绝对适合你。" --domain SK
echo ""

echo "3. 检测领域:"
node dist/index.js detect-domain -t "烟酰胺的透皮吸收率是传统成分的3倍，但真正有效的是坚持使用。" --top 2
echo ""

echo "4. 对比两个文本:"
echo "这是文本1" > t1.txt
echo "这是文本2" > t2.txt
node dist/index.js compare t1.txt t2.txt
rm t1.txt t2.txt
echo ""

echo "=== 测试完成 ==="
