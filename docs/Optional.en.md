# Optional enhancements

> Back to the [main README](../README.en.md)

> Language: English (this page) | [中文](./Optional.md)

## HiDPI

- `one-key-hidpi-mod`: compatible with Ventura and below only.
- `BetterDisplay`: Sonoma and above (activation tool: <https://macked.app/tools/betterdisplay.php>); may stutter slightly while running.
- **Manual display-HiDPI tutorial (no one-key tools)** — pcbeta thread: <https://bbs.pcbeta.com/forum.php?mod=viewthread&tid=1950179>

## Essential community scripts

- **Must-have scripts for Hackintosh** — pcbeta thread: <https://bbs.pcbeta.com/viewthread-2076529-1-1.html>

## Boot menu and default entry

OpenCore has **no** "remember the last boot" switch; what you can do is set a default entry and let the timeout boot it:

- Default entry: highlight the volume in the picker and press `Ctrl+Enter` (`Misc → Security → AllowSetDefault` is enabled), or switch it later in System Settings → Startup Disk;
- Timeout: `Misc → Boot → Timeout = 8` (boots the default entry after 8 idle seconds); set it back to `0` for an unlimited wait;
- Scan range: `Misc → Security → ScanPolicy = 33494787` allows APFS / HFS / ESP / EXT and every device type, **not NTFS**, so Windows stays out of the menu; add the NTFS bit `0x800` back to show it again; if a USB stick does not appear, check whether the ESP bit `0x400` is missing.

## SwitchResX registration

- Name: `Peter Gunn`
- Code: `0079FCB69A1708F8`

## Built-in microphone

The built-in microphone is usually driven directly by AppleALC (HDA path) — test recording first as-is. [AMDMicrophone-Continuity](https://github.com/hrx114514x/AMDMicrophone-Continuity) is an **alternative** for digital microphones on the Renoir ACP/PDM path (with DMA continuity fixes). If you adopt it, note:

- It must be installed to `/Library/Extensions`; OpenCore injection is not supported (hence not bundled in this EFI);
- Loading untrusted kexts must be allowed (`csr-active-config=01000000`, lowering system security);
- Verified on a Ryzen 5 5500U + macOS 26.5.1; whether this machine's microphone uses the ACP/PDM path needs to be confirmed by yourself.

## macOS 26 animation frame drops

Try [CompositorPacer](https://github.com/githubzijian/CompositorPacer): an invisible Metal "metronome" window keeps the WindowServer composition path busy, improving the animation frame-drop feel on some macOS 26 setups.

## Virtual machines and Docker (AMD-V)

[RyzenHV](https://github.com/OverlordDev/ryzen-hypervisor.framework) is a kext that implements the `Hypervisor.framework` API on top of AMD-V (SVM). On AMD `kern.hv_support` is always 0, so Docker Desktop, Parallels, VirtualBox and `qemu -accel hvf` never start; with this kext they run unmodified. It is an **experimental project**, hence not bundled in this EFI. Before adopting it:

- **Turn SVM on in the BIOS** (this EFI's BIOS setup allows SVM off — installing RyzenHV makes that no longer true);
- Try it on a **spare EFI** first: `./rhv kext --native` writes the kext into the EFI; if anything goes wrong, boot the EFI without the kext, or add the boot-arg `-rhv_off`;
- The author verified it only on a Ryzen 7 5800H + Sequoia 15.8.1; this machine's 4800H and macOS 26 are untested (on macOS 26 Docker may also need AMFI relaxed);
- How well each VM program works varies a lot — treat the project README's matrix as the source of truth (0.7.7: Docker Desktop 4.97.0 works; Parallels only 26.5.0 build 57613; VirtualBox 7.x experimental; VMware Fusion not working yet).

## arm64 apps (Maclator)

[Maclator](https://github.com/linuxkid473/maclator) is a "reverse Rosetta": it loads the real arm64 userland (dyld plus the arm64e dyld shared cache, downloaded by you from Apple's servers) together with an arm64 Mach-O and runs the arm64 code with an interpreter plus an x86-64 JIT; syscalls go to the x86-64 host kernel and Metal calls can be bridged to the host GPU. The point is to keep apps that ship arm64 only within reach on x86-64. It is an experimental research project — note:

- It is designed for and verified on **Intel Macs** (Core i5-4440 + macOS 26.7); this machine is AMD and untested, so whether the JIT and the Metal bridge work here is up to you to find out;
- Requires a macOS 26 host, Xcode Command Line Tools and a Rust toolchain, about 10 GB of free disk, plus a one-time ≈5.5 GB download of the arm64e dyld shared cache;
- arm64 CLI tools, a small AppKit app, VS Code and Chromium (with GPU acceleration) are reported working; audio, most IOKit hardware, sandboxed apps and `CAMetalLayer`-based apps are not.
