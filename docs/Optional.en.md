# Optional enhancements

> Back to the [main README](../README.en.md)

> Language: English (this page) | [中文](./Optional.md)

## HiDPI

- `one-key-hidpi-mod`: compatible with Ventura and below only.
- `BetterDisplay`: Sonoma and above (activation tool: <https://macked.app/tools/betterdisplay.php>); may stutter slightly while running.
- **Manual display-HiDPI tutorial (no one-key tools)** — pcbeta thread: <https://bbs.pcbeta.com/forum.php?mod=viewthread&tid=1950179>

## Essential community scripts

- **Must-have scripts for Hackintosh** — pcbeta thread: <https://bbs.pcbeta.com/viewthread-2076529-1-1.html>

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
