APP_ABI := arm64-v8a armeabi-v7a x86 x86_64
APP_PLATFORM := android-26
APP_STL := c++_static
APP_CPPFLAGS := -std=c++20 -O3 -Wall -Wextra
APP_CFLAGS := -O3 -Wall
APP_LDFLAGS := -Wl,--gc-sections
