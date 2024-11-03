from prometheus_client import make_wsgi_app, Counter, Gauge
from django.middleware import MiddlewareMixin
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
import time

# Define the metrics
REQUEST_COUNT = Counter('request_count', 'Total request count')
REQUEST_LATENCY = Gauge('request_latency_seconds', 'Request latency in seconds')

class PrometheusMiddleware(MiddlewareMixin):
    def process_request(self, request):
        REQUEST_COUNT.inc()  
        request.start_time = time.time()  

    def process_response(self, request, response):
        latency = time.time() - request.start_time 
        REQUEST_LATENCY.observe(latency)
        return response  