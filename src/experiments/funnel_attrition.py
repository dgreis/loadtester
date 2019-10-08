from collections import OrderedDict

USER_EXPERIMENT_SETTINGS = OrderedDict([
    ('default',
     {
         'possibly_add_menu_items_to_cart' :
             [('add_menu_items_to_cart',1.0),('bounce', 0.0)],
         'possibly_proceed_to_checkout':
             [('proceed_to_checkout',1.0), ('bounce', 0.0)],
         'possibly_pay_there_ordering_app':
             [('pay_there_ordering_app',1.0),('bounce',0.0)]
     }
    )
])