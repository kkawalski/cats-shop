from marshmallow import fields
from marshmallow.validate import Length

from app import ma
from cats.models import Cat


class CatShema(ma.Schema):
    tail = fields.Boolean(dump_default=True)
    letter_cnt = fields.Method("letter_cnt_func")
    name = fields.String(required=True, validate=Length(min=1))

    class Meta:
        fields = (
            'id', 
            'name',
            'tail',
            'letter_cnt',
        )

    def letter_cnt_func(self, obj):
        return len(obj.name)

cat_schema = CatShema()
cats_schema = CatShema(many=True)


class CatModelSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Cat

cat_model_schema = CatModelSchema()
cats_model_schema = CatModelSchema(many=True)

