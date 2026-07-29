LOCAL_PATH := $(call my-dir)

include $(CLEAR_VARS)

LOCAL_MODULE    := module
LOCAL_SRC_FILES := main.cpp

LOCAL_CPPFLAGS  += -std=c++20 -O3 -Wall -Wextra -fvisibility=hidden -fvisibility-inlines-hidden
LOCAL_LDLIBS    += -llog -landroid
LOCAL_LDFLAGS   += -Wl,--gc-sections -Wl,--exclude-libs,ALL

include $(BUILD_SHARED_LIBRARY)
