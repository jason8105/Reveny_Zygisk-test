#include "Utility.h"
#include <fstream>
#include <sstream>
#include <cstring>
#include <cstdlib>
#include <cstdint>
#include <cstddef>
#include <algorithm>
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <dirent.h>
#include <android/log.h>

namespace Utility {

bool readFile(const std::string& path, std::string& out) {
    int fd = open(path.c_str(), O_RDONLY | O_CLOEXEC);
    if (fd < 0) return false;
    char buffer[1024];
    ssize_t bytesRead;
    out.clear();
    while ((bytesRead = read(fd, buffer, sizeof(buffer))) > 0) {
        out.append(buffer, bytesRead);
    }
    close(fd);
    return true;
}

bool writeFile(const std::string& path, const std::string& content) {
    int fd = open(path.c_str(), O_WRONLY | O_CREAT | O_TRUNC | O_CLOEXEC, 0666);
    if (fd < 0) return false;
    ssize_t bytesWritten = write(fd, content.c_str(), content.size());
    close(fd);
    return bytesWritten == static_cast<ssize_t>(content.size());
}

bool fileExists(const std::string& path) {
    struct stat buffer;
    return (stat(path.c_str(), &buffer) == 0);
}

std::string getPackageName() {
    std::string cmdline;
    if (readFile("/proc/self/cmdline", cmdline)) {
        size_t pos = cmdline.find('\0');
        if (pos != std::string::npos) {
            return cmdline.substr(0, pos);
        }
        return cmdline;
    }
    return "";
}

} // namespace Utility
