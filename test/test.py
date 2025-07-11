import unittest
import os,shutil

from m9lib import uControl,uConfig, uConfigSection

from m9lib import uLoggerLevel

from com_project import *

class Test_Template(unittest.TestCase):

    def setUp(self):
        pass

    def initialize(self, in_inifile, in_tempfolder, in_srcfolder):
        if in_inifile is not None:
            config = uConfig(in_inifile)
            logfile = config.GetSectionValue("ProjectTemplate", "Logfile")
            if os.path.exists(logfile):
                os.remove(logfile)

        if in_tempfolder is not None:
            self.tempfolder = r'test\{n}'.format(n=in_tempfolder)
            if in_tempfolder is not None:
                if os.path.isdir(self.tempfolder):
                    shutil.rmtree(self.tempfolder)

            # if in_source is not None:
            #     sourcefolder = r'test\{n}'.format(n=in_source)
            #     if os.path.isdir(sourcefolder):
            #         shutil.copytree(sourcefolder, tempfolder)

    def test_replace(self):
        self.initialize(r"test/test.ini", "target", "source")

        control = uControl("ProjectTemplate", r"test/test.ini", None)
        control.GetLogger().SetPrint(Print=True, Level=uLoggerLevel.DETAILS, Color=True)
        control.Execute ()

        # temp results
        self.assertTrue(True)

        self.source_folder = control.GetResults()[0].source_folder
        self.target_folder = control.GetResults()[0].target_folder
        self.assertEqual(self.validate_file(r"names.txt", r"names.txt", True), True)
        self.assertEqual(self.validate_file(r"sub ${Project}\${f_name}_under.py", r"sub TestProject\test_name_under.py", True), True)
        self.assertEqual(self.validate_file(r"sub ${Project}\${f-name}-dash.py", r"sub TestProject\test-name-dash.py", True), True)
        self.assertEqual(self.validate_file(r"sub ${Project}\sub ${Command}\info.txt", r"sub TestProject\sub TestCommand\info.txt", True), True)
        self.assertEqual(self.validate_file(r"sub ${Project}\sub ${Command}\no-changes.txt", r"sub TestProject\sub TestCommand\no-changes.txt", False), True)

    def validate_file(self, in_sourcefile, in_targetfile, in_changed):
        source_file = os.path.join(self.source_folder, in_sourcefile)
        if os.path.isfile(source_file) is False:
            return f"File does not exist: {source_file}"

        target_file = os.path.join(self.target_folder, in_targetfile)
        if os.path.isfile(target_file) is False:
            return f"File does not exist: {target_file}"
        
        if in_changed:
            if os.path.getsize(source_file) == os.path.getsize(target_file):
                return f"File size should have changed: {source_file} <> {target_file}"
        else:
            if os.path.getsize(source_file) == os.path.getsize(target_file):
                return True
            
            return f"File sizes don't match: {source_file} <> {target_file}"
        
        source_lines = self.count_lines(source_file)
        if source_lines is False:
            return f"Unable to count lines: {source_file}"
        target_lines = self.count_lines(target_file)
        if target_lines is False:
            return f"Unable to count lines: {target_file}"
        
        if source_lines!= target_lines:
            return f"Source and target lines do not match: {source_file} <> {target_file}"

        return True
    
    def count_lines(self, in_filepath):
        try:
            with open(in_filepath, "r") as file:
                lines = 0
                for line in file:
                    lines += 1
                return lines
        except:
            pass

        return False

unittest.main(verbosity=1)