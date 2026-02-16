class KeyGenerator:
    USER = "user"
    WORKOUT = "workout"

    def __init__(self, entity):
        switcher = {
            self.USER: "user",
            self.WORKOUT: "workout",
        }
        self.prefix = switcher.get(entity, "default")

    @staticmethod
    def gen_key(prefix, key, params=None):
        key_without_params = f"{prefix}:{key}"

        if params:
            hash_key = hash(params)
            return f"{key_without_params}:{hash_key}"

        return key_without_params

    def standard_one(self, key, params=None):
        entity_key = f"{self.entity}:{key}"
        # example:
        # users:user:<key>:<params_hash>
        return self.gen_key(self.prefix, entity_key, params)

    def standard_many(self, key=None, params=None):
        entities_key = f"{self.prefix}" if not key else f"{self.prefix}:{key}"
        # example:
        # users:users:<key>:<params_hash>
        return self.gen_key(self.prefix, entities_key, params)
