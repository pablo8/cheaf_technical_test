from django.core.cache import cache
import pickle


class CachedViewMixin:
    cache_timeout = 600

    def get_cache_key(self, request):
        """Genera una clave de caché única basada en la URL y el usuario autenticado (si aplica)."""
        user_id = request.user.id if request.user.is_authenticated else "anonymous"
        return f"{self.__class__.__name__}:{user_id}:{request.get_full_path()}"

    def dispatch(self, request, *args, **kwargs):
        """Intercepta la petición y decide si usa caché o la invalida."""
        cache_key = self.get_cache_key(request)

        if request.method in ["GET", "HEAD", "OPTIONS"]:
            cached_response = cache.get(cache_key)
            if cached_response:
                return pickle.loads(cached_response)

            response = super().dispatch(request, *args, **kwargs)
            if hasattr(response, "render") and callable(response.render):
                response.render()

            cache.set(cache_key, pickle.dumps(response), timeout=self.cache_timeout)
            return response

        response = super().dispatch(request, *args, **kwargs)
        self.clear_cache(request)
        return response

    def clear_cache(self, request):
        """Elimina la caché asociada al usuario actual para evitar datos desactualizados."""
        user_id = request.user.id if request.user.is_authenticated else "anonymous"
        cache.delete_pattern(f"{self.__class__.__name__}:*")
