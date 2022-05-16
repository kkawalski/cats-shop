from marshmallow import fields
from marshmallow.validate import Length

from app import ma


class CatShema(ma.Schema):
    tail = fields.Boolean(dump_default=True)
    letter_cnt = fields.Method("letter_cnt_func")
    name = fields.String(required=True, validate=Length(min=1))
    user_id = fields.Integer(required=True, load_only=True)
    # user = fields.Integer(dump_only=True)

    class Meta:
        fields = (
            'id', 
            'name',
            'tail',
            'letter_cnt',
            'user_id',
            # 'user',
        )

    def letter_cnt_func(self, obj):
        return len(obj.name)

cat_schema = CatShema()
cats_schema = CatShema(many=True)

# from cats.models import Cat
# from users.shemas import user_list_schema


# class CatModelSchema(ma.SQLAlchemyAutoSchema):
#     user = ma.Nested(user_list_schema)
#     user_id = fields.Integer(required=True, load_only=True)

#     class Meta:
#         model = Cat
#         include_fk = True

# cat_model_schema = CatModelSchema()
# cats_model_schema = CatModelSchema(many=True)

