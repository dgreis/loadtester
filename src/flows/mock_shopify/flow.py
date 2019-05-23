from src.actions.common_actions import *
from src.actions.ecommerce import *


flow = [  Navigate_To_Landing_Page
        , Select_Items
        , View_And_Add_Products_To_Cart
        , Proceed_To_Checkout
        , Fill_Out_Personal_Information
        , Continue_To_Payment_Method
        , Fill_Out_Bogus_Gateway_Details
        , Place_Order
        , Leave_After_Confirmation
       ]