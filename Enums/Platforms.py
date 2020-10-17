class Platforms:
    def __init__(self, platform):
        self.platforms = {
            "Xbox": 1,
            "Playstation": 2,
            "Steam": 3,
            "Stadia": 5
        }

        self.set_platform(platform)

    @property
    def platform_str(self):
        return list(self.platforms.keys())[list(self.platforms.values()).index(self.platform)]

    def set_platform(self, platform):
        self.platform = self.platforms[platform]
