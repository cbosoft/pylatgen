#!/usr/bin/env python3

import subprocess as sp
from enum import Enum

class LaTeX_DocType(Enum):
    ARTICLE = "article"
    REPORT = "report"

class LaTeX_Document(object):

    def __init__(self, title = "", doctype = LaTeX_DocType.ARTICLE, bibfile = "", author = "", date = " "):
        self.Title = title
        self.Bibfile = bibfile
        self.Type = doctype.value
        self.Author = author
        self.Date = date
        self.Content = list()

    def __repr__(self):
        rv = "LaTeX " + self.Type.capitalize() + " (" + str(len(self.Content)) + " ish lines)"
        return rv

    def AddChapter(self, chapter_title, numbered = True):

        assert(type(chapter_title) is str)
        assert(type(numbered) is bool)

        ast = "*"
        if numbered: ast = ""
        self.Content.append(r"\chapter" + ast + "{" + chapter_title + "}")

    def AddSection(self, section_title, numbered = True):

        assert(type(section_title) is str)
        assert(type(numbered) is bool)

        ast = "*"
        if numbered: ast = ""
        self.Content.append(r"\section" + ast + "{" + section_title + "}")

    def AddSubSection(self, subsection_title, numbered = True):

        assert(type(section_title) is str)
        assert(type(numbered) is bool)

        ast = "*"
        if numbered: ast = ""
        self.Content.append(r"\subsection" + ast + "{" + subsection_title + "}")

    def AddSubSubSection(self, subsubsection_title, numbered = True):

        assert(type(subsubsection_title) is str)
        assert(type(numbered) is bool)

        ast = "*"
        if numbered: ast = ""
        self.Content.append(r"\subsubsection" + ast + "{" + subsubsection_title + "}")

    def AddParagraph(self, paragraph):

        assert(type(paragraph) is str)

        self.Content.append(paragraph)
        self.Content.append("")
        
    def AddEquation(self, equation, equation_type="equation"):
        pass
    
    def GetTeX(self):
        tex = list()
        tex.append(r"\documentclass{" + self.Type + "}")
        tex.append(r"\usepackage{amsmath}")
        tex.append(r"\usepackage{amsfont}")
        tex.append(r"\usepackage[left = 1in, right = 1in]{geometry}")
        tex.append(r"\usepackage{graphicx}")
        tex.append(r"")
        tex.append(r"\title{" + self.Title + "}")
        tex.append(r"\author{" + self.Author + "}")
        tex.append(r"\date{" + self.Date + "}")
        tex.append(r"")
        tex.append(r"\begin{document}")

        for s in self.Content:
           tex.append(s)

        tex.append(r"\end{document}")

        return tex

    def Output(self, output_path):
        with open(output_path, 'w') as of:
            of.Writelines(self.GetTeX())
        return 1

    def Compile(self, output_path):
        pass
