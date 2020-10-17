class Errors:
    def __init_(self):
        self.window_name = "Owl Sector Error"

        self.errors = {
            "invalid_token": "The authentication process has failed. Please re-enter your access credentials to gain entry to Owl Sector systems.",
            "invalid_account": "The account entered does not have security clearance for Owl Sector systems.",
            "server_not_found": "It appears Owl Sector systems are under maintenance. You will have to operate off the grid until systems can be restored.",
            "no_connection": "It appears your location cannot connect to Owl Sector systems. Please wait to re-establish server connection.",
            "battlenet_platform": "It appears you are using an outdated Owl Sector system. Please upgrade your account to newer versions.\n\n(Battlenet is not a valid platform. Users must now be on Steam.)"
        }

    @property
    def error(self, code):
        return self.errors[code]
