#include "Utility.h"

#include <fstream>
#include <sstream>
#include <iostream>
#include <algorithm>
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/types.h>

namespace Utility {

bool readFile(const std::string& path, std::string& out) {
    std::ifstream file(path, std::ios::in | std::ios::binary);
    if (!file.is_open()) {
        return false;
    }
    std::ostringstream ss;
    ss << file.rdbuf();
    out = ss.str();
    return true;
}

bool writeFile(const std::string& path, const std::string& content) {
    std::ofstream file(path, std::ios::out | std::ios::binary);
    if (!file.is_open()) {
        return false;
    }
    file << content;
    return true;
}

std::vector<std::string> split(const std::string& str, char delimiter) {
    std::vector<std::string> tokens;
    std::string token;
    std::istringstream tokenStream(str);
    while (std::getline(tokenStream, token, delimiter)) {
        tokens.push_back(token);
    }
    return tokens;
}

} // namespace Utility
