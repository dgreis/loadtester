from src.flows.common_actions import Navigate_To_Landing_Page
from actions import *


flow = [ Navigate_To_Landing_Page
        ,Empty_Cart
        ,Select_Items
        ,Add_Items_To_Cart
        ,Proceed_To_Checkout
        ,Execute_Purchase
        ,Leave_After_Confirmation
        ]