#include "ModMenu.h"
#include <jni.h>
#include <string>
#include <vector>
#include <thread>
#include <chrono>
#include <android/log.h>

#define LOG_TAG "RevenyModMenu"
#define LOGI(...) __android_log_print(ANDROID_LOG_INFO, LOG_TAG, __VA_ARGS__)
#define LOGE(...) __android_log_print(ANDROID_LOG_ERROR, LOG_TAG, __VA_ARGS__)

namespace ModMenu {
    void Init() {
        LOGI("ModMenu initialized");
    }

    void Draw() {
        // UI render routine
    }
}
