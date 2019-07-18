from src.actions.common_actions import *
from src.actions.ecommerce import *
from src.actions.ordering_app import *


flow = [  Navigate_To_Landing_Page,
          Click_Through_GTM_Preview_Mode,
          Add_Menu_Items_To_Cart,
          Adjust_Cart,
          Proceed_To_Checkout,
          Ordering_App_Payment_Details,
          Place_Order
       ]