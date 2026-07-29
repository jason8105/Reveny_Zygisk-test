/* SPDX-License-Identifier: MIT */

/*
 * Copyright 2021 John Wu
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 */

#pragma once

#include <jni.h>
#include <stdint.h>

#define ZYGISK_API_VERSION 2

namespace zygisk {

struct AppSpecializeArgs {
    jint &uid;
    jint &gid;
    jintArray &gids;
    jint &runtime_flags;
    jobjectArray &rlimits;
    jint &mount_external;
    jstring &se_info;
    jstring &nice_name;
    jboolean &is_child_zygote;
    jstring &instruction_set;
    jstring &app_data_dir;
    jboolean &is_top_app;
    jobjectArray &pkg_data_info_list;
    jobjectArray &whitelisted_data_info_list;
    jboolean &mount_data_dirs;
    jboolean &mount_storage_dirs;
};

struct ServerSpecializeArgs {
    jint &uid;
    jint &gid;
    jintArray &gids;
    jint &runtime_flags;
    jlong &permitted_capabilities;
    jlong &effective_capabilities;
};

enum Option : int {
    FORCE_DENYLIST_UNLOAD = 0
};

class Api {
public:
    // Connect to companion process.
    // Returns a socket file descriptor to the companion process, or -1 on error.
    virtual int connectCompanion() = 0;

    // Control options.
    virtual void setOption(Option opt) = 0;
};

class ModuleBase {
public:
    virtual ~ModuleBase() = default;

    // Called when the module is loaded.
    virtual void onLoad(Api *api, JNIEnv *env) {}

    // Called before/after app specialization.
    virtual void preAppSpecialize(AppSpecializeArgs *args) {}
    virtual void postAppSpecialize(const AppSpecializeArgs *args) {}

    // Called before/after system server specialization.
    virtual void preServerSpecialize(ServerSpecializeArgs *args) {}
    virtual void postServerSpecialize(const ServerSpecializeArgs *args) {}
};

} // namespace zygisk

extern "C" void zygisk_module_entry(zygisk::Api *, zygisk::ModuleBase **);

#define REGISTER_ZYGISK_MODULE(clazz) \
extern "C" void zygisk_module_entry(zygisk::Api *api, zygisk::ModuleBase **module) { \
    *module = new clazz(); \
}
