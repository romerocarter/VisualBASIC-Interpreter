import lookup_table


class TokenObj:
    def __init__(self, val='', tok=lookup_table.UNKNOWN):
        self._value = val
        self._token = tok

    def get_val(self):
        return self._value

    def get_token(self):
        return self._token
