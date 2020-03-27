import csv
import os
import pandas as pd

# CONSTANTS
UNIQUE_SUFFIX = '_words_unique'
DEFAULTSFILE = 'resources/namedefaults.csv'


# Handles i/o operations
class FileOperations:
    def __init__(self):
        self.savedir_name = '/_word_data/'
        self.delimiter = {'.txt': '\t', '.csv': ','}
        # self.defaultnames = self.loaddefaults()

    # generates savefolder path, and checks if folder already exists
    def generate_dir(self, root, cust_dir):
        savedir = os.path.join(root, cust_dir)

        if not os.path.exists(savedir):
            os.makedirs(savedir)
        return savedir

    # prevent overwriting, returns filepath
    def checkexisting(self, root, filename, ext='.csv'):
        base = os.path.join(root, filename).replace('\\', '/')
        file = base + ext
        i = 1
        while True:
            if os.path.exists(file):
                file = base + '_' + str(i) + ext
                i += 1
            else:
                return file

    # Searches for desired files in all directorys
    def filefinder(self, root, naming, isprefix=False, ext='.csv'):
        foundfiles = []
        fileslist = []

        for path, _, files in os.walk(root):
            for file in files:
                if file.endswith(ext):
                    if isprefix:
                        if file.startswith(naming):
                            foundfiles.append(os.path.join(path, file).replace('\\', '/'))
                            fileslist.append(os.path.splitext(file)[0])
                    else:
                        if file.endswith(naming + ext):
                            foundfiles.append(os.path.join(path, file).replace('\\', '/'))
                            fileslist.append(os.path.splitext(file)[0])

        # Document which files were found
        mastertxt = os.path.join(root, "list_foundfiles.txt").replace('\\', '/')
        with open(mastertxt, 'w+') as f:
            for file in fileslist:
                f.write(str(file + '\n'))

        return foundfiles

    # Reads each file, containing list of files to analyze
    def parsefilelists(self, root, filepath, defaultoptions=None):
        ext = os.path.splitext(filepath)[1]
        delim = self.delimiter[ext]

        filenames = []
        listpaths = []

        # possible exceptions: IndexError, ValueError(?), Encoding
        with open(filepath, "r") as f:
            reader = csv.reader(f, delimiter=delim)

            for row in reader:
                if len(row) > 0:
                    filenames.append(row[0])

        for name in filenames:
            ext = name[-3:]  # can only be ".txt." or ".csv"
            foundfile = False
            for paths, _, files in os.walk(root):
                if foundfile:
                    foundfile = False
                    break
                for file in files:
                    if file.endswith(ext):
                        if file == name:
                            fullpath = os.path.join(paths, file).replace('\\', '/')
                            listpaths.append(fullpath)
                            foundfile = True
                            break
            continue

        return listpaths

    # Assumes the base file does exist
    def highestfile(self, root, filename, ext='.csv'):
        i = 1
        highestname = filename + ext

        files = [x for x in os.listdir(root) if x.startswith(filename)]

        if len(files) > 1:
            for file in files:
                name = os.path.splitext(file)[0].split('_')
                try:
                    if int(name[3]) > i:
                        i = int(name[3])
                        highestname = file
                except (ValueError, IndexError) as e:
                    continue
        return root + highestname
    
    # Saves given dataframe to a csv, returns true if successful
    def dfsavefile(self, df: pd.DataFrame, root, filename):

        if not os.path.exists(root.replace('\\', '/')):
            os.makedirs(root)

        filepath = self.checkexisting(root, filename)
        encoding = 'utf-8-sig'
        df.to_csv(filepath)

        if self.fileexists_check(filepath):
            return True
        return False

    def fileexists_check(self, root, filename=""):
        if os.path.exists(os.path.join(root, filename).replace("\\", "/")):
            return True
        return False
    
    # word_set = set(all unique words ever in directory)
    # saves it as csv for correction purposes, in case of typos
    def recordwordset(self, words_set, save_root, saveprefix):
        filename = saveprefix + UNIQUE_SUFFIX
        wordsfile = self.checkexisting(save_root, filename)
        wordslist = list(words_set)

        with open(wordsfile, "w+", newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)

            for w in wordslist:
                writer.writerow([w])
    
    def loaddefaults(self):
        defaultnames = {}
        with open(DEFAULTSFILE, "r") as f:
            reader = csv.reader(f)
            next(reader)  # skip header
            for row in reader:
                try:
                    # rootdir: {startswith, endswith, analysiscolumn}
                    defaultnames[row[1]] = {'prefix': row[2], 'suffix': row[3], 'analysiscol': row[4]}
                except IndexError:
                    pass

        return defaultnames
