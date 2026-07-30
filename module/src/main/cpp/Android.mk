LOCAL_PATH := $(call my-dir)

include $(CLEAR_VARS)

LOCAL_MODULE := module

LOCAL_SRC_FILES := \
    main.cpp \
    Utility.cpp

LOCAL_CPPFLAGS := -std=c++20 -Wall -Wextra -fexceptions -frtti
LOCAL_LDLIBS := -llog

include $(BUILD_SHARED_LIBRARY)
