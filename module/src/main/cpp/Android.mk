LOCAL_PATH := $(call my-dir)

include $(CLEAR_VARS)

LOCAL_MODULE := module
LOCAL_SRC_FILES := main.cpp Utility.cpp
LOCAL_LDLIBS := -llog
LOCAL_CPPFLAGS += -std=c++17 -Wall

include $(BUILD_SHARED_LIBRARY)
