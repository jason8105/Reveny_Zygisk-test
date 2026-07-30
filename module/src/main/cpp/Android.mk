LOCAL_PATH := $(call my-dir)

include $(CLEAR_VARS)

LOCAL_MODULE := reveny

LOCAL_CPPFLAGS := -std=c++17 -fexceptions -frtti -fno-char8_t
LOCAL_CFLAGS := -O3 -fvisibility=hidden

LOCAL_C_INCLUDES := $(LOCAL_PATH) \
                    $(LOCAL_PATH)/includes \
                    $(LOCAL_PATH)/imgui

LOCAL_SRC_FILES := $(wildcard $(LOCAL_PATH)/*.cpp)
LOCAL_SRC_FILES += $(wildcard $(LOCAL_PATH)/*/*.cpp)
LOCAL_SRC_FILES += $(wildcard $(LOCAL_PATH)/*/*/*.cpp)
LOCAL_SRC_FILES := $(LOCAL_SRC_FILES:$(LOCAL_PATH)/%=%)

LOCAL_LDLIBS := -landroid -llog -lEGL -lGLESv2 -lGLESv3

include $(BUILD_SHARED_LIBRARY)
