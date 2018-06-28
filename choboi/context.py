

class Request:

    @classmethod
    def from_slack_input(cls, slack_input):
        request = cls()