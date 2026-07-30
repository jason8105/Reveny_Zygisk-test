#ifndef UTILITY_H
#define UTILITY_H

#include <string>
#include <vector>
#include <cstdint>
#include <cstddef>
#include <sys/types.h>

namespace Utility {
    std::string readFile(const std::string& path);
    bool writeFile(const std::string& path, const std::string& content);
    std::string getProcessName();
}

#endif // UTILITY_H
