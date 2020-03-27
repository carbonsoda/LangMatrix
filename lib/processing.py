import os
import re
import csv
import string
from collections import defaultdict
from datetime import datetime
from lib.fileoperations import FileOperations
import pandas as pd
from string import ascii_lowercase

# CONSTANTS
SAVE_DIR = '/_word_data/'
COUNT_SUFFIX = '_word_frequency'
UNIQUE_SUFFIX = '_words_unique'


class Processing(FileOperations):
    def __init__(self):
        super().__init__()
        self.unwanted_char = [r'\[\b', r'\(\b', r'\b\]', r'\b\)', r'\b\.']
        self.delimiter = {'.txt': '\t', '.csv': ','}
        # self.defaults = self.loaddefaults()

        # The two list of files to analyze
        self.A_analyzepath = ""
        self.B_analyzepath = ""
        self.A_files = []
        self.B_files = []
        self.A_col = ""
        self.B_col = ""

        # for saving individual sets of results
        # not implemented yet, rn they are with output dir
        self.A_savedir = ""
        self.B_savedir = ""

        today = str(datetime.today().date())
        self.outputdir = self.generate_dir(os.getcwd() + "/results/", today)

    # Sets up remaining paths and lists
    # Returns false if both parse lists are empty
    def config(self):
        # root directories for all transcript files
        if self.A_analyzepath:
            root_A = os.path.split(self.A_analyzepath)[0]
            self.A_files = self.parsefilelists(root_A, self.A_analyzepath)
        if self.B_analyzepath:
            root_B = os.path.split(self.B_analyzepath)[0]
            self.B_files = self.parsefilelists(root_B, self.B_analyzepath)

        if self.A_files and self.B_files:
            return True, False
        if self.A_files or self.B_files:
            return False, True
        return False, False

    def analysis(self, isdouble=False, issingle=False):
        if isdouble:
            Aname = os.path.splitext(os.path.split(self.A_analyzepath)[1])[0]
            Bname = os.path.splitext(os.path.split(self.B_analyzepath)[1])[0]

            # analyze each, returns dataframe
            A_wordcounts = self.process(self.A_analyzepath, self.A_files, self.A_col, Aname)
            B_wordcounts = self.process(self.B_analyzepath, self.B_files, self.B_col, Bname)

            # merging both together
            master_wordcounts = self.join_dfs([A_wordcounts, B_wordcounts])
            return self.dfsavefile(master_wordcounts, self.outputdir, Aname + '-' + Bname + '_master_matrix')
        elif issingle:
            analyzepath = ""
            colanalyze = ""
            analyzelist = []

            if self.A_files:
                analyzepath = self.A_analyzepath
                colanalyze = self.A_col
                analyzelist = self.A_files
            else:
                analyzepath = self.B_analyzepath
                colanalyze = self.B_col
                analyzelist = self.B_files

            wordcounts = self.process(analyzepath, analyzelist, colanalyze)
            if wordcounts is not None:
                return True
            return False

    def process(self, filepath, fileslist, col=None, listname=None):
        # set() and pd.DataFrame for word frequencies
        words, wordcounts = self.getwordcount(fileslist, col)

        # save this singular list's results to a file
        if not listname:
            listname = os.path.splitext(os.path.split(filepath)[1])[0]
        self.dfsavefile(wordcounts, self.outputdir, listname + '_matrix')

        if self.fileexists_check(self.outputdir, listname + '_matrix.csv'):
            return wordcounts
        return None

    # Loops through each file in a given list
    # Returns words as set, and dataframe of the word counts
    def getwordcount(self, fileslist, column):
        all_words = set()
        all_dfs = []  # list of all the dfs

        for transcript in fileslist:
            wordcount = self.wordcounting(transcript, column)  # type: pd.Series
            all_words.update(wordcount.keys())
            all_dfs.append(wordcount.to_frame(wordcount.name))

        total_df = self.join_dfs(all_dfs)

        return all_words, total_df

    # handles opening each transcript/words file and processes the unique wordcounts
    # returns wordcount as pd.Series
    def wordcounting(self, processfile, colanalyze=None):
        seriesname, ext = os.path.splitext(os.path.split(processfile)[1])
        delim = self.delimiter[ext]
        if colanalyze:
            # maps given column (A, B, C...) onto position in alphabet
            col = string.ascii_lowercase.index(colanalyze.lower())
            return self.column_analyze(processfile, col, delim, seriesname)
        else:
            # no column specified, but I think might remove this and throw error instead?
            return self.nocolumn_analyze(processfile, delim, seriesname)

    # Given specific column index to analyze, search word frequency
    # returns pd.Series
    def column_analyze(self, processfile, colanalyze, delimiter, seriesname):
        wordcolumn = pd.read_csv(processfile, header=None, squeeze=True,
                                 usecols=[colanalyze], delimiter=delimiter)  # type: pd.Series
        wordcount = pd.Series(' '.join(wordcolumn).split(), name=seriesname).value_counts()

        return wordcount

    # The user has not specified a column to analyze
    # returns pd.Series
    def nocolumn_analyze(self, processfile, delimiter, seriesname):
        wordcount = defaultdict(lambda: 0)
        encode = 'utf-8-sig'

        # Assumes user wants first non-numerical column, aka one with text
        while True:
            try:
                with open(processfile, "r", encoding=encode) as f:
                    reader = csv.reader(f, delimiter=delimiter)

                    for row in reader:
                        if not row:
                            continue
                        words = []
                        # find first cell in row w/o numbers
                        for i in range(len(row)):
                            if not row[i].isdigit():
                                words = row[i].split(" ")
                                break
                        for i in range(len(words)):
                            if ',' in words[i]:
                                w1, w2 = words[i].split(',')
                                words[i] = w1
                                words.append(w2)
                        # now filter
                        for word in words:
                            clean_word = self.fix_punctuation(word)
                            wordcount[clean_word] += 1
                break
            except UnicodeDecodeError:
                # 'utf-8-sig' prevents weird symbols showing up (ie euro symbol)
                # but sometimes it causes unicodedecodeerror and requires 'utf-8'
                # this is a catch-all route
                encode = 'cp1252'

        remove = [' ', '']
        for ch in remove:
            if ch in wordcount:
                del wordcount[ch]

        return pd.Series(wordcount, name=seriesname)

    # Helper for nocolumn_analyze
    def fix_punctuation(self, word):
        newword = word.lower()
        for unwanted in self.unwanted_char:
            newword = re.sub(unwanted, '', newword)

        if newword.startswith('-'):
            newword = newword[1:]
        if newword.endswith('-'):
            newword = newword[:-1]

        return newword

    # joins list of dataframes, where col[0] is all the unique words
    def join_dfs(self, dfs_list):
        # processing dataframes
        df_master = dfs_list[0].join(dfs_list[1:], how='outer', sort=False)
        df_master.fillna(0, inplace=True)
        df_master['labels'] = df_master.index.str.lower()
        df_master = df_master.sort_values('labels').drop('labels', axis=1)

        return df_master

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
        defaults_file = 'resources/namedefaults.csv'
        defaultnames = {}
        with open(defaults_file, "r") as f:
            reader = csv.reader(f)
            next(reader)  # skip header
            for row in reader:
                try:
                    # Name RootDir StartsWith EndsWith AnalysisCol
                    defaultnames[row[1]] = {'startswith': row[2], 'endswith': row[3], 'anylcol': row[4]}
                except IndexError:
                    pass

        return defaultnames



