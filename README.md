# Hackintosh-EFI-Lenovo-Legion-R7000-2020-Legion5-15ARH05-Ryzen-7-4800H

> Language: [English](./README.en.md) | 中文（本页）

Lenovo 拯救者 R7000 2020（海外版：Legion 5 15ARH05，AMD Ryzen 7 4800H）专用 OpenCore EFI（OpenCore 1.0.9 dev），基于 SimpleKaruzi 的 EFI 深度调校，力求开箱即用。

- **支持范围**：实测 Catalina (10.15) ～ Tahoe (26)；Mojave (10.14) 为理论支持，未实测。
- 各版本安装成果截图见 [Screenshots](./Screenshots)。

## 文档导航

| 文档 | 内容 |
|:---|:---|
| [docs/Compatibility.md](./docs/Compatibility.md) | 各 macOS 版本差异速查、Wi-Fi 驱动矩阵、Tahoe 音频 |
| [docs/KnownIssues.md](./docs/KnownIssues.md) | 已知问题与修复（Kernel Panic、蓝牙、卡顿等） |
| [docs/Kexts.md](./docs/Kexts.md) | Kext 一览、维护须知（⚠️ 含不可更新清单）、NVMeFix 说明 |
| [docs/Optional.md](./docs/Optional.md) | 可选优化（HiDPI、内建麦克风、常用脚本等） |

> 全部文档均有英文版：[README.en.md](./README.en.md) 与 `docs/*.en.md`，各页顶部可互切。各问题修复与工具的链接内联在对应文档条目中。

## 配置文件选择

仓库只保留两份 config（Big Sur 已并入默认 config）。**使用前将所选文件重命名为 `config.plist`**：

| 配置文件 | 适用系统 | 关键差异 |
|:---|:---|:---|
| `config_Mojave2Catalina.plist` | Mojave (10.14) ～ Catalina (10.15) | 启用 `SSDT-Disable_XHC0.aml` 禁用第二 XHCI 控制器；开启 `XhciPortLimit`，无 USB 注入 kext；SecureBootModel = `Default`；boot-args 少 `itlwm_he=1` 与 `ipc_control_port_options=0` |
| `config.plist`（默认） | Big Sur (11.x) ～ Tahoe (26.x) | 预生成 `USBMap.kext` 全版本注入；开启 `XhciPortLimit`；SecureBootModel = `Disabled` |

> 出厂盘位（GPP1）的处理：macOS 11–15 由默认启用的 `PC711ProbeForce.kext` 强制驱动，macOS 26 原生支持，10.14–10.15 该盘不可用（也不会触发 panic）；`SSDT-Disable_NVMe_GPP1.aml` 在两份 config 中均已默认关闭，仅当确需屏蔽盘位时手动开启。

### 安装阶段：临时禁用 NootedRed

**全新安装系统时，需先将 `NootedRed.kext` 临时禁用**：在 config 的 `Kernel → Add` 中把 `NootedRed.kext` 的 `Enabled` 设为 `false`，完成安装、进入桌面后再改回 `true` 并重启。

日常使用必须保持启用——核显驱动依赖它。

### boot-args

```
-v debug=0x100 keepsyms=1 ipc_control_port_options=0 -lilubetaall -amfipassbeta -vi2c-force-polling alcid=101 -btlfxa2dpcheck itlwm_he=1
```

| 参数 | 作用 |
|:---|:---|
| `-v debug=0x100 keepsyms=1` | 详细启动日志与内核调试信息，便于排错 |
| `ipc_control_port_options=0` | 改善 Electron 应用兼容性 |
| `-lilubetaall` | 允许 Lilu 及其插件在所有系统版本加载 |
| `-amfipassbeta` | 允许 AMFIPass 加载（配合 OCLP-MOD） |
| `-vi2c-force-polling` | I2C 触摸板强制轮询 |
| `alcid=101` | 声卡 layout-id 注入 |
| `-btlfxa2dpcheck` | 修复 Intel 蓝牙 + AirPods 无声（Monterey+ 生效） |
| `itlwm_he=1` | Intel AX200 启用 Wi-Fi 6（HE）模式 |

两份 config 的 boot-args 仅差 `itlwm_he=1` 与 `ipc_control_port_options=0`（低版本用不到，已省略），其余完全相同。

## BIOS 设置

- **启用** Switchable Graphics（双显卡切换）
- UMA Frame Buffer Size ≥ **1G**
- **关闭** Secure Boot；AMD SVM 与 TPM 可选关闭（不影响使用）

## NVMe 兼容说明

出厂海力士 PC611 不在 macOS 原生支持列表内（macOS 11–15 触发 Identify 超时 panic）。默认 config 已启用 `PC711ProbeForce.kext`：**强制让 macOS 原生不支持的 NVMe 也能运行**，取代旧的"屏蔽出厂盘位"方案。

- 出厂 PC611 无论在哪个硬盘位，macOS 11–15 都由 PC711ProbeForce 强制驱动；macOS 26 原生支持 PC711，无需加载。
- 10.14–10.15 低于 PC711Probe 的最低内核要求（不加载）：该版本下出厂盘不可用，但不会触发 panic。
- `SSDT-Disable_NVMe_GPP1.aml`（屏蔽 GPP1 盘位）在两份 config 中均已默认关闭，仅当 Force 不适用于你的型号时再手动开启。
- 更换为 WD、Samsung 等兼容硬盘时无需任何处理。

## 硬件配置

| 组件 | 型号 / 名称 | 备注 |
|:---|:---|:---|
| 主板 | LENOVO LNVNB161216 | AMD 平台笔记本（海外对应机型：Lenovo Legion 5 15ARH05） |
| BIOS | EUCN41WW (2023-09-20) | UEFI，Secure Boot 已在 BIOS 内禁用 |
| CPU | AMD Ryzen 7 4800H (Renoir) | 8 核心 16 线程 |
| 独立显卡 | NVIDIA GeForce GTX 1650 | macOS 无官方驱动，日常使用已通过 `SSDT-Disable_GPU_GPP0.aml` 屏蔽；社区驱动实验（[nullmoth/nvidia-macos-driver](https://github.com/nullmoth/nvidia-macos-driver)，进行中）见 [experimental 分支](https://github.com/Emilelu/Hackintosh-EFI-Lenovo-Legion-R7000-2020-Legion5-15ARH05-Ryzen-7-4800H/tree/experimental-nvidia-gtx1650) |
| 核显 | AMD Radeon(TM) Graphics (Renoir) | 已通过 UMAF 解锁并将显存设为 4G（NootedRed 最低 512M，建议 ≥1G） |
| 内建显示器 | LQ156T1JW05 | 2560x1440 @ 165Hz，连接核显（自行更换），EDID 已注入 config |
| 有线网卡 | Realtek RTL8168/8111 | 设备 ID `10EC-8168` |
| 无线网卡 | Intel Wi-Fi 6 AX200 | 设备 ID `8086-2723` |
| 蓝牙 | Intel Wireless Bluetooth | 设备 ID `8087-0029`；AirPods 无声与 HID 设备连接问题均已修复（见 [KnownIssues.md](./docs/KnownIssues.md#2-intel-蓝牙连接-airpods-无声已修复)） |
| 声卡 | Realtek ALC257 | 设备 ID `10EC-0257`，layout-id = 101 |
| NVMe SSD（出厂） | SK hynix HFS512GD9TNI-L2A0B (PC611) | macOS 原生不支持，默认由 `PC711ProbeForce.kext` 强制驱动（见下文） |
| NVMe SSD（加装） | WD Blue SN570 500GB | 系统盘 |
| 触摸板 | SYNA2BA6 | I2C HID，VoodooI2C 轮询模式驱动 |
| 键盘 | PS/2 (FUJ7401) | VoodooPS2Controller 驱动 |

## 新驱动方案与实验分支出处

| 项 | 出处 |
|:---|:---|
| AirportItlwm Sequoia / Tahoe 2.4.0 构建（官方 itlwm release 仅到 Sonoma） | <https://github.com/laobamac/itlwm/releases> |
| SimpleHDA：恢复 Tahoe 移除的 AppleHDA（laobamac） | <https://github.com/laobamac/SimpleHDA> |
| USB 预生成映射新思路（win10Q，B 站视频） | <https://www.bilibili.com/video/BV1YK9XBqEbK/> |
| IntelBluetoothFirmware 第三方 fork（修复 HID 连接，勿用官方版） | <https://github.com/emulatorchen/IntelBluetoothFirmware> |
| NVIDIA 社区驱动实验（Turing 及更新；主分支保持核显方案） | <https://github.com/nullmoth/nvidia-macos-driver> |
| ↳ 本机卡住对应的上游 issue #220 | <https://github.com/nullmoth/nvidia-macos-driver/issues/220> |
| ↳ 实验分支 experimental-nvidia-gtx1650（N 卡实验 config） | <https://github.com/Emilelu/Hackintosh-EFI-Lenovo-Legion-R7000-2020-Legion5-15ARH05-Ryzen-7-4800H/tree/experimental-nvidia-gtx1650> |

## 后记

从 Chameleon 到 Clover，从 Clover 到 OpenCore。
从 Yosemite 到 Tahoe。

十年前初次接触黑苹果时，笔者尚在小学阶段，折腾的第一台机器是联想 IdeaPad Y460N。该机型不支持 UEFI 引导，只能依靠 Chameleon，或通过模拟 EFI 的方式使用 Clover。彼时若能成功装上一个可用的 Hackintosh，便足以欣喜许久。

日后设备几经更迭，从 Intel 平台到 AMD 平台，始终以笔记本为主，每一台都曾用于黑苹果的尝试与研究。

如今 Apple Silicon 已迭代数代，黑苹果的时代行将落幕。这块拼了十年的拼图，终于在 macOS Tahoe 26 上拼完了最后一块。

**谨以此帖，纪念十年青春，画上完美的终止符。**

感谢一路上所有开源开发者的付出，没有前辈们的无私奉献，黑苹果不会有今天的高度。

黑果将死，但折腾永存。

愿这份 EFI 能帮助到仍在坚守黑苹果的各位。

---

*本 EFI 已涵盖目前所有已知问题的修复。因系统版本差异较多，请务必选择对应的配置文件。如遇到新问题，欢迎提交 Issue & Pull Request。*
