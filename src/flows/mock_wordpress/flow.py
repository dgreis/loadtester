from src.actions.common_actions import *
from src.actions.ecommerce import *


flow = [  Navigate_To_Landing_Page
        , Select_Items
        , View_And_Add_Products_To_Cart
        , View_Cart
        , Possibly_Redeem_Coupon
        , Proceed_To_Checkout
        , Fill_Out_Personal_Information
        , Fill_Out_Stripe_CC_Details
        , Place_Order
        , Leave_After_Confirmation
       ]