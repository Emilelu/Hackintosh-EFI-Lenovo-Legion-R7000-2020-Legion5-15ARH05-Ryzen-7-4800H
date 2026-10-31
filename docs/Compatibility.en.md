# Version compatibility & Wi-Fi drivers

> Back to the [main README](../README.en.md)

> Language: English (this page) | [中文](./Compatibility.md)

## Version differences at a glance

| macOS | USB | Bluetooth | Wi-Fi | Other |
|:---|:---|:---|:---|:---|
| Mojave (10.14) – Catalina (10.15) | XHC0 disabled + `XhciPortLimit` (no injection kext) | IntelBluetoothInjector | AirportItlwmMojave / Catalina | SecureBootModel = `Default` |
| Big Sur (11.x) – Tahoe (26.x) | Pre-generated `USBMap.kext` + `XhciPortLimit` | ≤ Big Sur: IntelBluetoothInjector; Monterey+: BlueToolFixup | AirportItlwm matched per version (table below) | SecureBootModel = `Disabled` |

> **The cost on Catalina and below**: the `GenericUSBXHCI.kext` modified for Big Sur+ cannot be used, and the dual XHCI controllers conflict with each other, so one of them must be disabled via `SSDT-Disable_XHC0.aml`. The left USB-A, the rear Type-C and the internal camera become unavailable — the necessary price for stable Bluetooth and a normal boot.

## Wi-Fi driver matrix

AirportItlwm picks its version automatically via MinKernel / MaxKernel. **The Sonoma 14.0–14.3 and 14.4+ drivers are mutually incompatible — never mix them**:

| macOS | Kext | Kernel version |
|:---|:---|:---|
| Mojave (10.14) | AirportItlwmMojave | 18.x |
| Catalina (10.15) | AirportItlwmCatalina | 19.x |
| Big Sur (11.x) | AirportItlwmBigSur | 20.x |
| Monterey (12.x) | AirportItlwmMonterey | 21.x |
| Ventura (13.x) | AirportItlwmVentura | 22.x |
| Sonoma 14.0–14.3 | AirportItlwmSonomaUpTo14dot3 | 23.0.0–23.3.99 |
| Sonoma 14.4+ | AirportItlwmSonomaAbove14dot4 | 23.4.0–23.99.99 |
| Sequoia (15.x) | AirportItlwmSequoia (laobamac build) | 24.x |
| Tahoe (26.x) | AirportItlwmTahoe (laobamac build) | 25.x+ |

> **Where the Sequoia / Tahoe builds come from**: the official itlwm releases only go up to Sonoma, so Sequoia (15.x) and Tahoe (26.x) use the 2.4.0 builds from [laobamac/itlwm](https://github.com/laobamac/itlwm/releases). They work over the native Wi-Fi interface directly — no IOSkywalkFamily / IO80211FamilyLegacy framework swap needed (the old OCLP approach was removed along with these builds). Follow laobamac's releases for updates.

## Tahoe audio

Tahoe removed AppleHDA.kext. This EFI integrates `SimpleHDA.kext` from [laobamac/SimpleHDA](https://github.com/laobamac/SimpleHDA) (a Lilu plugin, MinKernel 25.0.0) to restore AppleHDA, while AppleALC keeps handling the codec (`alcid=101`).
