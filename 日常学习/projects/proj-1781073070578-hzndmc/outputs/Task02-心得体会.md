# Task02：激活函数与位置编码 — 学习心得

## 踩的坑

SwiGLU 最大的坑是参数对齐——加了门控路径后中间维度不能随便选，必须是 8d/3 再对齐 256 倍数，否则 Tensor Core 效率直接掉。RoPE 的坑更深：复数乘法必须用 FP32，我一开始用 FP16 跑，三角函数中间值直接溢出，loss 飞掉。查了 LLaMA 和 Qwen 源码才发现全是从 float() 强转的。

## 查的资料

SwiGLU 看了 Noam Shazeer 原始论文和 LLaMA 源码的 intermediate_size 计算；RoPE 看了苏剑林的博客和 Qwen 的动态 NTK 实现。

## 感悟

不是越精确越好，而是够用的精度 + 够大的范围才是工程最优解。SwiGLU 的矩阵融合、RoPE 的 FP32 强制，本质都是在精度和带宽之间找平衡。

## 以后应用

这两个组件是 LLaMA/Qwen/Mistral 的标配，做模型微调、推理优化、甚至自己搭小模型都会用到。对以后做 FPGA 加速器设计也有启发——RoPE 的旋转可以用 CORDIC 硬件实现，SwiGLU 的融合矩阵可以用双端口 BRAM。
