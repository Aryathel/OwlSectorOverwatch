class Orbit:
    def __init__(self, locale):
        self.translations = {
            "en": "In Orbit",
            "pl": "Na orbicie",
            "pt-br": "Em órbita",
            "es": "En orbita",
            "fr": "En orbite",
            "en-mx": "En orbita",
            "de": "Im Orbit",
            "it": "In orbita",
            "ru": "На орбите",
            "ko": "궤도에서",
            "ja": "軌道上",
            "zh-cht": "在軌道上",
            "zh-chs": "在轨道上"
        }

        self.set_orbit_text(locale)

    def set_orbit_text(self, locale):
        self.orbit_text = self.translations[locale]
