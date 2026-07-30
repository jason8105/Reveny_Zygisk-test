#pragma once

#include <string>
#include <vector>
#include <cstdint>
#include <string_view>
#include <android/log.h>

#ifndef LOG_TAG
#define LOG_TAG "ZygiskModule"
#endif

#define LOGD(...) __android_log_print(ANDROID_LOG_DEBUG, LOG_TAG, __VA_ARGS__)
#define LOGE(...) __android_log_print(ANDROID_LOG_ERROR, LOG_TAG, __VA_ARGS__)
#define LOGI(...) __android_log_print(ANDROID_LOG_INFO, LOG_TAG, __VA_ARGS__)

namespace Utility {
    bool readFile(const std::string& path, std::string& out);
    bool writeFile(const std::string& path, const std::string& content);
    std::vector<std::string> split(const std::string& str, char delimiter);
}
