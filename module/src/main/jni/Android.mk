LOCAL_PATH := $(call my-dir)

include $(CLEAR_VARS)

LOCAL_MODULE := module

LOCAL_CPPFLAGS := -std=c++17 -fpermissive -Wno-error -fdeclspec -fexceptions -frtti -fvisibility=hidden
LOCAL_CFLAGS := -fvisibility=hidden -Wno-error

LOCAL_C_INCLUDES := $(LOCAL_PATH) \
                    $(LOCAL_PATH)/../cpp \
                    $(LOCAL_PATH)/../cpp/Headers \
                    $(LOCAL_PATH)/../cpp/External/ImGui \
                    $(LOCAL_PATH)/../cpp/External/KittyMemory \
                    $(LOCAL_PATH)/../cpp/External/Dobby

LOCAL_SRC_FILES := \
    ../cpp/Main.cpp \
    ../cpp/ModMenu.cpp \
    ../cpp/Drawing.cpp \
    ../cpp/Utility.cpp \
    ../cpp/External/ImGui/imgui.cpp \
    ../cpp/External/ImGui/imgui_draw.cpp \
    ../cpp/External/ImGui/imgui_tables.cpp \
    ../cpp/External/ImGui/imgui_widgets.cpp

LOCAL_LDLIBS := -llog -landroid -lEGL -lGLESv2

include $(BUILD_SHARED_LIBRARY)
