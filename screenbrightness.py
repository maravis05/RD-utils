
#requires wmi module to be installed
#"pip install wmi"

#THIS WILL ONLY WORK ON CERTAIN DISPLAYS, I.E. THOSE THAT WINDOWS CAN ACCESS

import wmi

#set desired screen brightness as a percentage
percent_bright = 100

wmi.WMI(namespace='wmi').WmiMonitorBrightnessMethods()[0].WmiSetBrightness(percent_bright,0)

