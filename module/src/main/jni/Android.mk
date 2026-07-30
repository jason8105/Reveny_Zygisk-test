LOCAL_PATH := $(call my-dir)

include $(CLEAR_VARS)

LOCAL_MODULE := reveny

LOCAL_CPPFLAGS := -std=c++20 -fexceptions -frtti -Wall -Wno-error=format-security -Wno-unused-variable
LOCAL_CFLAGS := -Wall -Wno-error=format-security

LOCAL_C_INCLUDES := $(LOCAL_PATH)

LOCAL_SRC_FILES := ModMenu.cpp \
                   main.cpp

LOCAL_LDLIBS := -llog -landroid -lEGL -lGLESv2 -lz

include $(BUILD_SHARED_LIBRARY)
