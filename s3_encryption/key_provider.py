from s3_encryption.materials import Materials


class DefaultKeyProvider(object):

    def __init__(self, key, **kwargs):
        desc = kwargs.get('materials_description', {})
        self._encryption_materials = Materials(key=key, description=desc)

    @property
    def encryption_materials(self):
        return self._encryption_materials

    def key_for(self, materials_description):
        return self._encryption_materials.key
