LOCAL_PATH := $(call my-dir)

include $(CLEAR_VARS)

LOCAL_MODULE := module
LOCAL_SRC_FILES := Main.cpp
LOCAL_CPPFLAGS := -std=c++20
LOCAL_LDLIBS := -llog -ldl

include $(BUILD_SHARED_LIBRARY)
