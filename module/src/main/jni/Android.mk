LOCAL_PATH := $(call my-dir)

include $(CLEAR_VARS)

LOCAL_MODULE := module
LOCAL_SRC_FILES := $(patsubst $(LOCAL_PATH)/%,%,$(wildcard $(LOCAL_PATH)/*.cpp $(LOCAL_PATH)/*.c $(LOCAL_PATH)/cpp/*.cpp $(LOCAL_PATH)/../cpp/*.cpp))
ifeq ($(LOCAL_SRC_FILES),)
    LOCAL_SRC_FILES := main.cpp
endif

LOCAL_LDLIBS := -llog

include $(BUILD_SHARED_LIBRARY)
