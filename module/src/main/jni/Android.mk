LOCAL_PATH := $(call my-dir)

include $(CLEAR_VARS)

LOCAL_MODULE := module
LOCAL_SRC_FILES := main.cpp
LOCAL_CPPFLAGS += -std=c++20

include $(BUILD_SHARED_LIBRARY)
