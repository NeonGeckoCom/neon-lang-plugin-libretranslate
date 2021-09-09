import requests

from ovos_plugin_manager.templates.language import LanguageDetector,\
    LanguageTranslator

from libretranslate_neon_plugin.constants import DEFAULT_LIBRE_HOST

class LibreTranslateDetectPlugin(LanguageDetector):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # host it yourself https://github.com/uav4geo/LibreTranslate
        self.url = self.config.get("libretranslate_host") or DEFAULT_LIBRE_HOST
        self.api_key = self.config.get("key")

    def detect(self, text):
        return self.detect_probs(text)[0]["language"]

    def detect_probs(self, text):
        params = {"q": text}
        if self.api_key:
            params["api_key"] = self.api_key
        return requests.post(self.url, params=params).json()


class LibreTranslatePlugin(LanguageTranslator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # host it yourself https://github.com/uav4geo/LibreTranslate
        self.url = self.config.get("libretranslate_host") or DEFAULT_LIBRE_HOST
        self.api_key = self.config.get("key")

    def translate(self, text, target=None, source=None, url=None):
        source = source or self.default_language
        target = target or self.internal_language
        params = {"q": text,
                  "source": source.split("-")[0],
                  "target": target.split("-")[0]}
        if self.api_key:
            params["api_key"] = self.api_key
        r = requests.post(self.url, params=params).json()
        if r.get("error"):
            return None
        return r["translatedText"]
