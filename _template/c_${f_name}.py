from m9lib import uCommand, uCommandResult, uCommandRegistry

# Custom command results are optional; if there is no custom behavior,
#   remove this class from uCommandRegistry.RegisterCommand() to use
#   the built-in class uCommandResult.
class ${Command}Result(uCommandResult):

    def __init__(self):
        super().__init__()

# Your command class name must match the section name in your config file
#   and be registered for uControl to create an instance of your command
#   object.
class ${Command}(uCommand):
    
    def __init__(self):
        super().__init__()
        
    def imp_execute(self, in_preview):
        # This is your main execution function.

        # Command objects are destroyed after execution, but the result
        #   object is maintained by uControl.  Save any relevant data to
        #   the result object.
        result = self.GetResult()

        # Parameters are read from the command section of the
        #   config file.
        self.LogParamString("MyParam is set to [=MyParam]")

        self.LogMessage("${Command} command execution...")

        # Return True, "Success", or a failure string.
        return "Success"

uCommandRegistry.RegisterCommand(${Command}, ${Command}Result)
