#include <jni.h>
#include <android/log.h>
#include "zygisk.hpp"

using zygisk::Api;
using zygisk::AppSpecializeArgs;
using zygisk::ServerSpecializeArgs;

class RevenyZygisk : public zygisk::ModuleBase {
public:
    void onLoad(Api *api, JNIEnv *env) override {
        this->api = api;
        this->env = env;
    }

    void preAppSpecialize(AppSpecializeArgs *args) override {
        __android_log_print(ANDROID_LOG_INFO, "RevenyZygisk", "preAppSpecialize");
    }

    void postAppSpecialize(const AppSpecializeArgs *args) override {
        __android_log_print(ANDROID_LOG_INFO, "RevenyZygisk", "postAppSpecialize");
    }

    void preServerSpecialize(ServerSpecializeArgs *args) override {
        __android_log_print(ANDROID_LOG_INFO, "RevenyZygisk", "preServerSpecialize");
    }

    void postServerSpecialize(const ServerSpecializeArgs *args) override {
        __android_log_print(ANDROID_LOG_INFO, "RevenyZygisk", "postServerSpecialize");
    }

private:
    Api *api;
    JNIEnv *env;
};

REGISTER_ZYGISK_MODULE(RevenyZygisk)
