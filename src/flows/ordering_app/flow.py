from src.actions.common_actions import *
from src.actions.ecommerce import *
from src.actions.ordering_app import *


flow = [  Navigate_To_Landing_Page,
          Click_Through_GTM_Preview_Mode,
          Possibly_Add_Menu_Items_To_Cart,
          Possibly_Adjust_Cart,
          Possibly_Proceed_To_Checkout,
          Possibly_Fill_In_Ordering_App_Payment_Details,
          Place_Order,
          Leave_After_Confirmation
        ]