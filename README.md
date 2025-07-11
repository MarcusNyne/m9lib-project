# m9lib Project Creator

[**m9lib**](https://github.com/MarcusNyne/m9lib) is a python library that provides a framework for executing custom commands from configuration.  The library also includes helpful features around configuration, csv, logging, and directory scanning that provide benefits beyond the command execution framework.

This application may be used to create an empty m9lib project from a template.
- If you are new to **m9lib**, follow the quick-start below.
- Once you have a basic understanding, modify the configuration file to create your own empty project.
- Since the project creator itself is an **m9lib** project, take a look under the hood and use this project as an example of an m9lib project.
 
## Installation

Run "install_windows.bat" to set up your virtual environment.  A "venv" folder will be created inside your project.

## Create EmptyProject

From VSCODE, run "ProjectTemplate".  This will create a new, empty project in your folder structure at the same level as **m9lib-project**, named "EmptyProject".

Navigate to "EmptyProject" and run "install_windows.bat".  This will setup a new virtual environment in the "venv" folder.

Open the project workspace (empty_project.code-workspace) in VSCODE and run "EmptyProject".  Note the colored console output.

### Configuration file (empty_project.ini)

**m9lib** is a configuration-driven framework.  The configuration file contains both application-level and command-level settings.

```python
[EmptyProject]
Logfile = logs\{YMD} EmptyCommand.log
Preview = False
Execute = run

[EmptyCommand:run]
MyParam=Some custom value
```

**`[EmptyProject]`** is the "control-section", containing application-level configuration.
- *EmptyProject* is the section name.  This matches the control name passed to **uControl()**
- *Logfile*: This log was created when you ran the application.  {YMD} is replaced by **uFormat.String()**
- *Preview*: Convenient way to pass a preview flag into the command.  This is for your use and has no impact within the control framework.
- *Execute*: A comma-delimited list of commands to run.  This can contain command names or section ids.  In this example, "run" is a section id.  A setting of "Execute=EmptyCommand" would have the same result, by referencing a command-section by name.

**`[EmptyCommand:run]`** is a "command-section", containing command-level configuration parameters.
- *EmptyCommand* is the section name.  By default, this is also considered the "class name", which allows **uControl** to know what class to instantiate for the command.  Thus, it will match the **uCommand**-derived class registered with **uCommandRegistry.RegisterCommand()**
- *run* is the section id.  This is referenced directly from the control-section *Execute* setting.
- *MyParam* is a command parameter.  Commands use parameters during execution.  A command will have access to the entire configuration file, but configuration specific to a command execution should come from the command-section.

### Control script (empty_project.py)

Contains a custom control class **"class EmptyProject(uControl)"**.  Implement the provided methods for custom behavior.
- **imp_ini_command(self, in_command)**: called to initialize a command before execution
- **imp_prepare(self)**: called before any commands are executed
- **imp_finalize(self)**: called after all commands are executed

A custom control class is not required.  If you do not wish to implement custom functionality, delete the **EmptyProject** class and use **uControl** directly.
- A line to accomplish this was provided, but commented out.  Try uncommenting this line to see the difference.

The logger line was provided to allow more detailed logging, in color.
- Comment this line out to see the difference
- By default, the console only prints warning-and-above messages, and does not print in color

Because a logfile path was a provided, log lines are also written to a log file.  By default, only warnings go to the console, but more detailed informational messages can be found in the log file.

### Command script (c_empty_project.py)

A command script includes:
- A custom command result class (optional)
- A custom command class
- Command class registration

The custom result class is **"class EmptyCommandResult(uCommandResult)"**.
- It is not necessary to implement a custom result class.  If not required, delete the class and remove the class from the registration call.
- To conserve memory, command objects are released immediately after execution.  However, command results will be maintained by **uControl**, so add any properties that you would like to be available post-execution.

The custom command class is "class EmptyCommand(uCommand)".
- Note that calling super class initialization is required.
- Implement your command within **imp_execute()**
- There are a wide variety of methods available for parameter access and logging.  Commands should use command parameters for execution.
- To access configuration outside of the command-section, use **GetConfig()**

Finally, the custom command class must be registered.
- **uControl** will create the command class by using the class-name from configuration, which matches the class name that is registered, which matches the custom command class.
- If you are not using a custom result class, remove it from configuration.  In this case, **uCommandResult** is used for command results.

### Log files (logs folder)

Log files will be created in the "logs" folder.  This is configured in "empty_project.ini".

## Create your custom project

Now that you are familiar with the structure of an empty project, use the m9lib project creator to create empty projects with your own custom names.

All that is required is a few changes to "m9lib-project.ini".

```ini
[ProjectTemplate]
Logfile = logs\{YMD} Template.log
Preview = False
Execute = new_project

[comTemplate:new_project]
SourceFolder = _template
TargetFolder = ..
Replace = new_project_replace

[Replace:new_project_replace]
f_name = empty_project
Project = EmptyProject
Command = EmptyCommand
```

The command-section is `[comTemplate:new_project]`.  Make a copy of this section with a new id.
- *TargetFolder* is the root folder where your new project folder will be created
- Update the *Execute* line of the `[ProjectTemplate]` to reference your new command id

Make a copy of the `[Replace]` section with a new id.
- Change *f_name* to your custom file name prefix
- Change *Project* to the name of your project, including the project folder
- Change *Control* to the name of your custom Control, and the name of the section in the configuration file
- Change *Command* to the name of your custom Command
- Update the *Replace* line of your new command-section to reference this section id

Wasn't that easy?  Now you understand the power and convenience of configuration-driven command execution.

Run "ProjectTemplate" to create your new project.
