# 版本兼容性与 Wi-Fi 驱动

> 返回 [主 README](../README.md)

> Language: [English](./Compatibility.en.md) | 中文（本页）

## 各版本差异速查

| macOS | USB 方案 | 蓝牙 | Wi-Fi | 其他 |
|:---|:---|:---|:---|:---|
| Mojave (10.14) ～ Catalina (10.15) | 禁用 XHC0 + `XhciPortLimit`（无注入 kext） | IntelBluetoothInjector | AirportItlwmMojave / Catalina | SecureBootModel = `Default` |
| Big Sur (11.x) ～ Tahoe (26.x) | 预生成 `USBMap.kext` + `XhciPortLimit` | ≤ Big Sur：IntelBluetoothInjector；Monterey+：BlueToolFixup | AirportItlwm 按版本自动匹配（见下表） | SecureBootModel = `Disabled` |

> **Catalina 及以下的代价**：无法使用为 Big Sur+ 修改的 `GenericUSBXHCI.kext`，双 XHCI 控制器互相冲突，必须通过 `SSDT-Disable_XHC0.aml` 禁用其中一个。左侧 USB-A、后侧 Type-C 及内置摄像头将不可用，此为获得稳定蓝牙与正常启动的必要代价。

## Wi-Fi 驱动矩阵

AirportItlwm 通过 MinKernel / MaxKernel 自动匹配版本，**Sonoma 14.0–14.3 与 14.4+ 的驱动互不通用，切勿混用**：

| macOS | Kext | 内核版本 |
|:---|:---|:---|
| Mojave (10.14) | AirportItlwmMojave | 18.x |
| Catalina (10.15) | AirportItlwmCatalina | 19.x |
| Big Sur (11.x) | AirportItlwmBigSur | 20.x |
| Monterey (12.x) | AirportItlwmMonterey | 21.x |
| Ventura (13.x) | AirportItlwmVentura | 22.x |
| Sonoma 14.0–14.3 | AirportItlwmSonomaUpTo14dot3 | 23.0.0–23.3.99 |
| Sonoma 14.4+ | AirportItlwmSonomaAbove14dot4 | 23.4.0–23.99.99 |
| Sequoia (15.x) | AirportItlwmSequoia（laobamac 构建） | 24.x |
| Tahoe (26.x) | AirportItlwmTahoe（laobamac 构建） | 25.x+ |

> **Sequoia / Tahoe 构建来源**：itlwm 官方 release 仅提供到 Sonoma，Sequoia (15.x) 与 Tahoe (26.x) 使用 [laobamac/itlwm](https://github.com/laobamac/itlwm/releases) 的 2.4.0 构建，直接以原生 Wi-Fi 接口工作，无需替换 IOSkywalkFamily / IO80211FamilyLegacy 传统框架（原 OCLP 方案已随新构建移除）。更新跟随 laobamac 的 release。

## Tahoe 音频

Tahoe 移除了 AppleHDA.kext。本 EFI 集成 [laobamac/SimpleHDA](https://github.com/laobamac/SimpleHDA) 的 `SimpleHDA.kext`（Lilu 插件，MinKernel 25.0.0）恢复 AppleHDA，AppleALC 继续负责编解码（`alcid=101`）。
