LOCAL_PATH := $(call my-dir)

include $(CLEAR_VARS)

LOCAL_MODULE := module

LOCAL_CPPFLAGS += -std=c++17
LOCAL_CPP_FEATURES := rtti exceptions

LOCAL_C_INCLUDES := $(LOCAL_PATH) \
                    $(LOCAL_PATH)/imgui \
                    $(LOCAL_PATH)/imgui/backends \
                    $(LOCAL_PATH)/include \
                    $(LOCAL_PATH)/includes

LOCAL_SRC_FILES := $(patsubst $(LOCAL_PATH)/%,%,$(wildcard $(LOCAL_PATH)/*.cpp)) \
                   $(patsubst $(LOCAL_PATH)/%,%,$(wildcard $(LOCAL_PATH)/*.c)) \
                   $(patsubst $(LOCAL_PATH)/%,%,$(wildcard $(LOCAL_PATH)/imgui/*.cpp)) \
                   $(patsubst $(LOCAL_PATH)/%,%,$(wildcard $(LOCAL_PATH)/imgui/backends/*.cpp))

LOCAL_LDLIBS := -llog -landroid -lEGL -lGLESv3

include $(BUILD_SHARED_LIBRARY)
