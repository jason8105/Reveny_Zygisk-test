LOCAL_PATH := $(call my-dir)

include $(CLEAR_VARS)

LOCAL_MODULE := module

LOCAL_CPPFLAGS := -std=c++17 -fpermissive -Wno-error -fdeclspec -fexceptions -frtti -fvisibility=hidden
LOCAL_CFLAGS := -fvisibility=hidden -Wno-error

LOCAL_C_INCLUDES := $(LOCAL_PATH)

LOCAL_SRC_FILES := \
    Main.cpp \
    ModMenu.cpp

LOCAL_LDLIBS := -llog -landroid -lEGL -lGLESv2

include $(BUILD_SHARED_LIBRARY)
