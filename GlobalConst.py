import os

from modules.manage_graph import ManageGraph
from modules.serial_interface import SerialInterface

dir_TGView = os.path.dirname(os.path.abspath(__file__)) + '/TGView'  # /home/pi/TGView
root_path = os.path.dirname(os.path.abspath(__file__))


# assign fonts for various GUI components
LARGEST_FONT = ("Lato", 68, 'bold')
LARGER_FONT = ("Lato", 45, 'bold')
LARGE_FONT = ("Lato", 28, 'bold')
SMALL_FONT = ("Lato", 20, 'bold')
SMALLER_FONT = ("Lato", 18)
SMALLERR_FONT = ("Lato", 14)
SMALLEST_FONT = ("Lato", 8)
QAM_GREEN = "#7fa6a3"  ###html color code for QAM green

manageGraphData = ManageGraph()
s_interface = SerialInterface()

start_record_time = ""
directory = ""
