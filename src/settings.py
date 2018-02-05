#Settings for GA Test Simulation

N = 10
URL = "http://127.0.0.1:8888"

LOGGING_FORMAT = "%(asctime)-15s: %(message)s"

variant_list =  ['original', 'variant1']


variant_thresholds = {
    'original': 0.5,
    'variant1': 0.7
}
