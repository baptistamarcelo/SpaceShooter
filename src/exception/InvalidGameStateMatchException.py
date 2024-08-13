class InvalidGameStateMatchException(Exception):
    def __init__(self, match_state):
        message = f"game_state.match '{match_state}' is invalid"
        super().__init__(message)
