#include <jni.h>
#include <android/log.h>
#include "zygisk.hpp"

#define LOG_TAG "RevenyZygisk"
#define LOGD(...) __android_log_print(ANDROID_LOG_DEBUG, LOG_TAG, __VA_ARGS__)

class RevenyModule : public zygisk::ModuleBase {
public:
    void onLoad(zygisk::Api *api, JNIEnv *env) override {
        this->api = api;
        this->env = env;
        LOGD("Reveny Zygisk module loaded successfully");
    }

    void preAppSpecialize(zygisk::AppSpecializeArgs *args) override {
        LOGD("preAppSpecialize execution");
    }

    void postAppSpecialize(const zygisk::AppSpecializeArgs *args) override {
        LOGD("postAppSpecialize execution");
    }

private:
    zygisk::Api *api = nullptr;
    JNIEnv *env = nullptr;
};

REGISTER_ZYGISK_MODULE(RevenyModule)
