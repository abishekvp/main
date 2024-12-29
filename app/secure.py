from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from django.http import JsonResponse
from django.core.cache import cache
import logging

# Set up a logger for the middleware
logger = logging.getLogger(__name__)

class MainMiddleware:
    """
    Middleware that validates JWT token for requests that modify the database (POST, PUT, DELETE),
    enforces rate limiting, and restricts more than 5 requests from the same IP to the same URL within 1 minute.
    If restricted, the IP will be blocked for 10 minutes.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Skip token validation and rate-limiting for token endpoint
        if request.method in ['POST', 'PUT', 'DELETE'] and not request.path.startswith('/api/token/'):
            
            # 1. Check for Authorization header containing Bearer token
            token = request.headers.get('Authorization', None)
            if token and token.startswith('Bearer '):
                token = token.split(' ')[1]  # Extract the token part
            else:
                return JsonResponse({'detail': 'Authentication token required'}, status=401)

            try:
                # Validate the token
                decoded_token = self.validate_jwt_token(token)
                print(decoded_token, "decoded_token")
                if not decoded_token:
                    return JsonResponse({'detail': 'Invalid or expired token'}, status=401)

            except Exception as e:
                return JsonResponse({'detail': str(e)}, status=401)

            # 2. Rate limiting: Restrict more than 5 requests from the same IP to the same URL within 1 minute
            ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR'))
            if isinstance(ip, str) and ',' in ip:
                ip = ip.split(',')[0]

            url = request.path
            cache_key = f"{ip}:{url}"

            # Check the cache for the number of requests made from this IP to the same URL
            request_count = cache.get(cache_key, 0)

            # Check for blocked IP status first
            blocked_cache_key = f"blocked:{ip}"
            if cache.get(blocked_cache_key):
                return JsonResponse({'detail': 'Too many requests. Please try again after some time.'}, status=403)

            # Restrict requests if more than 5 requests have been made
            if request_count >= 5:
                return JsonResponse({'detail': 'Too many requests. Please try again after some time.'}, status=429)

            # Increase the request count in cache, set expiration time to 1 minute
            cache.set(cache_key, request_count + 1, timeout=60)

            # 3. Block the IP for 10 minutes after exceeding the limit
            if request_count + 1 > 5:
                cache.set(blocked_cache_key, True, timeout=600)  # Block for 10 minutes

        # Continue processing the request
        response = self.get_response(request)
        return response

    def validate_jwt_token(self, token):
        """
        Validate the JWT token using SimpleJWT.
        Returns the decoded token if valid, else returns None.
        """
        print(token, "token")
        # Validate the token using SimpleJWT's AccessToken class
        decoded_token = AccessToken(token)
        print(decoded_token)
        return decoded_token.payload  # Return the decoded payload if the token is valid
