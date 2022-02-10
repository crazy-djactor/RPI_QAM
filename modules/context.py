from datetime import datetime
from tkinter import StringVar


class TestContext:
    test_startTimeLabelValue = ''

    def __init__(self):
        directory = ""


class AppContext:
    directory = ""
    pathF = ""
    newStartTime = None
    newStopTime = None

    oldStartTimeRH2O = None
    oldStartTimeRO2 = None

    oldStopTimeRH2O = None
    oldStopTimeRO2 = None

    newStartTimeO2 = None
    newStopTimeO2 = None
    oldStartTimeO2 = None
    oldStopTimeO2 = None

    o2bAvgEdit = ""
    o2bAvgUnedit = ""
    o2bMaxEdit = ""
    o2bMaxUnedit = ""
    o2bFinalEdit = ""
    o2bFinalUnedit = None

    h2obMaxUnedit = ""
    h2obAvgEdit = ""
    h2obAvgUnedit = ""
    h2obFinalEdit = ""
    h2obFinalUnedit = ""

    edit_test_folder = ""
    opencv_toplevel = None      # top

    start_time = datetime.now()
    start_timee = start_time.strftime("%m_%d_%y_%H.%M.%S")
    start_timeez = start_time.strftime("%m/%d/%y @ %I:%M %p")

    start_timet = None

    O2xbReset = None

    O2xb = None
    O2yb = None

    testingStatusMessageMeeco = None
    testingStatusMessageDeltaf = None

    newTime_durationH2O = None
    time_elapsedH2O = None

    last_drawO2time = None
    last_drawH2otime = None

    o2Valuelist = []
    h2oValuelist = []

    o2MeanValue = ''
    o2MeanValueVar = ''
    o2MaxValue = ''
    o2MaxValueVar = ''

    o2FinalValue = ''
    o2FinalValueVar = ''

    h2oMeanValue = ''
    h2oMeanValueVar = ''
    h2oMaxValue = ''
    h2oMaxValueVar = ''

    h2oFinalValue = ''
    h2oFinalValueVar = ''

    currento2 = None
    currenth2o = None

    test_stop_time = datetime.now().strftime("%m_%d_%y_%H.%M.%S")
    test_start_time = datetime.now().strftime("%m_%d_%y_%H.%M.%S")

    current_savePath = ''

    time_elapsed_string = ''
    time_elapsed = None

    def __init__(self):
        directory = ""

