from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from users.models import User
from users.views import key_gen, redis_cache


@receiver(post_save, sender=User)
def clear_cache_on_save(instance, created, **kwargs):
    print("+++++++++++++++clear_cache_on_save")
    print(kwargs)
    cache_key_entities = key_gen.standard_many()

    if created:
        redis_cache.delete(cache_key_entities)
        return

    cache_key_entity = key_gen.standard_one(instance.pk)
    redis_cache.delete_many([cache_key_entities, cache_key_entity])


@receiver(post_delete, sender=User)
def clear_cache_on_delete(instance, **kwargs):
    cache_key_entities = key_gen.standard_many()
    cache_key_entity = key_gen.standard_one(instance.pk)
    redis_cache.delete_many([cache_key_entities, cache_key_entity])
