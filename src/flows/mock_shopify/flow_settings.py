TLD = "https://greis-mock-ecom.myshopify.com"
INVENTORY_URL_PREFIX = '/products/'
#GA_TRACKING_ID = "UA-109607513-3"
TEST = True

USER_HEADLESS = False

EXPERIMENT_ACTIVE = False
#EXPERIMENT_NAME = 'hidden_coupon'

#DBC_DATABASE = 'wordpress'
#DBC_UNIX_SOCKET = '/Applications/MAMP/tmp/mysql/mysql.sock'

N = 1

SHOP_SIZE = 19
BASKETSIZE_LAMBDA = 3
PREFSHAPEPARAMS = { 'ALPHA' : 2.03, 'BETA': 4.67 }

USE_ONLY_PRODUCT_IDS = False
PRODUCT_BACKEND = 'file'
PRODUCT_BACKEND_ARGS = { 'PRODUCT_FILE_LOC' : '/Users/davidgreis/Documents/Personal'\
                         '/Data_Projects/mock-shopify-site/product-csvs-master/apparel.csv'}

SEQUENCE_VIEW_ADD_PRODUCTS = ['Navigate_To_Product_Page',
                              'Add_Item_To_Cart_From_Product_Page',
                              'Update_Quantity_On_Product_Page'
                              ]

ADD_TO_CART_TEXT = 'add'

UPDATE_QUANTITY_BY = 'name'
UPDATE_QUANTITY_TEXT = 'updates[]'

CHECKOUT_ELEMENT_BY = 'name'
CHECKOUT_ELEMENT_TEXT = "checkout"

PERSONAL_INFO_ELEMENT_ID_MAP = {
     'First Name': 'checkout_shipping_address_first_name',
     'Last Name': 'checkout_shipping_address_last_name',
     'Street': 'checkout_shipping_address_address1',
     'City': 'checkout_shipping_address_city',
     'Zip': 'checkout_shipping_address_zip',
     'Email': 'checkout_email_or_phone'
}

BILLING_COUNTRY_BY = 'id'
BILLING_COUNTRY_TEXT = 'checkout_shipping_address_country'

BILLING_STATE_FILTER_BY = 'id'
BILLING_STATE_FILTER_TEXT = 'checkout_shipping_address_province'

BILLING_STATE_SELECT_BY = 'id'
BILLING_STATE_SELECT_TEXT = 'continue_button'

PLACE_ORDER_BUTTON_ID = 'continue_button'

CONFIRMATION_URL_TEXT = 'thank_you'


