#!/usr/bin/env python3

import subprocess as sp
from enum import Enum

class LaTeX_DocType(Enum):
    ARTICLE = "article"
    REPORT = "report"
    BOOK = "book"

class LaTeX_Document(object):

    def __init__(self, title = "", doctype = LaTeX_DocType.ARTICLE, bibfile = "", bibstyle = "apalike", author = "", date = " ", extra_preamble = list()):
        # General properties of the document
        self.Title = title
        if (bibfile != ""):
            self.Bibfile = bibfile
            self.Bibstyle = bibstyle
        else:
            self.Bibfile = False
            self.Bibstyle = False
        self.Type = doctype.value
        self.Author = author
        self.Date = date
        self.Content = list()
        self.ExtraPreamble = extra_preamble

        # Document switches
        self.maketitle = False
        self.indentparagraphs = True
        self.doublespaceparagraphs = False

        # Meta switches
        self.DEBUG = False
        self.HAS_NOMENCLATURE = False
        self.HAS_APPENDIX = False
        

    def __repr__(self):
        rv = "LaTeX " + self.Type.capitalize() + " (" + str(len(self.Content)) + " ish lines)"
        return rv

    ###################################################################################################
    #### Settings #####################################################################################
    def MakeTitle(self):
        self.maketitle = True

    def Debug(self):
        self.debug = True

    ###################################################################################################
    ### General methods ###############################################################################
    def ADD_CHAPTER(self, chapter_title, to, numbered = True):

        assert(type(chapter_title) is str)
        assert(type(numbered) is bool)
        assert(type(to) is list)

        ast = "*"
        if numbered: ast = ""
        to.append(r"\chapter" + ast + "{" + chapter_title + "}")

    def ADD_SECTION(self, section_title, to, numbered = True):

        assert(type(section_title) is str)
        assert(type(numbered) is bool)
        assert(type(to) is list)

        ast = "*"
        if numbered: ast = ""
        to.append(r"\section" + ast + "{" + section_title + "}")

    def ADD_SUBSECTION(self, subsection_title, to, numbered = True):

        assert(type(subsection_title) is str)
        assert(type(numbered) is bool)
        assert(type(to) is list)

        ast = "*"
        if numbered: ast = ""
        to.append(r"\subsection" + ast + "{" + subsection_title + "}")

    def ADD_SUBSUBSECTION(self, subsubsection_title, to, numbered = True):

        assert(type(subsubsection_title) is str)
        assert(type(numbered) is bool)
        assert(type(to) is list)

        ast = "*"
        if numbered: ast = ""
        to.append(r"\subsubsection" + ast + "{" + subsubsection_title + "}")

    def ADD_PARAGRAPH(self, paragraph, to):

        assert(type(paragraph) is str)

        if (self.doublespaceparagraphs):
            to.append(r"\newline\newline")
        if (not self.indentparagraphs):
            to.append(r"\noindent")
        to.append(paragraph)
        to.append("")
        
    def ADD_EQUATION(self, equation, to, equation_type="equation", label = None, numbered = True):

        if (type(equation) is str):
            equation = [equation]
        elif (type(equation) is list):
            assert(type(equation[0]) is str)
        else:
            assert(type(equation) is str)  # will fail
        assert(type(equation_type) is str)
        assert(((type(label) is str) or (label == None)))
        assert(type(numbered is bool))
        assert(type(to) is list)

        if not numbered and not "*" in equation_type: equation_type += "*"

        line = r"\begin{" + equation_type + "}"
        if (label != None):
            line += r"\label{" + label + "}"
        to.append(line)
        for s in equation:
            to.append(s)
        to.append(r"\end{" + equation_type + "}")

    def ADD_TABLE(self, *args, to = None, horiz_lines = False, vert_lines = False, both_lines = False, bold_header = False, centered = True):

        assert(type(to) is not None)
        
        if (both_lines):
            vert_lines = True
            horiz_lines = True
        lrows = len(args)
        lcols = len(args[0])

        #if (bold_header):
        #    for i in range(len(args[0])):
        #        args[0][i] = r"\textbf{" + args[0][i] + "}"
        
        for a in args:
            assert(type(a) is list)
            assert(len(a) == lcols)

        if (centered): to.append(r"\begin{center}")
            
        line = r"\begin{tabular}{"
        if (horiz_lines): line += "|"
        for i in range(lcols):
            line += "c "
            if (horiz_lines): line += "|"
        line += "}"
        
        to.append(line)
        if (vert_lines): to.append(r"\hline")
        for a in args:
            line = ""
            for c in a:
                line += str(c) + "&"
            line = line[:-1] + r"\\"
            if (bold_header and args[0] == a): line += r"\hline"
            to.append(line)
            if (vert_lines): to.append(r"\hline")
        to.append(r"\end{tabular}")
        if (centered): to.append(r"\end{center}")

    def ADD_NOMENCLATURE(self, symbol, description, to, prefix = None):
        line = r"\nomenclature"
        if (prefix != None):
            line += "[" + prefix + "]"
        line += "{" + symbol + "}{" + description + "}"
        to.append(line)
        if (not self.HAS_NOMENCLATURE): self.HAS_NOMENCLATURE = True

    ###################################################################################################
    ### Document Body Methods #########################################################################

    def AddChapter(self, chapter_title, numbered = True):
        self.ADD_CHAPTER(chapter_title, self.Content, numbered = numbered)
        
    def AddSection(self, section_title, numbered = True):
        self.ADD_SECTION(section_title, self.Content, numbered = True)
        
    def AddSubsection(self, subsection_title, numbered = True):
        self.ADD_SUBSECTION(subsection_title, self.Content, numbered = True)
        
    def AddSubSubSection(self, subsubsection_title, numbered = True):
        self.ADD_SUBSUBSECTION(subsubsection_title, self.Content, numbered = True)
        
    def AddParagraph(self, paragraph):
        self.ADD_PARAGRAPH(paragraph, self.Content)
        
    def AddEquation(self, equation, equation_type="equation", label = None, numbered = True):
        self.ADD_EQUATION(equation, self.Content, equation_type="equation", label = None, numbered = True)
        
    def AddTable(self, *args, horiz_lines = False, vert_lines = False, both_lines = False, bold_header = False, centered = True):
        self.ADD_TABLE(*args, to = self.Content, horiz_lines = False, vert_lines = False, both_lines = False, bold_header = False, centered = True)
        
    def AddNomenclature(self, symbol, description, prefix = None):
        self.ADD_NOMENCLATURE(symbol, description, self.Content, prefix = None)
    
    ###################################################################################################
    ### Appendix Methods ##############################################################################

    def APPENDIX_INIT(self):
        if (not self.HAS_APPENDIX):
            self.HAS_APPENDIX = True
            self.AppendixContent = list()

    def AppendixAddChapter(self, chapter_title, numbered = True):
        self.APPENDIX_INIT()
        self.ADD_CHAPTER(chapter_title, self.AppendixContent, numbered = numbered)
        
    def AppendixAddSection(self, section_title, numbered = True):
        self.APPENDIX_INIT()
        self.ADD_SECTION(section_title, self.AppendixContent, numbered = True)
        
    def AppendixAddSubsection(self, subsection_title, numbered = True):
        self.APPENDIX_INIT()
        self.ADD_SUBSECTION(subsection_title, self.AppendixContent, numbered = True)
        
    def AppendixAddSubSubSection(self, subsubsection_title, numbered = True):
        self.APPENDIX_INIT()
        self.ADD_SUBSUBSECTION(subsubsection_title, self.AppendixContent, numbered = True)
        
    def AppendixAddParagraph(self, paragraph):
        self.APPENDIX_INIT()
        self.ADD_PARAGRAPH(paragraph, self.AppendixContent)
        
    def AppendixAddEquation(self, equation, equation_type="equation", label = None, numbered = True):
        self.APPENDIX_INIT()
        self.ADD_EQUATION(equation, self.AppendixContent, equation_type="equation", label = None, numbered = True)
        
    def AppendixAddTable(self, *args, horiz_lines = False, vert_lines = False, both_lines = False, bold_header = False, centered = True):
        self.APPENDIX_INIT()
        self.ADD_TABLE(*args, to = self.AppendixContent, horiz_lines = False, vert_lines = False, both_lines = False, bold_header = False, centered = True)
        
    def AppendixAddNomenclature(self, symbol, description, prefix = None):
        self.APPENDIX_INIT()
        self.ADD_NOMENCLATURE(symbol, description, self.AppendixContent, prefix = None)

    ###################################################################################################
    ### Outpute + Build Methods #######################################################################
    def GetTeX(self):
        tex = list()
        tex.append(r"\documentclass{" + self.Type + "}")
        if not self.DEBUG: tex.append(r"\batchmode") # reduces compiler output
        tex.append(r"\usepackage{amsmath}")
        tex.append(r"\usepackage{amssymb}")
        tex.append(r"\usepackage{amsfonts}")
        tex.append(r"\usepackage[english]{babel}")
        tex.append(r"\usepackage[left = 1in, right = 1in]{geometry}")
        tex.append(r"\usepackage{graphicx}")
        tex.append(r"")
        tex.append(r"\title{" + self.Title + "}")
        tex.append(r"\author{" + self.Author + "}")
        tex.append(r"\date{" + self.Date + "}")
        tex.append(r"")

        for s in self.ExtraPreamble:
            tex.append(s)
        
        tex.append(r"\begin{document}")

        if (self.maketitle): tex.append(r"\maketitle")

        for s in self.Content:
           tex.append(s)

        if (self.HAS_NOMENCLATURE): tex.append(r"\printnomenclature")
            
        if (self.Bibfile):
            tex.append(r"\bibliography{" + self.Bibfile + "}")
            tex.append(r"\bibliographystyle{" + self.Bibstyle + "}")

        if (self.HAS_APPENDIX):
            tex.append(r"\appendix")
            for s in self.AppendixContent:
                tex.append(s)
            
        tex.append(r"\end{document}")

        return tex

    def Output(self, output_name):
        if output_name[-4:] == ".tex":
            output_name = output_name[:-4]
        self.OutputName = output_name
        lines = self.GetTeX()
        with open(output_name + ".tex", 'w') as of:
            of.write('\n'.join(lines))
        return 1

    def Compile(self):
        print("\n********************************************************")
        print("**** PyLaTeX Compile ***********************************\n")
        
        print("\n\n********************************************************")
        print("**** Build *********************************************\n")
        sp.call("pdflatex " + self.OutputName + ".tex", shell = True)

        rebuild = False
        
        if (self.Bibfile):
            print("\n\n********************************************************")
            print("**** Bibliography **************************************\n")
            sp.call("bibtex " + self.OutputName, shell = True)
            rebuild = True
            
        if (self.HAS_NOMENCLATURE):
            print("\n\n********************************************************")
            print("**** Nomenclature **************************************\n")
            sp.call("makeindex " + self.OutputName + ".nlo -s " + "nomencl.ist -o " + self.OutputName + ".nls", shell = True)
            rebuild = True
            
        if (rebuild):
            print("\n\n********************************************************")
            print("**** Penultimate Build *********************************\n")
            sp.call("pdflatex " + self.OutputName + ".tex", shell = True)
        
            print("\n\n********************************************************")
            print("**** Final build ***************************************\n")
            sp.call("pdflatex " + self.OutputName + ".tex", shell = True)

        print("\n\nTidying up....")
        sp.call("rm -rf *.aux *.log *.bbl *.blg *~ *.ilg *.nls *.nlo *.tex", shell = True)

def TeX_Replace(string, *args):

    assert(string.count("##") == len(args))

    for a in args:
        if (type(a) is float):
            a = "{:.3f}".format(a)
        string = string.replace("##", str(a), 1)

    return string
