LOCAL_PATH := $(call my-dir)

include $(CLEAR_VARS)

LOCAL_MODULE := module
LOCAL_SRC_FILES := ../cpp/Main.cpp
LOCAL_C_INCLUDES := $(LOCAL_PATH)/../cpp
LOCAL_LDLIBS := -llog -landroid
LOCAL_CPPFLAGS := -std=c++2a

include $(BUILD_SHARED_LIBRARY)
