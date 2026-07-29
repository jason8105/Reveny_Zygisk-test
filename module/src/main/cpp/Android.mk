LOCAL_PATH := $(call my-dir)

# 1. Sabse pehle External libraries ko compile karne ke liye include karein
include $(LOCAL_PATH)/External/Android.mk

# 2. Main module ke variables clear karein
include $(CLEAR_VARS)

LOCAL_MODULE := module

LOCAL_CPPFLAGS := -std=c++17 -fpermissive -Wno-error -fdeclspec -fexceptions -frtti -fvisibility=hidden
LOCAL_CFLAGS := -fvisibility=hidden -Wno-error

# 3. Saare folders ke paths yahan daalein taaki 'imgui.h' easily mil jaye
LOCAL_C_INCLUDES := $(LOCAL_PATH) \
                    $(LOCAL_PATH)/Include \
                    $(LOCAL_PATH)/Headers \
                    $(LOCAL_PATH)/External/ImGui \
                    $(LOCAL_PATH)/External/KittyMemory \
                    $(LOCAL_PATH)/External/Dobby

# 4. Saari C++ files ko compile list mein add karein
LOCAL_SRC_FILES := \
    Main.cpp \
    ModMenu.cpp \
    Drawing.cpp \
    Utility.cpp

# 5. Android ki default libraries
LOCAL_LDLIBS := -llog -landroid -lEGL -lGLESv2

# 6. External folder se aane wali static libraries ko link karein
LOCAL_STATIC_LIBRARIES := libimgui libkitty libdobby

include $(BUILD_SHARED_LIBRARY)
