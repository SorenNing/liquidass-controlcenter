# LiquidAss Control Center extraction (source-only)

This is a source extraction plan from `winaviation-tweaks/liquidass`, not a replacement renderer.

Retained original components:
- `Hooks/ControlCenter.x`: original SpringBoard Control Center hooks.
- `Shared/LGGlassKit.x`, `Shared/LGLiveBackdropView.m/.h`, `Shared/LGHostRegistry.h`, `Shared/LGSharedSupport.m/.h`: original material injection and live backdrop lifecycle.
- `LiquidAssBackboardd/Tweak.mm`, `LGSymbolResolver.mm/.h`: original QuartzCore/Metal `dylv.liquidglass.refraction` renderer and PAC resolver.

The source prunes non-Control-Center host defaults and restricts runtime preference access to a separate `com.minis.liquidasscc` domain. The original filter ID, Metal renderer, PAC resolver, and ControlCenter hooks are retained. The backboardd renderer preserves upstream crash-loop state and is gated off on first boot unless both explicit enable values are true. The default PreferenceLoader page is XML/plist-only, so no preference bundle Mach-O is loaded into Preferences.

Build only with the original roothide Theos workflow (`THEOS_PACKAGE_SCHEME=roothide`, `ARCHS="arm64 arm64e"`, iPhoneOS 16.5 SDK) on macOS/Apple ld64/TAPI. `.github/workflows/build.yml` performs the build and uploads an artifact named `UNVERIFIED`; `scripts/audit_package.py` checks the resulting loader metadata. This workspace has object-compile results only, not a linked or installable DEB.

The renderer is a separate backboardd dylib. A SpringBoard-only package cannot reproduce the original glass refraction; a package containing only `ControlCenter.x` is intentionally not considered equivalent.

## Verified upstream baseline

The upstream official arm64e release `dylv.liquidass_0.1.1-2b_iphoneos-arm64e.deb` was statically inspected. Its `LiquidAssBackboardd.dylib` uses real `LC_DYLD_CHAINED_FIXUPS` / ARM64E PAC00 and loads Foundation, CoreFoundation, Metal, QuartzCore, `@loader_path/.jbroot/usr/lib/libroothide.dylib`, libc++, and libSystem. Its package has separate SpringBoard and backboardd filters. This is the binary baseline the extracted package must match; local iSH stub-link outputs are not acceptable.
