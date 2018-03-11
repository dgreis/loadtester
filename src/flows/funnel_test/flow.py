from actions import *
from src.flows.click_button.actions import Click_Button
from src.flows.common_actions import Navigate_To_Landing_Page, Determine_Treatment

flow = [Navigate_To_Landing_Page,
        Determine_Treatment,
        Click_Button,
        Wait_For_Pic,
        Possibly_Bounce,
        Click_Add_To_Cart,
        Wait_To_Claim_Gift,
        Claim_Gift]