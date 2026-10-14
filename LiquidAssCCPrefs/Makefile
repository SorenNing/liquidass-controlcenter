include $(THEOS)/makefiles/common.mk

BUNDLE_NAME = LiquidAssCCPrefs
LiquidAssCCPrefs_FILES = LGCCRootListController.m
LiquidAssCCPrefs_INSTALL_PATH = /Library/PreferenceBundles
LiquidAssCCPrefs_CFLAGS = -fobjc-arc -fno-autolink
LiquidAssCCPrefs_FRAMEWORKS = UIKit Foundation CoreFoundation
LiquidAssCCPrefs_PRIVATE_FRAMEWORKS = Preferences
LiquidAssCCPrefs_LIBRARIES = roothide
LiquidAssCCPrefs_RESOURCE_DIRS = Resources
LiquidAssCCPrefs_LDFLAGS = -Wl,-undefined,error -Wl,-fixup_chains

include $(THEOS_MAKE_PATH)/bundle.mk
