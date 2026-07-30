LOCAL_PATH := $(call my-dir)

include $(CLEAR_VARS)

LOCAL_MODULE := reveny
LOCAL_SRC_FILES := main.cpp
LOCAL_LDLIBS := -log -landroid
LOCAL_CPPFLAGS := -std=c++17

include $(BUILD_SHARED_LIBRARY)
