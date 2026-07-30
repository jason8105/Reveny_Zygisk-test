LOCAL_PATH := $(call my-dir)

include $(CLEAR_VARS)

LOCAL_MODULE := reveny
LOCAL_SRC_FILES := \
    main.cpp \
    Utility.cpp

# Explicitly set C++ standard to avoid NDK default mismatches
LOCAL_CPP_FEATURES := rtti exceptions
LOCAL_CPP_EXTENSION := .cpp
LOCAL_CFLAGS := -std=c++17 -Wall -Wextra -Wno-unused-parameter
LOCAL_CPPFLAGS := -std=c++17 -fno-rtti -fno-exceptions

# Ensure we link against required NDK libraries
LOCAL_LDLIBS := -llog -landroid

include $(BUILD_SHARED_LIBRARY)
