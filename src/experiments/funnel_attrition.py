from collections import OrderedDict

USER_EXPERIMENT_SETTINGS = OrderedDict([
    ('default',
     {
         'possibly_add_menu_items_to_cart' :
             [('add_menu_items_to_cart',0.8),('bounce', 0.2)],
         'possibly_adjust_cart':
             [('adjust_cart',0.6), ('bounce', 0.4)],
         'possibly_proceed_to_checkout':
             [('proceed_to_checkout',0.4), ('bounce', 0.6)],
         'possibly_fill_in_ordering_app_payment_details':
             [('fill_in_ordering_app_payment_details',0.3),('bounce',0.7)]
     }
    )
])