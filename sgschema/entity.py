from .field import Field


class Entity(object):
    
    def __init__(self, schema, name):
        
        self.schema = schema
        self.name = name
        
        self.fields = {}
        self.field_aliases = {}
        self.field_tags = {}

    def _get_or_make_field(self, name):
        try:
            return self.fields[name]
        except KeyError:
            return self.fields.setdefault(name, Field(self, name))

    def _reduce_raw(self, schema, raw_entity):
        pass

    def _dump(self):
        return dict((k, v) for k, v in (
            ('fields', self.fields),
            ('field_aliases', self.field_aliases),
            ('field_tags', self.field_tags),
        ) if v)

    def _load(self, raw):
        for name, value in raw.pop('fields', {}).iteritems():
            self._get_or_make_field(name)._load(value)
        self.field_aliases.update(raw.pop('field_aliases', {}))
        self.field_tags.update(raw.pop('field_tags', {}))
        if raw:
            raise ValueError('unknown entity keys: %s' % ', '.join(sorted(raw)))
