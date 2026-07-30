#include "Utility.h"

#include <fstream>
#include <sstream>
#include <vector>
#include <string>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <unistd.h>
#include <fcntl.h>
#include <dirent.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <android/log.h>

#ifndef LOG_TAG
#define LOG_TAG "ZygiskModule"
#endif

#define LOGI(...) __android_log_print(ANDROID_LOG_INFO, LOG_TAG, __VA_ARGS__)
#define LOGE(...) __android_log_print(ANDROID_LOG_ERROR, LOG_TAG, __VA_ARGS__)

namespace Utility {

std::string readFile(const std::string& path) {
    std::ifstream file(path, std::ios::in | std::ios::binary);
    if (!file.is_open()) {
        return "";
    }
    std::ostringstream ss;
    ss << file.rdbuf();
    return ss.str();
}

bool writeFile(const std::string& path, const std::string& content) {
    std::ofstream file(path, std::ios::out | std::ios::binary);
    if (!file.is_open()) {
        return false;
    }
    file << content;
    return file.good();
}

std::string getProcessName() {
    char path[128];
    snprintf(path, sizeof(path), "/proc/%d/cmdline", getpid());
    int fd = open(path, O_RDONLY);
    if (fd < 0) {
        return "";
    }
    char buffer[256] = {0};
    ssize_t bytesRead = read(fd, buffer, sizeof(buffer) - 1);
    close(fd);
    if (bytesRead <= 0) {
        return "";
    }
    buffer[bytesRead] = '\0';
    return std::string(buffer);
}

} // namespace Utility
