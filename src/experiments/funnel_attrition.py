from collections import OrderedDict

USER_EXPERIMENT_SETTINGS = OrderedDict([
    ('default',
     {
         'possibly_add_menu_items_to_cart' :
             [('add_menu_items_to_cart',1.0),('bounce', 0.0)],
         'possibly_adjust_cart':
             [('adjust_cart',1.0), ('bounce', 0.0)],
         'possibly_toa_proceed_to_checkout':
             [('toa_proceed_to_checkout',1.0), ('bounce', 0.0)],
         'possibly_fill_in_ordering_app_payment_details':
             [('fill_in_ordering_app_payment_details',1.0),('bounce',0.0)]
     }
    )
])