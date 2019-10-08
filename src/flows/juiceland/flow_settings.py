
TLD = "https://www.googletagmanager.com/start_preview/gtm?uiv2&id=GTM-5VXXQFT&check_preview_status=1&gtm_auth=mvWyCGu2Lp9PiKlMnTlMIw&gtm_preview=env-96&gtm_debug=&url=https%3A%2F%2Fordering.app%2Fjuiceland%2Fadstesting%2F"
INVENTORY_URL_PREFIX = '/products/'
#GA_TRACKING_ID = "UA-109607513-3"
GTM_PASSTHROUGH_LINK = "https://ordering.app/juiceland/adstesting/"
TEST = True

USER_HEADLESS = False

EXPERIMENT_ACTIVE = True
EXPERIMENT_NAME = 'funnel_attrition'

N = 1

MENU_ITEMS = [('Test Item','Test Item1')]

USE_ONLY_PRODUCT_IDS = False
PRODUCT_BACKEND = 'file'
PRODUCT_BACKEND_ARGS = { 'PRODUCT_FILE_LOC' : '/Users/davidgreis/Documents/Personal'\
                         '/Data_Projects/mock-shopify-site/product-csvs-master/apparel.csv'}

SEQUENCE_VIEW_ADD_PRODUCTS = ['Navigate_To_Product_Page',
                              'Add_Item_To_Cart_From_Product_Page',
                              'Update_Quantity_On_Product_Page'
                              ]

ADD_TO_CART_BY = 'id'
ADD_TO_CART_TEXT = 'button-cart-add'

UPDATE_QUANTITY_BY = 'name'
UPDATE_QUANTITY_TEXT = 'updates[]'

CHECKOUT_ELEMENT_BY = 'link text'
CHECKOUT_ELEMENT_TEXT = "Checkout"

PERSONAL_INFO_ELEMENT_ID_MAP = {
     'Name': 'customer_name',
     'Phone Number': 'customer_phone',
     'Email': 'customer_email'
}


PLACE_ORDER_BUTTON_ID = 'send-order'

CONFIRMATION_URL_TEXT = 'receipt'

