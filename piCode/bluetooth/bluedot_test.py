"""
Found from the https://bluedot.readthedocs.io documentation
    1/27/2019
"""

from bluedot import BlueDot
bd = BlueDot()
bd.wait_for_press()
print("You pressed the blue dot!")
