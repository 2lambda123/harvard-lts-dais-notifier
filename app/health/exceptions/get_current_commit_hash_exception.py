class GetCurrentCommitHashException(Exception):
    def __init__(self, reason: str) -> None:
        self.message = f"There was an error when getting current git commit hash. Reason was: {reason}"
        super().__init__(self.message)
