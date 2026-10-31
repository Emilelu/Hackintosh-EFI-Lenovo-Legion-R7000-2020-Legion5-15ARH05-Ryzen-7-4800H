# Known issues & fixes

> Back to the [main README](../README.en.md)

> Language: English (this page) | [中文](./KnownIssues.md)

### 1. macOS Tahoe 26.4+ boot Kernel Panic (fixed)

The first boot after a normal shutdown or restart very likely panics and needs one forced reboot. Root cause: in Darwin 25.4.0 the offset of the kernel-thread TSC check instruction moved from 0x488 to 0x490, so the old AMD kernel patch's match mask no longer hits and the patch never applies. Solved for good by updating the AMD kernel patch.
> Details: [AMD_Vanilla PR #215](https://github.com/AMD-OSX/AMD_Vanilla/pull/215)

### 2. Intel Bluetooth + AirPods no sound (fixed)

macOS's `bluetoothd` reads the Bluetooth hardware clock (HCI Read Clock) when establishing the A2DP channel; Intel cards cannot support it or respond too slowly, and on timeout the system cuts the audio channel outright — "connected but no sound". This EFI ships a fixed `BlueToolFixup.kext` (v2.7.3) plus the `-btlfxa2dpcheck` boot argument; macOS 12 – 26 are supported in theory.
> Verified on Tahoe 26.4.1 + AX200 + AirPods Pro 2. Details: [pcbeta thread](https://bbs.pcbeta.com/viewthread-2068319-1-1.html), [BlueToolFixup-FixA2DP](https://github.com/hexxyan/BlueToolFixup-FixA2DP)
>
> ⚠️ The bundled BlueToolFixup is a **modified build** — do not replace it with the official one; see [Kexts.en.md](./Kexts.en.md#kexts-that-must-not-follow-official-updates).

### 3. Occasional hang during boot (not fully fixed)

Affects all versions: the boot process occasionally stalls. Press any key to resume the boot; if that fails, force-restart. Widely suspected to be caused by the instability of AMD's dual XHCI controllers; this EFI now uses a pre-generated USB map (`USBMap.kext`) and keeps the second-XHCI-disabling strategy only in the 10.14–10.15 config, which reduced the occurrence to a minimum.

### 4. Chromium / Electron apps freezing (NootedRed limitation)

NootedRed officially does not support Chromium hardware acceleration; browsers and Electron apps may freeze or show graphical glitches. Root cause: apps using OpenGL dual-source blending crash NootedRed. Workarounds:

- Disable **GPU rasterization** in `chrome://flags`, or launch with `open -a <app> --args --disable-gpu`.
- **GLFriend**: a small dedicated launcher (AppleScript) that starts affected apps with pure OpenGL 4.1 acceleration, avoiding the dual-source-blend crash; works on macOS 10.15+, any app selectable, at the cost of always launching through it ([tool intro](https://imacos.top/2024/09/03/glfriend-v1-02/)).
- **Sonoma+ wallpaper / video-decode hangs, repeated gpuRestart**: CoreMedia's Metal transfer session conflicts with VideoToolbox hardware decoding; disable that preference to work around it ([NootedRed #235](https://github.com/ChefKissInc/NootedRed/issues/235#issuecomment-4567109847)):
  ```bash
  sudo defaults write /Library/Preferences/com.apple.coremedia allowMetalTransferSession -bool NO
  sudo chmod 644 /Library/Preferences/com.apple.coremedia.plist
  ```
  When doing this from Recovery, replace the path with `/Volumes/<system volume>/Library/...`, then reboot.

### 5. macOS Tahoe system stutter (Spotlight indexing)

On Tahoe, Finder, right-click menus and app launches stuttering is often caused by the Spotlight indexer (`mds`). Mitigations:

- Temporary: `sudo mdutil -a -i off`, and add `/Applications` to the Spotlight Privacy exclusion list.
- Permanent (needs SIP disabled from Recovery):
  ```bash
  sudo launchctl unload -w /System/Library/LaunchDaemons/com.apple.metadata.mds.plist
  sudo rm -rf /.Spotlight-V100
  ```
- Cost: you lose system-wide search; third-party tools like Raycast can fill in.
> Details: [pcbeta thread](https://bbs.pcbeta.com/viewthread-2073020-1-1.html)

### 6. macOS 26 animation frame drops

Try [CompositorPacer](https://github.com/githubzijian/CompositorPacer): an invisible Metal "metronome" window keeps the WindowServer composition path busy, improving the animation frame-drop feel on some macOS 26 setups.

### 7. Intel Bluetooth HID devices fail to connect (solved)

Bluetooth HID devices (mice, keyboards, etc.) pair but never connect. Solved by moving the Intel Bluetooth drivers to the [emulatorchen/IntelBluetoothFirmware](https://github.com/emulatorchen/IntelBluetoothFirmware) third-party fork at 2.5.2 (`IntelBluetoothFirmware` / `IntelBTPatcher` / `IntelBluetoothInjector`), together with the fixed BlueToolFixup 2.7.3 and `-btlfxa2dpcheck`.
>
> ⚠️ The Bluetooth trio is a **third-party fork** — do not replace it with the official build; see [Kexts.en.md](./Kexts.en.md#kexts-that-must-not-follow-official-updates).
