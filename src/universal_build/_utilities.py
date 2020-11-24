class DashInsensitiveDict(dict):
    @classmethod
    def _k(cls, key):  # type: ignore
        return key.lower().strip().replace("-", "_")

    def __init__(self, *args, **kwargs):  # type: ignore
        super(DashInsensitiveDict, self).__init__(*args, **kwargs)
        self._convert_keys()

    def __getitem__(self, key):  # type: ignore
        return super(DashInsensitiveDict, self).__getitem__(self.__class__._k(key))

    def __setitem__(self, key, value):  # type: ignore
        super(DashInsensitiveDict, self).__setitem__(self.__class__._k(key), value)

    def __delitem__(self, key):  # type: ignore
        return super(DashInsensitiveDict, self).__delitem__(self.__class__._k(key))

    def __contains__(self, key):  # type: ignore
        return super(DashInsensitiveDict, self).__contains__(self.__class__._k(key))

    def has_key(self, key):  # type: ignore
        return self.__class__._k(key) in super(DashInsensitiveDict, self)

    def pop(self, key, *args, **kwargs):  # type: ignore
        return super(DashInsensitiveDict, self).pop(
            self.__class__._k(key), *args, **kwargs
        )

    def get(self, key, *args, **kwargs):  # type: ignore
        return super(DashInsensitiveDict, self).get(
            self.__class__._k(key), *args, **kwargs
        )

    def setdefault(self, key, *args, **kwargs):  # type: ignore
        return super(DashInsensitiveDict, self).setdefault(
            self.__class__._k(key), *args, **kwargs
        )

    def update(self, E={}, **F):  # type: ignore
        super(DashInsensitiveDict, self).update(self.__class__(E))
        super(DashInsensitiveDict, self).update(self.__class__(**F))

    def _convert_keys(self):  # type: ignore
        for k in list(self.keys()):
            v = super(DashInsensitiveDict, self).pop(k)
            self.__setitem__(k, v)
