#import <UIKit/UIKit.h>
#import <QuartzCore/QuartzCore.h>
#import <objc/message.h>
#import <math.h>

@interface LGSettingsLowBlurView : UIView
@property (nonatomic) CGFloat lgBlurRadius;
@end

@implementation LGSettingsLowBlurView
+ (Class)layerClass { return NSClassFromString(@"CABackdropLayer") ?: CALayer.class; }
- (instancetype)initWithFrame:(CGRect)frame {
    self = [super initWithFrame:frame];
    if (!self) return nil;
    self.userInteractionEnabled = NO;
    self.backgroundColor = UIColor.clearColor;
    self.opaque = NO;
    _lgBlurRadius = 3.0;
    [self lg_configure];
    return self;
}
- (void)didMoveToWindow { [super didMoveToWindow]; [self lg_configure]; }
- (void)layoutSubviews { [super layoutSubviews]; [self lg_configure]; }
- (void)setLgBlurRadius:(CGFloat)radius {
    if (fabs(_lgBlurRadius - radius) < 0.01) return;
    _lgBlurRadius = radius;
    [self lg_configure];
}

- (void)lg_configure {
    Class backdrop = NSClassFromString(@"CABackdropLayer");
    if (!backdrop || ![self.layer isKindOfClass:backdrop]) return;
    @try {
        if (_lgBlurRadius <= 0.0) {
            self.layer.filters = nil;
            return;
        }
        [self.layer setValue:@NO forKey:@"layerUsesCoreImageFilters"];
        [self.layer setValue:@YES forKey:@"windowServerAware"];
        if (![self.layer valueForKey:@"groupName"])
            [self.layer setValue:NSUUID.UUID.UUIDString forKey:@"groupName"];
        Class filterClass = NSClassFromString(@"CAFilter");
        SEL selector = NSSelectorFromString(@"filterWithName:");
        id filter = filterClass && [filterClass respondsToSelector:selector]
            ? ((id (*)(Class, SEL, NSString *))objc_msgSend)
                (filterClass, selector, @"gaussianBlur") : nil;
        if (filter) {
            [filter setValue:@(_lgBlurRadius) forKey:@"inputRadius"];
            [filter setValue:@YES forKey:@"inputNormalizeEdges"];
            self.layer.filters = @[ filter ];
        }
    } @catch (__unused NSException *exception) {}
}
@end
