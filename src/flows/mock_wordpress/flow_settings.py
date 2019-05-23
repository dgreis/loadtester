TLD = "http://localhost.domain:8888/wordpress/shop/"
INVENTORY_URL_PREFIX = '/product/.'
GA_TRACKING_ID = "UA-109607513-3"
TEST = True

USER_HEADLESS = False

EXPERIMENT_ACTIVE = False
EXPERIMENT_NAME = 'hidden_coupon'

DBC_DATABASE = 'wordpress'
DBC_UNIX_SOCKET = '/Applications/MAMP/tmp/mysql/mysql.sock'

N = 1

SHOP_SIZE = 18
BASKETSIZE_LAMBDA = 3
PREFSHAPEPARAMS = { 'ALPHA' : 2.03, 'BETA': 4.67 }

USE_ONLY_PRODUCT_IDS = False
#PRODUCT_ID_OFFSET = 179 #TODO: Can this be removed?
PRODUCT_BACKEND = 'database'
PRODUCT_BACKEND_ARGS = { 'PRODUCT_ALIAS_QUERY' : "select ID, post_name from wordpress.wp_posts " \
                                                 "where post_type IN ('product')"
                        }

SEQUENCE_VIEW_ADD_PRODUCTS = ['Navigate_To_Product_Page'
                            , 'Update_Quantity_On_Product_Page'
                            , 'Add_Item_To_Cart_From_Product_Page'
                            , 'Navigate_Back'
                             ]

ADD_TO_CART_TEXT = 'add-to-cart'

UPDATE_QUANTITY_BY = 'name'
UPDATE_QUANTITY_TEXT = 'quantity'

CHECKOUT_ELEMENT_BY = 'link text'
CHECKOUT_ELEMENT_TEXT = "Checkout"

PERSONAL_INFO_ELEMENT_ID_MAP = {
     'First Name': 'billing_first_name',
     'Last Name': 'billing_last_name',
     'Street': 'billing_address_1',
     'City': 'billing_city',
     'Zip': 'billing_postcode',
     'Phone': 'billing_phone',
     'Email': 'billing_email'
}

BILLING_COUNTRY_BY = 'class name'
BILLING_COUNTRY_TEXT = 'select2-selection'

BILLING_STATE_FILTER_BY = 'xpath'
BILLING_STATE_FILTER_TEXT = '//span[@aria-labelledby="select2-billing_state-container"]'

BILLING_STATE_SELECT_BY = 'xpath'
BILLING_STATE_SELECT_TEXT = '//li[@class="select2-results__option select2-results__option--highlighted"]'

PLACE_ORDER_BUTTON_ID = 'place_order'
CONFIRMATION_URL_TEXT = 'order-received'


