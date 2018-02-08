#Settings for GA Test Simulation

N = 500
TLD = "http://127.0.0.1:8888"

LOGGING_FORMAT = "%(asctime)-15s, %(message)s"

variant_list =  ['original', 'variant1']


variant_click_thresholds = {
    'original': 0.8,
    'variant1': 0.95
}

variant_bounce_thresholds = {
    'original': 0.2,
    'variant1': 0
}
