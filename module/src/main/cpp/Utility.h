#ifndef UTILITY_H
#define UTILITY_H

#include <string>
#include <vector>
#include <cstdint>
#include <cstddef>
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <dirent.h>
#include <android/log.h>

#ifndef LOG_TAG
#define LOG_TAG "RevenyZygisk"
#endif

#define LOGD(...) __android_log_print(ANDROID_LOG_DEBUG, LOG_TAG, __VA_ARGS__)
#define LOGE(...) __android_log_print(ANDROID_LOG_ERROR, LOG_TAG, __VA_ARGS__)
#define LOGI(...) __android_log_print(ANDROID_LOG_INFO, LOG_TAG, __VA_ARGS__)

namespace Utility {
    bool readFile(const std::string& path, std::string& out);
    bool writeFile(const std::string& path, const std::string& content);
    bool fileExists(const std::string& path);
    std::string getPackageName();
}

#endif // UTILITY_H
