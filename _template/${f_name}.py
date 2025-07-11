from m9lib import uControl, uLoggerLevel

# It is not necessary to create a custom uControl.  If you do not wish to customize this functionality,
#   delete this class and use the commented line below.
class ${Control}(uControl):
    def __init__(self, Config, Params=None):
        super().__init__("${Control}", Config, Params)

    def imp_ini_command (self, in_command):
        self.GetLogger().WriteLine(f"[+YELLOW]imp_ini_command({in_command.GetName()}:{in_command.GetId()})[+]")
        # return False to fail command initialization and skip command execution
        return True

    def imp_prepare (self):
        self.GetLogger().WriteLine(f"[+YELLOW]imp_prepare()[+]")
        # perform application-level initialization before executing any commands; return False to fail execution
        return True

    def imp_finalize (self):
        self.GetLogger().WriteLine(f"[+YELLOW]imp_finalize()[+]")
        # None makes the final result based on command success; return any value to customize this behavior
        return None

from c_${f_name} import *

uControl.PrintFailures()
control = ${Control}(r"${f_name}.ini")
# control = uControl("${Control}", r"${f_name}.ini") # use this line if a custom uControl is not desired
control.GetLogger().SetPrint(Print=True, Level=uLoggerLevel.INFO, Color=True)
control.Execute ()

# Note the following about error messages.  There are three categories of error messages:
# - System level uControl messages
# - System level uConfig messages
# - User level command messages

# The SetPrint() method enables printing of the log to the console based on the specified logging level
# The PrintFailures() method turns on console printing of uControl and uConfig failures
# This will result in uControl and uConfig failures displaying twice in the console, but only once in the log

print(f"Final result: {control.GetFinalResult()}")
results = control.GetResults(Id="run")
for run_result in results:
    print(f"[{run_result.GetSpecification()}]: {run_result.GetResult()}")
print(f"Execution summary: {control.GetSummary()}")
