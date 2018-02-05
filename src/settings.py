#Settings for GA Test Simulation

N = 1000
URL = "http://127.0.0.1:8888"

LOGGING_FORMAT = "%(asctime)-15s: %(message)s"

variant_map = {
    u'/' : 'original',
    u'/index-1.html' : 'variant1'
}

variant_thresholds = {
    'original': 0.5,
    'variant1': 0.7
}
