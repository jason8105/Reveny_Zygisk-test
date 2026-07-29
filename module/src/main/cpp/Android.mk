LOCAL_PATH := $(call my-dir)

include $(CLEAR_VARS)

LOCAL_MODULE := module

# Dynamically discover all .cpp and .c source files in the directory
LOCAL_SRC_FILES := $(patsubst $(LOCAL_PATH)/%,%,$(wildcard $(LOCAL_PATH)/*.cpp $(LOCAL_PATH)/*.c))

LOCAL_LDLIBS := -llog
LOCAL_CFLAGS := -Wall -O3
LOCAL_CPPFLAGS := -std=c++20

include $(BUILD_SHARED_LIBRARY)
