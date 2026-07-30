#include <jni.h>
#include <android/log.h>

#define LOG_TAG "Reveny"
#define LOGI(...) __android_log_print(ANDROID_LOG_INFO, LOG_TAG, __VA_ARGS__)

#if __has_include("zygisk.hpp")
#include "zygisk.hpp"

using zygisk::Api;
using zygisk::AppSpecializeArgs;
using zygisk::ServerSpecializeArgs;

class RevenyModule : public zygisk::ModuleBase {
public:
    void onLoad(Api *api, JNIEnv *env) override {
        this->api = api;
        this->env = env;
    }

    void preAppSpecialize(AppSpecializeArgs *args) override {
    }

    void postAppSpecialize(const AppSpecializeArgs *args) override {
    }

private:
    Api *api = nullptr;
    JNIEnv *env = nullptr;
};

REGISTER_ZYGISK_MODULE(RevenyModule)

#else

extern "C" jint JNI_OnLoad(JavaVM* vm, void* reserved) {
    LOGI("Reveny module initialized");
    return JNI_VERSION_1_6;
}

#endif
