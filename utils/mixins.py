from django.core.cache import cache
import pickle


class CachedViewMixin:
    cache_timeout = 30

    def get_cache_key(self, request):
        """Genera una clave de caché única basada en la URL y el usuario autenticado (si aplica)."""
        if not request.user or not request.user.is_authenticated:
            return None  # No cachear respuestas de usuarios anónimos

        return f"{self.__class__.__name__}:{request.user.id}:{request.get_full_path()}"

    def dispatch(self, request, *args, **kwargs):
        """Intercepta la petición y decide si usa caché o la invalida."""

        cache_key = self.get_cache_key(request)
        # Solo usar caché si la clave de caché existe
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            cached_response = cache.get(cache_key)
            if cached_response:
                return pickle.loads(cached_response)

            response = super().dispatch(request, *args, **kwargs)

            if response.status_code == 200:
                if hasattr(response, "render") and callable(response.render):
                    response.render()
                cache.set(cache_key, pickle.dumps(response), timeout=self.cache_timeout)

            return response
        # Si es un método que modifica datos, borra caché
        response = super().dispatch(request, *args, **kwargs)
        if cache_key:
            self.clear_cache(request)
        return response

    def clear_cache(self, request):
        """Elimina la caché asociada al usuario actual para evitar datos desactualizados."""
        user_id = request.user.id if request.user.is_authenticated else "anonymous"
        cache.delete_pattern(f"{self.__class__.__name__}:{user_id}:*")
