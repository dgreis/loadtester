#Settings for GA Test Simulation

N = 500
TLD = "http://localhost:8888/wordpress/shop/"
GA_TRACKING_ID = "UA-109607513-3"

LOGGING_FORMAT = "time:%(asctime)-15s, %(message)s"

variant_list =  ['original', 'variant1']


variant_click_thresholds = {
    'original': 0.8,
    'variant1': 0.95
}

variant_bounce_thresholds = {
    'original': 0.2,
    'variant1': 0
}
