import os

import followthemoney
from followthemoney.model import Model as FTMModel
from followthemoney.util import set_model_locale

__version__ = '1.18.2'


class RingFTMModel(FTMModel):
    def load_dir(self, schema_path):
        for (path, _, filenames) in os.walk(schema_path):
            for filename in filenames:
                self._load(os.path.join(path, filename))
        self.generate()


model_path = os.path.dirname(followthemoney.__file__)
model_path = os.path.join(model_path, 'schema')

# Data model singleton
model = RingFTMModel(model_path)
model.load_dir(os.path.join(os.path.dirname(__file__), "ftm_schema"))


def get_degradation_mapping():
    from followthemoney import model as base_ftm_model
    schemata = base_ftm_model.schemata.values()

    res = {}
    for m in model:
        schema = m
        while True:
            if schema in schemata:
                break

            if not schema.extends:
                raise Exception("No basic schema found")

            # TODO: breadth first search?
            for parent in schema.extends:
                if parent in schemata:
                    schema = parent

                    break
        res[m.name] = schema

    return res
        # if schema != ftm.schema:
        #     ftm.schema = schema


__all__ = [model, set_model_locale]
