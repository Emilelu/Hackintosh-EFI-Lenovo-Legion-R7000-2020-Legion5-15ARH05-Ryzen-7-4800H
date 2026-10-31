# 可选优化与增强

> 返回 [主 README](../README.md)

> Language: [English](./Optional.en.md) | 中文（本页）

## HiDPI

- `one-key-hidpi-mod`：仅兼容 Ventura 及以下。
- `BetterDisplay`：适配 Sonoma 及以上（激活工具：<https://macked.app/tools/betterdisplay.php>），运行时可能轻微卡顿。
- **区别于一键工具的手动开启显示器 HiDPI 教程**（远景帖）：<https://bbs.pcbeta.com/forum.php?mod=viewthread&tid=1950179>

## 常用脚本

- **黑果子必备常用脚本**（远景帖）：<https://bbs.pcbeta.com/viewthread-2076529-1-1.html>

## SwitchResX 注册信息

- Name：`Peter Gunn`
- Code：`0079FCB69A1708F8`

## 内建麦克风

内建麦克风通常已由 AppleALC 直接驱动（HDA 通道），可先直接测试录音是否正常。[AMDMicrophone-Continuity](https://github.com/hrx114514x/AMDMicrophone-Continuity) 是**另一种方案**：针对走 Renoir ACP/PDM 通道的数字麦克风（含 DMA 连续性修复）。若采用，注意：

- 必须安装到 `/Library/Extensions`，不支持经 OpenCore 注入（因此本 EFI 不内置）；
- 需允许加载不受信任的 kext（`csr-active-config=01000000`，降低系统安全性）；
- 已在 Ryzen 5 5500U + macOS 26.5.1 验证；本机麦克风是否走 ACP/PDM 通道需自行确认。

## macOS 26 动画掉帧

可尝试 [CompositorPacer](https://github.com/githubzijian/CompositorPacer)：通过一个不可见的 Metal 节拍窗口保持 WindowServer 合成路径活跃，改善部分 macOS 26 环境下的动画掉帧感。

## 虚拟机与 Docker（AMD-V）

[RyzenHV](https://github.com/OverlordDev/ryzen-hypervisor.framework) 用 kext 在 AMD-V（SVM）之上实现 `Hypervisor.framework` 接口。AMD 平台 `kern.hv_support` 恒为 0，Docker Desktop、Parallels、VirtualBox、`qemu -accel hvf` 因此都起不来；装上它，这些程序无需改动即可运行。**属实验性项目**，本 EFI 不内置，自行取用前注意：

- 需在 BIOS 中**开启 SVM**（本 EFI 的 BIOS 设置里 SVM 可关，装了 RyzenHV 这条即不再成立）；
- 先在**备用 EFI** 上试：kext 由 `./rhv kext --native` 写入 EFI，出问题改从不含该 kext 的 EFI 启动，或临时加 boot-arg `-rhv_off`；
- 作者仅在 Ryzen 7 5800H + Sequoia 15.8.1 上验证，本机 4800H 与 macOS 26 均未验证（macOS 26 下 Docker 可能还需放宽 AMFI）；
- 各虚拟机程序的可用程度差别很大，以项目 README 的支持矩阵为准（0.7.7：Docker Desktop 4.97.0 可用；Parallels 仅 26.5.0 build 57613；VirtualBox 7.x 实验性；VMware Fusion 尚不可用）。

## arm64 应用（Maclator）

[Maclator](https://github.com/linuxkid473/maclator) 是"反向 Rosetta"：把真正的 arm64 用户态（dyld 与 arm64e dyld 共享缓存，由你自行从 Apple 服务器下载）与 arm64 Mach-O 一起加载，用解释器 + x86-64 JIT 执行，系统调用交给 x86-64 宿主内核，Metal 调用可桥接到宿主 GPU。用途是让只发 arm64 的新应用在 x86-64 上还有一试的余地。属实验性研究项目，注意：

- 作者按 **Intel Mac** 设计，并在 Intel Core i5-4440 + macOS 26.7 上验证；本机是 AMD 平台，未验证（JIT 与 Metal 桥在本机能否工作需自测）；
- 需 macOS 26 宿主、Xcode 命令行工具与 Rust 工具链，约 10 GB 空闲磁盘，首次还要下载约 5.5 GB 的 arm64e dyld 共享缓存；
- 已跑通 arm64 命令行工具、小型 AppKit 应用、VS Code 与 Chromium（含 GPU 加速）；音频、多数 IOKit 硬件、沙盒应用与 `CAMetalLayer` 类应用尚不支持。
