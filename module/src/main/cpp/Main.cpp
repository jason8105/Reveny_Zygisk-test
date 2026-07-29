#include <jni.h>
#include <unistd.h>
#include <android/log.h>
#include "zygisk.hpp"

#define LOGD(...) __android_log_print(ANDROID_LOG_DEBUG, "RevenyZygisk", __VA_ARGS__)

using zygisk::Api;
using zygisk::AppSpecializeArgs;
using zygisk::ServerSpecializeArgs;

class RevenyZygiskModule : public zygisk::ModuleBase {
public:
    void onLoad(Api *api, JNIEnv *env) override {
        this->api = api;
        this->env = env;
    }

    void preAppSpecialize(AppSpecializeArgs *args) override {
    }

    void postAppSpecialize(const AppSpecializeArgs *args) override {
    }

    void preServerSpecialize(ServerSpecializeArgs *args) override {
    }

    void postServerSpecialize(const ServerSpecializeArgs *args) override {
    }

private:
    Api *api;
    JNIEnv *env;
};

REGISTER_ZYGISK_MODULE(RevenyZygiskModule)
