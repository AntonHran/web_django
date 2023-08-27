from django import template

from ..models import Tag, MtM


register = template.Library()


def get_tags(mtm_obj):
    tags_id = MtM.objects.filter(quote_id=mtm_obj).all()
    return [Tag.objects.get(id=tag.tag_id).name for tag in tags_id]


register.filter("tags_", get_tags)
