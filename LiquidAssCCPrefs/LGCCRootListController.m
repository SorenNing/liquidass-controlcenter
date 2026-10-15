#import <UIKit/UIKit.h>
#import <Foundation/Foundation.h>
#import <Preferences/PSListController.h>
#import <Preferences/PSSpecifier.h>

@interface LGCCRootListController : PSListController
- (void)restoreRecommendedDefaults:(PSSpecifier *)specifier;
- (void)applyRecommendedDefaults;
@end

@implementation LGCCRootListController

- (NSArray *)specifiers {
    if (!_specifiers) {
        _specifiers = [[self loadSpecifiersFromPlistName:@"Root" target:self] mutableCopy];
        if (!_specifiers) _specifiers = [NSMutableArray array];
    }
    return _specifiers;
}

- (void)restoreRecommendedDefaults {
    [self restoreRecommendedDefaults:nil];
}

- (void)restoreRecommendedDefaults:(PSSpecifier *)specifier {
    (void)specifier;
    UIAlertController *confirmation = [UIAlertController
        alertControllerWithTitle:@"恢复原始默认参数？"
        message:@"此操作会重置本插件的液态玻璃参数，但保留总开关和控制中心开关状态；浅色背景保护会恢复到 0.30。"
        preferredStyle:UIAlertControllerStyleAlert];
    [confirmation addAction:[UIAlertAction actionWithTitle:@"取消"
        style:UIAlertActionStyleCancel handler:nil]];
    __weak typeof(self) weakSelf = self;
    [confirmation addAction:[UIAlertAction actionWithTitle:@"恢复默认"
        style:UIAlertActionStyleDestructive handler:^(__unused UIAlertAction *action) {
            [weakSelf applyRecommendedDefaults];
        }]];
    [self presentViewController:confirmation animated:YES completion:nil];
}

- (void)applyRecommendedDefaults {
    NSDictionary *root = [NSDictionary dictionaryWithContentsOfFile:
        [[NSBundle bundleForClass:self.class] pathForResource:@"Root" ofType:@"plist"]];
    NSArray *items = [root[@"items"] isKindOfClass:NSArray.class] ? root[@"items"] : @[];
    NSMutableDictionary *values = [NSMutableDictionary dictionary];
    for (NSDictionary *item in items) {
        NSString *key = item[@"key"];
        id value = item[@"default"];
        if (![key isKindOfClass:NSString.class] || !key.length || !value) continue;
        if ([key isEqualToString:@"Global.Enabled"] ||
            [key isEqualToString:@"ControlCenter.Enabled"]) continue;
        values[key] = value;
    }
    if (values.count == 0) {
        [self showRestoreResult:NO];
        return;
    }
    CFArrayRef storedKeys = CFPreferencesCopyKeyList(
        CFSTR("com.minis.liquidasscc"), kCFPreferencesCurrentUser,
        kCFPreferencesAnyHost);
    NSArray *existingKeys = CFBridgingRelease(storedKeys) ?: @[];
    NSMutableArray *keysToRemove = [NSMutableArray array];
    for (id key in existingKeys) {
        if (![key isKindOfClass:NSString.class]) continue;
        if ([key isEqualToString:@"Global.Enabled"] ||
            [key isEqualToString:@"ControlCenter.Enabled"] || values[key] != nil) continue;
        [keysToRemove addObject:key];
    }
    CFPreferencesSetMultiple((__bridge CFDictionaryRef)values,
        (__bridge CFArrayRef)keysToRemove, CFSTR("com.minis.liquidasscc"),
        kCFPreferencesCurrentUser, kCFPreferencesAnyHost);
    BOOL synchronized = CFPreferencesAppSynchronize(
        CFSTR("com.minis.liquidasscc"));
    if (!synchronized) {
        [self showRestoreResult:NO];
        return;
    }
    CFNotificationCenterPostNotification(CFNotificationCenterGetDarwinNotifyCenter(),
        CFSTR("com.minis.liquidasscc/Reload"), NULL, NULL, true);
    [self showRestoreResult:YES];
    [self reloadSpecifiers];
}

- (void)showRestoreResult:(BOOL)success {
    NSString *title = success ? @"已恢复原始默认参数" : @"恢复失败";
    NSString *message = success ? @"总开关状态已保留。请关闭并重新打开控制中心查看效果。"
                                : @"偏好写入或同步失败，未报告成功。请检查越狱文件系统状态后重试。";
    UIAlertController *alert = [UIAlertController alertControllerWithTitle:title
        message:message preferredStyle:UIAlertControllerStyleAlert];
    [alert addAction:[UIAlertAction actionWithTitle:@"好"
        style:UIAlertActionStyleDefault handler:nil]];
    [self presentViewController:alert animated:YES completion:nil];
}
@end
