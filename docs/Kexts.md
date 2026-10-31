# Kext 一览与维护须知

> 返回 [主 README](../README.md)

> Language: [English](./Kexts.en.md) | 中文（本页）

## 已集成 Kext

| 类别 | Kext | 版本 | 用途 / 适用版本 |
|:---|:---|:---|:---|
| 基础 | `Lilu` | 1.7.3 | 补丁引擎，所有插件的前置依赖 |
| | `VirtualSMC` | 1.3.9 | SMC 模拟（含 `SMCBatteryManager` 电池、`SMCLightSensor` 光线传感器） |
| | `SMCProcessorAMD` | 1.0.1 | VirtualSMC 插件，AMD CPU 传感器 |
| | `ForgedInvariant` | 1.5.0 | TSC 不变量修复 |
| | `AppleMCEReporterDisabler` | 1.2 | 禁用 MCE 报告，避免 AMD 平台 Kernel Panic |
| | `RestrictEvents` | 1.1.7 | 修复 CPU 名称显示等 |
| 核显 | `NootedRed` | 0.9.0 | Renoir 核显驱动（Mojave+） |
| | `BrightnessKeys` | 1.0.4 | 亮度快捷键 |
| 音频 | `AppleALC` | 1.9.8 | 声卡编解码（`alcid=101`） |
| | `SimpleHDA` | 1.0.0 | laobamac 出品，恢复 Tahoe 移除的 AppleHDA（MinKernel 25.0.0） |
| 有线网 | `RealtekRTL8111` | 3.0.0 | Realtek 网卡驱动 |
| 无线网 | `AirportItlwm`（9 个版本） | 2.3.0 / 2.4.0 | 按 macOS 版本自动匹配：≤ Sonoma 为官方 2.3.0，Sequoia/Tahoe 为 [laobamac](https://github.com/laobamac/itlwm/releases) 2.4.0，见 [Compatibility.md](./Compatibility.md#wi-fi-驱动矩阵) |
| 蓝牙 | `IntelBluetoothFirmware` / `IntelBTPatcher` | 2.5.2 | Intel 蓝牙固件与补丁（**emulatorchen fork**，勿用官方版） |
| | `IntelBluetoothInjector` | 2.5.2 | ≤ Big Sur（MaxKernel 20.99.99） |
| | `BlueToolFixup`（修复版） | 2.7.3 | Monterey+，含 AirPods 无声修复 ⚠️ 勿更新，见下文 |
| USB | `GenericUSBXHCI` | 1.3.0b2 | AMD XHCI 控制器驱动，Big Sur+ ⚠️ 修改版勿更新 |
| | `USBMap` | 1.1 | 预生成 USB 映射（全版本；思路来自 win10Q），默认 config 使用 |
| 存储 | `NVMeFix` | 1.1.4 | NVMe 电源管理与兼容性修复（见下文说明） |
| | `PC711ProbeForce` | 1.8.1 | 强制驱动 macOS 不支持的 NVMe（仅 11–15），默认启用，见下文 |
| | `CtlnaAHCIPort` / `SATA-unsupported` | 341.0.2 / 0.9.2 | SATA 控制器支持（Big Sur+ / Catalina 及以下） |
| 输入 | `VoodooPS2Controller` | 2.3.8 | PS/2 键盘 |
| | `VoodooI2C` + `VoodooI2CHID` | 2.9.1 | I2C 触摸板 |
| 其他 | `YogaSMC` | 1.5.3 | 联想 Fn 功能键 |
| | `ECEnabler` | 1.0.6 | 读取 EC 全量字段，修复电池状态 |
| | `Innie` | 1.3.1 | 将 PCIe 设备标记为内建 |
| | `AMFIPass` | 1.4.1 | 允许 OCLP-MOD 打补丁（Sequoia+ 配合 `-amfipassbeta`） |
| | `HoRNDIS` | 9.2 | Android USB 网络共享 |
| | `CpuTscSync` | 1.1.2 | TSC 同步备用方案（默认禁用，保留备用） |

## 不能跟随官方更新的 Kext

以下 kext 为修改版、第三方 fork 或本机定制产物，**更新后会失去修复 / 映射，直接导致功能异常**：

| Kext | 原因 |
|:---|:---|
| `BlueToolFixup.kext` 2.7.3 | 来自 [BlueToolFixup-FixA2DP](https://github.com/hexxyan/BlueToolFixup-FixA2DP) 的修复版，含 A2DP 时钟读取补丁；官方版无此修复，替换后 AirPods 将再度无声（配套 `-btlfxa2dpcheck` 也会失效） |
| `IntelBluetoothFirmware` / `IntelBTPatcher` / `IntelBluetoothInjector` 2.5.2 | 来自 [emulatorchen/IntelBluetoothFirmware](https://github.com/emulatorchen/IntelBluetoothFirmware) 第三方 fork，修复 HID 设备无法连接；官方版无此修复。更新只跟该 fork |
| `GenericUSBXHCI.kext` 1.3.0b2 | 为 Big Sur+ 修改的 AMD XHCI fork；官方 RehabMan 版无 AMD 适配 |
| `USBMap.kext` 1.1 | 由 USBToolBox 导出的**本机预生成映射**，不是上游发布物（思路来自 win10Q） |
| `CtlnaAHCIPort` / `SATA-unsupported` / `AppleMCEReporterDisabler` | 无官方 release 渠道的社区维护版，维持现状 |

## 可更新 Kext 的现状（2026-10 核对）

其余 kext 均可跟随官方更新。核对结果：

- **已是最新**：ForgedInvariant 1.5.0、YogaSMC 1.5.3、ECEnabler 1.0.6、Innie 1.3.1、SMCProcessorAMD 1.0.1、PC711ProbeForce 1.8.1、SimpleHDA 1.0.0、HoRNDIS 9.2（官方早已停更）、RealtekRTL8111 3.0.0、AirportItlwm ≤ Sonoma（= itlwm 官方 v2.3.0，最新 release）与 Sequoia/Tahoe（= laobamac 2.4.0）。
- **本地高于官方 release**（CI 构建版，无需降级）：Lilu 1.7.3（官方 1.7.2；dortania CI 同为 1.7.3）、NootedRed 0.9.0（官方 0.8.10）、RestrictEvents 1.1.7（官方 1.1.6）、BrightnessKeys 1.0.4（官方 1.0.3）、NVMeFix 1.1.4（官方 1.1.3）、VoodooPS2Controller 2.3.8。
- **本次已更新**：VirtualSMC 家族 1.3.8 → **1.3.9**（dortania CI b5c62c2）。
- **OpenCore 本体**：已更新至 **1.0.9 dev**（dortania 78d5ff8，2026-10-23），替换了 `BOOTx64.efi`、`OpenCore.efi`、`OpenRuntime.efi`、`OpenCanopy.efi`、`ResetNvramEntry.efi`；`HfsPlus.efi` 保持 OcBinaryData 版。两份 config 均通过 ocvalidate (1.0.9) 校验（1.0.9 起每个 Drivers 条目必填 `HideVerbose`，已补齐）。

更新方法：从各官方仓库 release 下载，整体替换 `EFI/OC/Kexts/<名称>.kext` 目录即可，config 无需改动（BundlePath 不变；若版本有变建议同步 Comment 版本戳）。特殊渠道：蓝牙跟 [emulatorchen fork](https://github.com/emulatorchen/IntelBluetoothFirmware)，Sequoia/Tahoe 网卡跟 [laobamac/itlwm](https://github.com/laobamac/itlwm/releases)，NootedRed 跟 ChefKiss CI。

## PC711ProbeForce（NVMe 强驱，默认启用）

[PC711Probe](https://github.com/hrx114514x/PC711Probe)（v1.8.1）为 Lilu 插件，修复 macOS 11–15 上部分 NVMe 的 Identify 超时 panic（macOS 26 已原生支持 PC711）。官方实机验证过 SK hynix PC711 / BC711 / BC511 与三星 PM991；**据网友反馈，其他型号的 NVMe 也能正常工作**。

- `PC711ProbeForce.kext` 是 Force 版：**强制让 macOS 原生不支持的 NVMe 也能运行**，本 EFI 默认启用（MaxKernel 24.99.99 封顶，即仅 macOS 11–15 加载；macOS 26 原生支持无需加载），用于替代旧的 SSDT 屏蔽出厂盘位方案。
- 不受硬盘位限制：出厂 PC611 在任何盘位都由它处理。
- ⚠️ 标准版 `PC711Probe.kext` 与 Force 版绝不可同时启用；本 EFI 仅内置 Force 版（标准版已移除，需要时从上游 release 自取并先禁用 Force）。
- 10.14–10.15 低于其 MinKernel（20）：不加载；该版本下出厂盘不会触发 panic，仅不可用。
- 更新渠道：[PC711Probe releases](https://github.com/hrx114514x/PC711Probe/releases)。

## NVMeFix 是否需要？

**建议保留**。系统盘 WD SN570 为非 Apple NVMe，NVMeFix 提供其电源管理（APST）修复，可降低睡眠唤醒时 NVMe 掉盘 / panic 的概率；与 PC711ProbeForce（默认启用）互不冲突，开销可忽略。
