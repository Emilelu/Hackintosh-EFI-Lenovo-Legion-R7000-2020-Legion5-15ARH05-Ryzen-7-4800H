# Hackintosh-EFI-Lenovo-Legion-R7000-2020-Legion5-15ARH05-Ryzen-7-4800H

> Language: English (this page) | [中文](./README.md)

OpenCore EFI dedicated to the Lenovo Legion R7000 2020 (China model; sold internationally as the Lenovo Legion 5 15ARH05, AMD Ryzen 7 4800H) — OpenCore 1.0.9 dev, deeply tuned from SimpleKaruzi's EFI, aiming to work out of the box.

- **Supported range**: tested Catalina (10.15) – Tahoe (26); Mojave (10.14) is theoretically supported, untested.
- Installation screenshots per macOS version: [Screenshots](./Screenshots).

> ⚠️ **Generate your own SMBIOS with OCAT before first use.** The shipped config has its identity blanked (`SystemSerialNumber` / `MLB` / `SystemUUID` empty, `ROM` zero-length). Booting it as-is makes Setup Assistant crash, then the machine powers off or reboots. Use [OCAT (OCAuxiliaryTools)](https://github.com/ic005k/OCAuxiliaryTools) to generate a fresh set for `MacBookPro16,2` into `PlatformInfo → Generic`, or fill in a valid serial plus a 6-byte ROM (the wired NIC MAC). Keep the identity local and never commit it back.

## Documentation

| Doc | Content |
|:---|:---|
| [docs/Compatibility.en.md](./docs/Compatibility.en.md) | macOS version differences at a glance, Wi-Fi driver matrix, Tahoe audio |
| [docs/KnownIssues.en.md](./docs/KnownIssues.en.md) | Known issues & fixes (Kernel Panic, Bluetooth, stuttering, etc.) |
| [docs/Kexts.en.md](./docs/Kexts.en.md) | Kext overview, maintenance notes (⚠️ includes a must-not-update list), NVMeFix notes |
| [docs/Optional.en.md](./docs/Optional.en.md) | Optional enhancements (HiDPI, built-in microphone, essential scripts, etc.) |

> All docs exist in both languages; every page carries a language switcher. Links for issue fixes and tools are inlined at the matching doc entries.

## Choosing a config

The repository ships only two configs (Big Sur has been folded into the default one). **Rename the chosen file to `config.plist` before use**:

| Config | Applies to | Key differences |
|:---|:---|:---|
| `config_Mojave2Catalina.plist` | Mojave (10.14) – Catalina (10.15) | Enables `SSDT-Disable_XHC0.aml` to disable the second XHCI controller; `XhciPortLimit` on, no USB injection kext; SecureBootModel = `Default`; boot-args omit `itlwm_he=1` and `ipc_control_port_options=0` |
| `config.plist` (default) | Big Sur (11.x) – Tahoe (26.x) | Pre-generated `USBMap.kext` injection for all versions; `XhciPortLimit` on; SecureBootModel = `Disabled` |

> This branch's `config.plist` is the discrete-only NVIDIA experiment and is not interchangeable with the main branch — see the next section.
>
> Factory drive slot (GPP1): on macOS 11–15 the slot is handled by the default-enabled `PC711ProbeForce.kext`; macOS 26 supports PC711 natively; on 10.14–10.15 the drive is unusable (but does not panic). `SSDT-Disable_NVMe_GPP1.aml` is disabled by default in both configs — enable it manually only if you truly need the slot blocked.

### About NootedRed (main branch only)

The main branch depends on `NootedRed.kext`: for a fresh install set its `Enabled` to `false` under `Kernel → Add`, then flip it back to `true` and reboot once the desktop comes up.

**This experimental branch does not load NootedRed** — the internal panel is driven by the GTX 1650, so none of that applies.

## Experimental branch: NVIDIA GTX 1650, discrete-only

This branch tests [nullmoth/nvidia-macos-driver](https://github.com/nullmoth/nvidia-macos-driver). It is mutually exclusive with the main branch (iGPU + NootedRed), which remains the daily-driver setup.

### Differences from the main branch

| Item | Main branch | This branch |
|:---|:---|:---|
| BIOS | Hybrid (Switchable Graphics on) | **Discrete-only**, internal panel driven by the GTX 1650 |
| iGPU driver | NootedRed enabled | Not loaded |
| dGPU | Blocked by `SSDT-Disable_GPU_GPP0.aml` | Unblocked, driven by nullmoth's driver |
| `Kernel → Block` | `AppleEthernetRL` only | adds `com.apple.iokit.IONDRVSupport` (keeps the firmware framebuffer off display index 0) |
| APFS | OpenCore `EnableJumpstart` | `EnableJumpstart=false` plus `apfs_aligned.efi` |
| Audio | AppleALC + SimpleHDA | adds `NMHDA.kext` (HDMI audio) |
| SIP | `0x803` | `0x430a0000` (driver requirement) |
| boot-args | see below | adds `nvfb=1 nvaccel=1 nvfbheads=4 -nvkmsnosmooth nvrmsettle=10000 nvfbhidpi=1 nvrmtgp=1 nvrmgps=1 nvrmnvpcf=1 nmhdavol=1 nvrmacpibl=1 nmhybrid=1` |
| Tools | — | `NullMothSafe.efi`: remove the NVIDIA driver / boot once without it |

### Test status (2026-11-17, macOS 26.7.3)

| Scenario | Result |
|:---|:---|
| Internal panel only | **Displays normally, reaches the desktop** |
| Internal + external monitor | Both panels show the mouse pointer only; WindowServer suspected not to start. HiDPI and Hybrid are untestable |
| Internal brightness | **Not adjustable** |

The bottleneck has moved from driver bring-up to WindowServer / multi-display initialisation; whether BAR1 is fully resolved is still unconfirmed. Upstream: <https://github.com/nullmoth/nvidia-macos-driver/issues/220>.

### Caveats

- The two configs are not interchangeable: dropping this branch's `config.plist` into the main branch (or the other way round) gives no display or no boot.
- Switch BIOS back to Switchable Graphics before returning to the main branch.

## BIOS setup

- **Enable** Switchable Graphics (dual-GPU switching)
- UMA Frame Buffer Size ≥ **1G**
- **Disable** Secure Boot; AMD SVM and TPM may be turned off as well (no impact either way)

## NVMe compatibility

The factory SK hynix PC611 is not in macOS's native support list (macOS 11–15 hits an Identify-timeout panic). The default config ships with `PC711ProbeForce.kext` enabled: it **forces NVMe drives that macOS does not natively support to work**, replacing the old "block the factory drive slot" approach.

- The factory PC611 is force-driven by PC711ProbeForce on macOS 11–15 no matter which slot it sits in; macOS 26 supports PC711 natively and needs no kext.
- 10.14–10.15 fall below PC711Probe's minimum kernel (it does not load): the factory drive is unusable there, but does not panic.
- `SSDT-Disable_NVMe_GPP1.aml` (blocks the GPP1 slot) is disabled by default in both configs — enable it manually only if Force does not suit your drive.
- Swapping in WD, Samsung or other compatible drives requires no action either.

## boot-args

```
-v debug=0x100 keepsyms=1 ipc_control_port_options=0 -lilubetaall -amfipassbeta -vi2c-force-polling alcid=101 -btlfxa2dpcheck itlwm_he=1
```

| Argument | Purpose |
|:---|:---|
| `-v debug=0x100 keepsyms=1` | Verbose boot log and kernel debug symbols for troubleshooting |
| `ipc_control_port_options=0` | Improves Electron app compatibility |
| `-lilubetaall` | Allows Lilu and its plugins to load on every macOS version |
| `-amfipassbeta` | Allows AMFIPass to load (used with OCLP-MOD) |
| `-vi2c-force-polling` | Forces polling for the I2C trackpad |
| `alcid=101` | Audio layout-id injection |
| `-btlfxa2dpcheck` | Fixes Intel Bluetooth + AirPods no sound (Monterey+) |
| `itlwm_he=1` | Enables Wi-Fi 6 (HE) mode for the Intel AX200 |

The two configs' boot-args differ only by `itlwm_he=1` and `ipc_control_port_options=0` (useless on older versions, hence omitted); everything else is identical.

## Hardware

| Component | Model / Name | Notes |
|:---|:---|:---|
| Mainboard | LENOVO LNVNB161216 | AMD-platform laptop (international model: Lenovo Legion 5 15ARH05) |
| BIOS | EUCN41WW (2023-09-20) | UEFI, Secure Boot disabled in BIOS setup |
| CPU | AMD Ryzen 7 4800H (Renoir) | 8 cores / 16 threads |
| Discrete GPU | NVIDIA GeForce GTX 1650 | On this branch it is driven by [nullmoth/nvidia-macos-driver](https://github.com/nullmoth/nvidia-macos-driver); the main branch blocks it with `SSDT-Disable_GPU_GPP0.aml` |
| iGPU | AMD Radeon(TM) Graphics (Renoir) | Unlocked via UMAF with VRAM set to 4G (NootedRed needs at least 512M, ≥1G recommended) |
| Internal display | LQ156T1JW05 | 2560x1440 @ 165Hz (swapped by the author); the main branch wires it to the iGPU and injects EDID, **this branch is discrete-only and the panel belongs to the GTX 1650** |
| Ethernet | Realtek RTL8168/8111 | Device ID `10EC-8168` |
| Wi-Fi | Intel Wi-Fi 6 AX200 | Device ID `8086-2723` |
| Bluetooth | Intel Wireless Bluetooth | Device ID `8087-0029`; both the AirPods no-sound and HID connection issues are fixed (see [KnownIssues.en.md](./docs/KnownIssues.en.md#2-intel-bluetooth-airpods-no-sound-fixed)) |
| Audio | Realtek ALC257 | Device ID `10EC-0257`, layout-id = 101 |
| NVMe SSD (factory) | SK hynix HFS512GD9TNI-L2A0B (PC611) | Not natively supported by macOS; force-driven by `PC711ProbeForce.kext` by default (see below) |
| NVMe SSD (added) | WD Blue SN570 500GB | System disk |
| Trackpad | SYNA2BA6 | I2C HID, driven by VoodooI2C in polling mode |
| Keyboard | PS/2 (FUJ7401) | Driven by VoodooPS2Controller |

## New driver solutions & experimental branch sources

| Item | Source |
|:---|:---|
| AirportItlwm Sequoia / Tahoe 2.4.0 builds (the official itlwm releases stop at Sonoma) | <https://github.com/laobamac/itlwm/releases> |
| SimpleHDA: restores AppleHDA removed in Tahoe (laobamac) | <https://github.com/laobamac/SimpleHDA> |
| New pre-generated USB mapping idea (win10Q, Bilibili video) | <https://www.bilibili.com/video/BV1YK9XBqEbK/> |
| IntelBluetoothFirmware third-party fork (fixes HID connections; do not use the official build) | <https://github.com/emulatorchen/IntelBluetoothFirmware> |
| nullmoth/nvidia-macos-driver: NVIDIA community-driver experiment (Turing and newer; the main branch keeps the iGPU setup) | <https://github.com/nullmoth/nvidia-macos-driver> |
| ↳ nullmoth/nvidia-macos-driver#220: upstream issue #220 matching this machine's boot hang | <https://github.com/nullmoth/nvidia-macos-driver/issues/220> |
| ↳ experimental branch experimental-nvidia-gtx1650 (NVIDIA experiment config) | <https://github.com/Emilelu/Hackintosh-EFI-Lenovo-Legion-R7000-2020-Legion5-15ARH05-Ryzen-7-4800H/tree/experimental-nvidia-gtx1650> |

## Afterword

From Chameleon to Clover, from Clover to OpenCore.
From Yosemite to Tahoe.

Ten years ago, when I first touched Hackintosh as a primary schooler, the machine I toyed with was a Lenovo IdeaPad Y460N. It did not support UEFI boot, so Chameleon was the only option — or Clover by emulating an EFI. Back then, getting a usable Hackintosh running was already a delight.

The devices kept changing since, from Intel platforms to AMD, always laptops, each one used for Hackintosh experiments and research.

Apple Silicon has gone through several generations now, and the age of Hackintosh is drawing to a close. With macOS Tahoe 26, the puzzle I have been assembling for ten years finally got its last piece.

**This post commemorates ten years of my youth, and marks a perfect full stop.**

Thanks to every open-source developer along the way — without their selfless work, Hackintosh would not be where it is.

Hackintosh may be dying, but tinkering lives forever.

May this EFI help those who are still holding the line.

---

*This EFI covers all known issue fixes so far. With so many macOS version differences, make sure to pick the matching config file. For new problems, Issues & Pull Requests are welcome.*
