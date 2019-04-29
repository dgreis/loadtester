TLD = "http://localhost:8888/wordpress/shop/"
GA_TRACKING_ID = "UA-109607513-3"
TEST = True

EXPERIMENT_ACTIVE = False
EXPERIMENT_NAME = 'hidden_coupon'

DBC_DATABASE = 'wordpress'
DBC_UNIX_SOCKET = '/Applications/MAMP/tmp/mysql/mysql.sock'

N = 1

SHOP_SIZE = 18
BASKETSIZE_LAMBDA = 3
PREFSHAPEPARAMS = { 'ALPHA' : 2.03, 'BETA': 4.67 }

USE_ONLY_PRODUCT_IDS = False
PRODUCT_ID_OFFSET = 179
PRODUCT_ALIAS_QUERY = "select ID, post_name from wordpress.wp_posts " \
                      "where post_type IN ('product')"