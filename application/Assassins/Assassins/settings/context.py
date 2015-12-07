from django.conf import settings

def compress(request):
	return {
		'compress': settings.COMPRESS_ENABLED,
		'REQUIRE_DEBUG': settings.REQUIRE_DEBUG,
		'HEAP_TOKEN': settings.HEAP_TOKEN
	}