include $(THEOS)/makefiles/common.mk
TWEAK_NAME = LiquidAssCCBackboardd
LiquidAssCCBackboardd_INSTALL_PATH = /Library/MobileSubstrate/DynamicLibraries
LiquidAssCCBackboardd_FILES = Tweak.mm LGSymbolResolver.mm
LiquidAssCCBackboardd_CFLAGS = -fobjc-arc -std=c++17 -fno-objc-arc-exceptions
LiquidAssCCBackboardd_FRAMEWORKS = Metal Foundation QuartzCore CoreFoundation
LiquidAssCCBackboardd_LDFLAGS = -lc++ -Wl,-undefined,error -Wl,-fixup_chains
LiquidAssCCBackboardd_LIBRARIES = roothide
include $(THEOS_MAKE_PATH)/tweak.mk
