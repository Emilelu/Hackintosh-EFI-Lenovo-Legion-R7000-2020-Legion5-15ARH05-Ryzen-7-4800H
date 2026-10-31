# Kext overview & maintenance notes

> Back to the [main README](../README.en.md)

> Language: English (this page) | [中文](./Kexts.md)

## Integrated kexts

| Category | Kext | Version | Purpose / applicability |
|:---|:---|:---|:---|
| Base | `Lilu` | 1.7.3 | Patch engine, prerequisite of every plugin |
| | `VirtualSMC` | 1.3.9 | SMC emulation (with `SMCBatteryManager` battery, `SMCLightSensor` light sensor) |
| | `SMCProcessorAMD` | 1.0.1 | VirtualSMC plugin, AMD CPU sensors |
| | `ForgedInvariant` | 1.5.0 | TSC invariant fix |
| | `AppleMCEReporterDisabler` | 1.2 | Disables MCE reporting, avoids AMD-platform Kernel Panics |
| | `RestrictEvents` | 1.1.7 | Fixes CPU name display, etc. |
| iGPU | `NootedRed` | 0.9.0 | Renoir iGPU driver (Mojave+) |
| | `BrightnessKeys` | 1.0.4 | Brightness hotkeys |
| Audio | `AppleALC` | 1.9.8 | Codec driver (`alcid=101`) |
| | `SimpleHDA` | 1.0.0 | by laobamac, restores AppleHDA removed in Tahoe (MinKernel 25.0.0) |
| Ethernet | `RealtekRTL8111` | 3.0.0 | Realtek NIC driver |
| Wi-Fi | `AirportItlwm` (9 builds) | 2.3.0 / 2.4.0 | Matched per macOS version: ≤ Sonoma is official 2.3.0, Sequoia/Tahoe are [laobamac](https://github.com/laobamac/itlwm/releases) 2.4.0 — see [Compatibility.en.md](./Compatibility.en.md#wi-fi-driver-matrix) |
| Bluetooth | `IntelBluetoothFirmware` / `IntelBTPatcher` | 2.5.2 | Intel Bluetooth firmware & patcher (**emulatorchen fork**, do not use the official build) |
| | `IntelBluetoothInjector` | 2.5.2 | ≤ Big Sur (MaxKernel 20.99.99) |
| | `BlueToolFixup` (fixed build) | 2.7.3 | Monterey+, includes the AirPods no-sound fix ⚠️ do not update, see below |
| USB | `GenericUSBXHCI` | 1.3.0b2 | AMD XHCI controller driver, Big Sur+ ⚠️ modified build, do not update |
| | `USBMap` | 1.1 | Pre-generated USB map (all versions; idea from win10Q), used by the default config |
| Storage | `NVMeFix` | 1.1.4 | NVMe power management & compatibility fixes (see below) |
| | `PC711ProbeForce` | 1.8.1 | Forces unsupported NVMe drives to work (11–15 only), enabled by default, see below |
| | `CtlnaAHCIPort` / `SATA-unsupported` | 341.0.2 / 0.9.2 | SATA controller support (Big Sur+ / Catalina and below) |
| Input | `VoodooPS2Controller` | 2.3.8 | PS/2 keyboard |
| | `VoodooI2C` + `VoodooI2CHID` | 2.9.1 | I2C trackpad |
| Misc | `YogaSMC` | 1.5.3 | Lenovo Fn hotkeys |
| | `ECEnabler` | 1.0.6 | Reads full EC fields, fixes battery status |
| | `Innie` | 1.3.1 | Marks PCIe devices as internal |
| | `AMFIPass` | 1.4.1 | Allows OCLP-MOD patching (Sequoia+ with `-amfipassbeta`) |
| | `HoRNDIS` | 9.2 | Android USB tethering |
| | `CpuTscSync` | 1.1.2 | TSC sync fallback (disabled by default, kept for backup) |

## Kexts that must NOT follow official updates

These kexts are modified builds, third-party forks or local custom products. **Updating them loses the fix / mapping and breaks functionality directly**:

| Kext | Reason |
|:---|:---|
| `BlueToolFixup.kext` 2.7.3 | Fixed build from [BlueToolFixup-FixA2DP](https://github.com/hexxyan/BlueToolFixup-FixA2DP) with the A2DP clock-read patch; the official build lacks it — replacing it makes AirPods silent again (and `-btlfxa2dpcheck` becomes useless) |
| `IntelBluetoothFirmware` / `IntelBTPatcher` / `IntelBluetoothInjector` 2.5.2 | From the [emulatorchen/IntelBluetoothFirmware](https://github.com/emulatorchen/IntelBluetoothFirmware) third-party fork, fixes HID devices failing to connect; the official build lacks the fix. Follow that fork for updates |
| `GenericUSBXHCI.kext` 1.3.0b2 | AMD XHCI fork modified for Big Sur+; the official RehabMan build has no AMD adaptation |
| `USBMap.kext` 1.1 | A **locally pre-generated USB map** exported by USBToolBox, not an upstream release (idea from win10Q) |
| `CtlnaAHCIPort` / `SATA-unsupported` / `AppleMCEReporterDisabler` | Community-maintained builds with no official release channel; keep as-is |

## Updatable kext status (checked 2026-10)

All other kexts can follow official updates. Findings:

- **Already latest**: ForgedInvariant 1.5.0, YogaSMC 1.5.3, ECEnabler 1.0.6, Innie 1.3.1, SMCProcessorAMD 1.0.1, PC711ProbeForce 1.8.1, SimpleHDA 1.0.0, HoRNDIS 9.2 (upstream dead long ago), RealtekRTL8111 3.0.0, AirportItlwm ≤ Sonoma (= itlwm official v2.3.0, the latest release) and Sequoia/Tahoe (= laobamac 2.4.0).
- **Local is ahead of the official release** (CI builds, no downgrade needed): Lilu 1.7.3 (official 1.7.2; dortania CI is also 1.7.3), NootedRed 0.9.0 (official 0.8.10), RestrictEvents 1.1.7 (official 1.1.6), BrightnessKeys 1.0.4 (official 1.0.3), NVMeFix 1.1.4 (official 1.1.3), VoodooPS2Controller 2.3.8.
- **Updated this round**: VirtualSMC family 1.3.8 → **1.3.9** (dortania CI b5c62c2).
- **OpenCore itself**: updated to **1.0.9 dev** (dortania 78d5ff8, 2026-10-23), replacing `BOOTx64.efi`, `OpenCore.efi`, `OpenRuntime.efi`, `OpenCanopy.efi`, `ResetNvramEntry.efi`; `HfsPlus.efi` stays at the OcBinaryData version. Both configs pass ocvalidate (1.0.9) — since 1.0.9 every Drivers entry requires the `HideVerbose` key, which has been added.

Update method: download from each official repository release and replace the whole `EFI/OC/Kexts/<name>.kext` directory; the config needs no change (BundlePath unchanged; if the version changes, update the Comment version stamp too). Special channels: Bluetooth follows the [emulatorchen fork](https://github.com/emulatorchen/IntelBluetoothFirmware), Sequoia/Tahoe Wi-Fi follows [laobamac/itlwm](https://github.com/laobamac/itlwm/releases), NootedRed follows ChefKiss CI.

## PC711ProbeForce (NVMe force-driver, enabled by default)

[PC711Probe](https://github.com/hrx114514x/PC711Probe) (v1.8.1) is a Lilu plugin fixing the Identify-timeout panic some NVMe drives hit on macOS 11–15 (macOS 26 supports PC711 natively). The upstream author verified SK hynix PC711 / BC711 / BC511 and Samsung PM991 on real hardware; **per user reports, other NVMe models work as well**.

- `PC711ProbeForce.kext` is the Force variant: it **forces NVMe drives that macOS does not natively support to work**. This EFI enables it by default (MaxKernel capped at 24.99.99, i.e. macOS 11–15 only; macOS 26 supports PC711 natively and needs no kext), replacing the old SSDT-based factory-slot blocking.
- Slot-independent: the factory PC611 is handled wherever it sits.
- ⚠️ The standard `PC711Probe.kext` and the Force variant must never be enabled together; this EFI ships only the Force build (the standard one was removed — grab it from the upstream release if needed, and disable Force first).
- 10.14–10.15 fall below its MinKernel (20): it does not load; there the factory drive does not panic but stays unusable.
- Update channel: [PC711Probe releases](https://github.com/hrx114514x/PC711Probe/releases).

## Is NVMeFix needed?

**Keep it**. The system disk (WD SN570) is a non-Apple NVMe; NVMeFix provides its power-management (APST) fix and lowers the chance of NVMe dropouts / panics around sleep-wake. It does not conflict with PC711ProbeForce (enabled by default) and its overhead is negligible.
