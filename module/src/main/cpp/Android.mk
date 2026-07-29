LOCAL_PATH := $(call my-dir)

include $(CLEAR_VARS)

LOCAL_MODULE := module

LOCAL_CPPFLAGS += -std=c++17 -fexceptions -frtti
LOCAL_CFLAGS += -O2

LOCAL_C_INCLUDES := $(LOCAL_PATH)

LOCAL_SRC_FILES := \
    Drawing.cpp \
    main.cpp

LOCAL_LDLIBS := -llog -landroid -lEGL -lGLESv3

include $(BUILD_SHARED_LIBRARY)
