# Copyright (c) 2025 M. Fairbanks
#
# This source code is licensed under the Apache License, Version 2.0, found in the
# LICENSE file in the root directory of this source tree.

from m9lib import uControl, uLoggerLevel

from com_project import *

control = uControl("ProjectTemplate", "m9lib-project.ini")
control.GetLogger().SetWriteLevel(uLoggerLevel.DETAILS)
control.GetLogger().SetPrint(Print=True, Level=uLoggerLevel.INFO, Color=True)
control.Execute()
