LOCAL_PATH := $(call my-dir)

include $(CLEAR_VARS)

LOCAL_MODULE := module

# Find all C/C++ source files recursively
FILE_LIST := $(wildcard $(LOCAL_PATH)/*.cpp) \
             $(wildcard $(LOCAL_PATH)/**/*.cpp) \
             $(wildcard $(LOCAL_PATH)/*.c) \
             $(wildcard $(LOCAL_PATH)/**/*.c) \
             $(wildcard $(LOCAL_PATH)/*.cc) \
             $(wildcard $(LOCAL_PATH)/**/*.cc)

LOCAL_SRC_FILES := $(FILE_LIST:$(LOCAL_PATH)/%=%)

LOCAL_C_INCLUDES := $(LOCAL_PATH) \
                    $(LOCAL_PATH)/.. \
                    $(LOCAL_PATH)/ModMenu

LOCAL_LDLIBS := -llog -landroid -lEGL -lGLESv2 -lz

# Suppress warnings and errors that prevent compilation in newer NDKs
LOCAL_CFLAGS := -O3 -fvisibility=hidden -fdata-sections -ffunction-sections -w -Wno-error -Wno-format-security -Wno-error=format-security -Wno-error=narrowing -Wno-c++11-narrowing
LOCAL_CPPFLAGS := -std=c++17 -fexceptions -frtti -O3 -fvisibility=hidden -fdata-sections -ffunction-sections -w -Wno-error -Wno-format-security -Wno-error=format-security -Wno-error=narrowing -Wno-c++11-narrowing

LOCAL_LDFLAGS := -Wl,--gc-sections

include $(BUILD_SHARED_LIBRARY)
