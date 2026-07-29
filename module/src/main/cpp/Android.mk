LOCAL_PATH := $(call my-dir)

include $(CLEAR_VARS)

LOCAL_MODULE := module

LOCAL_CPPFLAGS := -std=c++17 -fpermissive -Wno-error -fdeclspec -fexceptions -frtti -fvisibility=hidden
LOCAL_CFLAGS := -fvisibility=hidden -Wno-error

# 1. Saare Includes
LOCAL_C_INCLUDES := $(LOCAL_PATH) \
                    $(LOCAL_PATH)/Include \
                    $(LOCAL_PATH)/Headers \
                    $(LOCAL_PATH)/External/ImGui \
                    $(LOCAL_PATH)/External/KittyMemory \
                    $(LOCAL_PATH)/External/Dobby

# 2. Main C++ Files
LOCAL_SRC_FILES := \
    Main.cpp \
    ModMenu.cpp \
    Drawing.cpp \
    Utility.cpp

LOCAL_LDLIBS := -llog -landroid -lEGL -lGLESv2

# 3. External Libraries Link
LOCAL_STATIC_LIBRARIES := libimgui libkitty libdobby

include $(BUILD_SHARED_LIBRARY)

# 4. SABSE IMPORTANT: External Android.mk ko sabse last mein call karo!
# Isse LOCAL_PATH overwrite nahi hoga aur files sahi jagah dhoondhi jayengi.
include $(LOCAL_PATH)/External/Android.mk
