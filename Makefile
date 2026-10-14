export TARGET := iphone:clang:16.5:14.0
export ARCHS := arm64 arm64e
export THEOS_PACKAGE_SCHEME := roothide

ifneq ($(shell uname -s),Darwin)
$(error Use the object-only validation script on Linux; final dylibs require native Apple tooling)
endif
ifneq ($(THEOS_PACKAGE_SCHEME),roothide)
$(error This candidate is for roothide only; ordinary rootless has a different package layout)
endif
export TARGET_CC := $(shell xcrun -f clang)
export TARGET_CXX := $(shell xcrun -f clang++)
export TARGET_LD := $(shell xcrun -f clang++)
include $(THEOS)/makefiles/common.mk

TWEAK_NAME = liquidasscc
liquidasscc_FILES = Hooks/ControlCenter.x Shared/LGGlassKit.x Shared/LGLiveBackdropView.m Shared/LGSharedSupport.m Shared/LGNativeBlurView.m
# These Logos .x files are Objective-C, matching the shared .m implementations.
# Distinct dylib names can share the standard injection directory without overwriting.
liquidasscc_INSTALL_PATH = /Library/MobileSubstrate/DynamicLibraries
liquidasscc_CFLAGS = -fobjc-arc
liquidasscc_USE_MODULES = 0
liquidasscc_FRAMEWORKS = UIKit Foundation QuartzCore CoreFoundation CoreGraphics CoreMotion
liquidasscc_LIBRARIES = roothide substrate
liquidasscc_LDFLAGS = -Wl,-undefined,error -Wl,-fixup_chains
include $(THEOS_MAKE_PATH)/tweak.mk

SUBPROJECTS += LiquidAssBackboardd LiquidAssCCPrefs
include $(THEOS_MAKE_PATH)/aggregate.mk
