# Copyright (c) 2025 M. Fairbanks
#
# This source code is licensed under the Apache License, Version 2.0, found in the
# LICENSE file in the root directory of this source tree.

import os
import shutil

from m9lib import uCommand, uCommandRegistry

class comTemplate(uCommand):
    
    def __init__(self):
        super().__init__()
        
    def imp_execute(self, in_preview):
        if self.read_params() is False:
            return self.return_failure("* Initialization failure")

        if self.duplicate_source() is False:
            return self.return_failure("* Unable to duplicate source folder")

        if self.rename_folders() is False:
            return self.return_failure("* Failed renaming folders")

        if self.rename_files() is False:
            return self.return_failure("* Failed renaming files")

        if self.process_files() is False:
            return self.return_failure("* Failed processing files")

        return "Success"

    def return_failure(self, in_string):
        self.LogError(in_string)
        return in_string
    
    def read_params (self):

        replace_id = self.GetParam("Replace")
        replace_section = self.GetConfig().GetSection(Name="Replace", Id=replace_id)
        if replace_id is None or replace_section is None:
            self.LogError(f"Replace section not found: [Replace:{replace_id}]")
            return False
        
        self.source_folder = self.GetParam("SourceFolder")
        self.target_folder = self.GetParam("TargetFolder")
        add_folder = replace_section.GetValue("Project")
        if add_folder is not None:
            self.target_folder = os.path.join(self.target_folder, add_folder)

        self.LogParamString("Source folder: [=SourceFolder]")
        self.LogParamString(f"Target folder: {self.target_folder}")

        self.LogParamString("Replace:")
        self.replace = {}
        replace_cfgdict = replace_section.GetDictionary()
        for replace_key in list(replace_cfgdict.keys()):
            if replace_key.startswith('*') is False:
                self.replace["${"+replace_key+"}"] = replace_cfgdict[replace_key]
                self.LogParamString("{k} => {r}".format(k=replace_key, r=replace_cfgdict[replace_key]))

        self.GetLogger().WriteBlank()

        if os.path.exists(self.source_folder) == False:
            self.LogError("Source path doesn't exist: " + self.source_folder)
            return False

        if os.path.exists(self.target_folder) == True:
            self.LogError("Will not overwrite target path: " + self.target_folder)
            return False
        
        self.GetResult().source_folder = self.source_folder
        self.GetResult().target_folder = self.target_folder

        return True

    def duplicate_source(self):
        try:
            if os.path.isdir(self.source_folder):
                shutil.copytree(self.source_folder, self.target_folder)

            return True
        except:
            pass

        return False

    def replace_str(self, in_string):
        for key in self.replace:
            in_string = in_string.replace(key, self.replace[key])
        return in_string

    def rename_folders(self):
        folders = []
        try:
            for root, dirs, _ in os.walk(self.target_folder):
                for d in dirs:
                    r_dir = self.replace_str(d)
                    if d != r_dir:
                        folderpath = os.path.join(root, d)
                        newpath = os.path.join(root, r_dir)
                        folders.insert (0, [folderpath, newpath])

            for f in folders:
                os.rename(f[0], f[1])

            if len(folders)>0:
                self.LogMessage("Renamed {} folders".format(len(folders)))
                for f in folders:
                    self.LogDetails(f"{f[0]} => {f[1]}")

        except:
            return False

        return True

    def rename_files(self):
        try:
            renamed_files = []
            for root, _, files in os.walk(self.target_folder):
                for file in files:
                    r_file = self.replace_str(file)
                    if file != r_file:
                        filepath = os.path.join(root, file)
                        newpath = os.path.join(root, r_file)
                        os.rename(filepath, newpath)
                        renamed_files.append((filepath, newpath))

            self.LogMessage("Renamed {} files".format(len(renamed_files)))
            for file in renamed_files:
                self.LogDetails(f"{file[0]} => {file[1]}")
        except:
            return False

        return True

    def process_files(self):
        try:
            temp_name = "$.$"
            for root, _, files in os.walk(self.target_folder):
                for file in files:
                    filepath = os.path.join(root, file)
                    temppath = os.path.join(root, temp_name)
                    os.rename(filepath, temppath)

                    line_count = 0
                    fr = open(temppath, "r")
                    fw = open(filepath, "w")

                    try:
                        for line in fr:
                            newline = self.replace_str(line)
                            if newline != line:
                                line_count += 1
                            fw.write(newline)

                        if line_count>0:
                            s=""
                            if line_count>1:
                                s="s"
                            self.LogMessage("Replaced {l} line{s} in {f}".format(l=line_count, s=s, f=file))

                        fw.close()
                        fr.close()

                        os.remove(temppath)

                    except Exception as e:
                        # failure may be an attempt to read a binary file
                        fw.close()
                        fr.close()

                        # restore the file
                        try:
                            os.remove(filepath)
                            os.rename(temppath, filepath)
                        except:
                            return False
                        
                        if isinstance(e, UnicodeDecodeError) is False:
                            return False

        except:
            return False

        return True

uCommandRegistry.RegisterCommand(comTemplate)
