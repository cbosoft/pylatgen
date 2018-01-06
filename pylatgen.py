#!/usr/bin/env python3

import subprocess as sp
from enum import Enum

######################################################################################################
####### Enums ########################################################################################

class LaTeX_DocType(Enum):
    ARTICLE = "article"
    REPORT = "report"
    BOOK = "book"

class LaTeX_SecType(Enum):
    CHAPTER = "chapter"
    SECTION = "section"
    SUBSECTION = "subsection"
    SUBSUBSECTION = "subsubsection"
    PARAGRAPH = "par"

######################################################################################################
####### Exceptions ###################################################################################

class GenericDocException(Exception):
    '''Raised when I can't think of a better category to put it in'''
    
class InvalidDocException(Exception):
    '''Raised when user is trying to do something in the wrong document class'''

class UnimplementedMethodException(Exception):
    '''Raised when a prototype unwritten exception is called'''

######################################################################################################
####### Packages and Settings ########################################################################

class LATEX_FIGURE(object):
    Width = None
    Scale = None
    Height = None

    def __repr__(self):
        rv = "["
        setts = [("width", self.Width), ("scale", self.Scale), ("height", self.Height)]
        for opt, sett in setts:
            if (sett != None):
                rv += opt + "=" + str(sett) + ","
        if (rv == "["):
            return ""
        else:
            return rv[:-1] + "]"

class LATEX_GEOMETRY(object):
    Left = 72
    Right = 72
    Top = None
    Bottom = None

    def __repr__(self):
        rv = "["
        setts = [("left", self.Left), ("right", self.Right), ("top", self.Top), ("bottom", self.Bottom)]
        for opt, sett in setts:
            if (sett != None):
                rv += opt + "=" + str(sett) + "pt,"
        if (rv == "["):
            return ""
        else:
            return rv[:-1] + "]"

class LATEX_PROTO_DOC(object):

    ###################################################################################################
    #### Dunder Methods ###############################################################################
    
    def __init__(self, title = "", bibfile = "", bibstyle = "apalike", author = "", date = " ", extra_preamble = list()):
        # General properties of the document
        self.Title = title
        if (bibfile != ""):
            self.Bibfile = bibfile
            self.Bibstyle = bibstyle
        else:
            self.Bibfile = False
            self.Bibstyle = False
        if not self.Type: self.Type = "report" # by default
        self.Author = author
        self.Date = date
        self.Content = list()
        self.ExtraPreamble = extra_preamble

        # Switches
        self.MAKETITLE = False
        self.INDENT_PARS = True
        self.DEBUG = False

        self.HAS_EQUATION = False
        self.HAS_FIGURE = False
        self.HAS_SUBFIGURE = False
        self.HAS_NOMENCLATURE = False
        self.HAS_APPENDIX = False

        # Package Settings
        self.Geometry = LATEX_GEOMETRY()
        self.DefaultFigure = LATEX_FIGURE()
        
    def __repr__(self):
        rv = "LaTeX " + self.Type.capitalize() + " (" + str(len(self.Content)) + " ish lines)"
        return rv

    ###################################################################################################
    #### Settings #####################################################################################
    
    def MakeTitle(self):
        self.MAKETITLE = True

    def Debug(self):
        self.DEBUG = True

    ###################################################################################################
    #### Add Methods ##################################################################################

    def ADD(self, what, to, add_type, numbered):

        ast = "*"
        if numbered: ast = ""
        line = what
        if add_type != LaTeX_SecType.PARAGRAPH:
            line = "\\" + add_type.value + ast + "{" + what + "}"
        elif (not self.INDENT_PARS):
            to.append(r"\noindent")
        to.append(line)

    def ADD_CHAPTER(self, chapter_title, to, numbered):
        self.ADD(chapter_title, to, LaTeX_SecType.CHAPTER, numbered)

    def ADD_SECTION(self, section_title, to, numbered):
        self.ADD(section_title, to, LaTeX_SecType.SECTION, numbered)

    def ADD_SUBSECTION(self, section_title, to, numbered):
        self.ADD(section_title, to, LaTeX_SecType.SUBSECTION, numbered)

    def ADD_SUBSUBSECTION(self, section_title, to, numbered):
        self.ADD(section_title, to, LaTeX_SecType.SUBSUBSECTION, numbered)

    def ADD_PARAGRAPH(self, paragraph, to):
        self.ADD(paragraph, to, LaTeX_SecType.PARAGRAPH, None)

    def ADD_EQUATION(self, equation, to, equation_type, subslist, label, numbered):

        if (not self.HAS_EQUATION): self.HAS_EQUATION = True
    
        assert(type(equation) is str)
        assert(type(equation_type) is str)
        assert(((type(subslist) is list) or (subslist == None)))
        assert(((type(label) is str) or (label == None)))
        assert(type(numbered is bool))
        assert(type(to) is list)

        if (subslist):
            assert(type(subslist) is list)
            vardexlist = [(i + 1) for i, ltr in enumerate(equation) if ltr == "#"]
            idxoff = 0
            for idx in vardexlist:
                i = idx + idxoff
                vardex = int(equation[i])
                val = str(subslist[vardex])
                idxoff += len(val) - 2
                equation = equation.replace("#{}".format(vardex), val)
                #print("EQN: replaced {} with {}".format("#{}".format(vardex), str(subslist[vardex])))
        else:
            assert(not equation.count('#'))
            
        if not numbered and not "*" in equation_type: equation_type += "*"

        line = r"\begin{" + equation_type + "}"
        if (label != None):
            line += r"\label{" + label + "}"
        to.append(line)
        to.append(equation)
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

    def ADD_FIGURE(self, figpath, caption, label, to, figsettings):

        if not self.HAS_FIGURE: self.HAS_FIGURE = True

        assert(type(figpath) is type(caption))
        assert(type(figpath) is type(label))
        assert(((type(figsettings) is LATEX_FIGURE) or (figsettings == None)))
        assert(type(to) is list)

        settings = str(self.DefaultFigure)
        if (figsettings): settings = str(figsettings)

        to.append(r"\begin{figure}")
        to.append(r"\centering")
        if (type(figpath) is list):
            if not self.HAS_SUBFIGURE: self.HAS_SUBFIGURE = True
            for figp, cap, lab in zip(figpath, caption, label):
                to.append(r"\begin{subfigure}")
                to.append(r"\centering")
                to.append(r"\includegraphics" + settings + "{" + figp + "}")
                if caption: to.append(r"\caption{" + cap + "}")
                if label: to.append(r"\label{" + lab + "}")
                to.append(r"\end{subfigure}")
        else:
            to.append(r"\includegraphics" + settings + "{" + figpath + "}")
            if caption: to.append(r"\caption{" + caption + "}")
            if label: to.append(r"\label{" + label + "}")
        to.append(r"\end{figure}")

    def ADD_NOMENCLATURE(self, symbol, description, to, prefix = None):
        line = r"\nomenclature"
        if (prefix != None):
            line += "[" + prefix + "]"
        line += "{" + symbol + "}{" + description + "}"
        print(line)
        to.append(line)
        if (not self.HAS_NOMENCLATURE): self.HAS_NOMENCLATURE = True

    ###################################################################################################
    ### Document Body Methods #########################################################################

    def AddChapter(self, chapter_title, numbered = True):
        self.ADD_CHAPTER(chapter_title, self.Content, numbered)
        
    def AddSection(self, section_title, numbered = True):
        self.ADD_SECTION(section_title, self.Content, numbered)
        
    def AddSubsection(self, subsection_title, numbered = True):
        self.ADD_SUBSECTION(subsection_title, self.Content, numbered)
        
    def AddSubSubSection(self, subsubsection_title, numbered = True):
        self.ADD_SUBSUBSECTION(subsubsection_title, self.Content, numbered )
        
    def AddParagraph(self, paragraph):
        self.ADD_PARAGRAPH(paragraph, self.Content)
                  #(self, equation, to, equation_type, subslist, label, numbered)
    def AddEquation(self, equation, equation_type="equation", subslist = None, label = None, numbered = True):
        self.ADD_EQUATION(equation, self.Content, equation_type, subslist, label, numbered)
        
    def AddTable(self, *args, horiz_lines = False, vert_lines = False, both_lines = False, bold_header = False, centered = True):
        self.ADD_TABLE(*args, self.Content, horiz_lines, vert_lines, both_lines, bold_header, centered)

    def AddFigure(self, figpath, caption = None, label = None, figsettings = None):
        self.ADD_FIGURE(self, figpath, caption, label, self.Content, figsettings)
        
    def AddNomenclature(self, symbol, description, prefix = None):
        self.ADD_NOMENCLATURE(symbol, description, self.Content, prefix)
    
    ###################################################################################################
    ### Appendix Methods ##############################################################################

    def APPENDIX_INIT(self):
        if (not self.HAS_APPENDIX):
            self.HAS_APPENDIX = True
            self.AppendixContent = list()

    def AppendixAddChapter(self, chapter_title, numbered = True):
        self.APPENDIX_INIT()
        self.ADD_CHAPTER(chapter_title, self.AppendixContent, numbered)
        
    def AppendixAddSection(self, section_title, numbered = True):
        self.APPENDIX_INIT()
        self.ADD_SECTION(section_title, self.AppendixContent, numbered)
        
    def AppendixAddSubsection(self, subsection_title, numbered = True):
        self.APPENDIX_INIT()
        self.ADD_SUBSECTION(subsection_title, self.AppendixContent, numbered)
        
    def AppendixAddSubSubSection(self, subsubsection_title, numbered = True):
        self.APPENDIX_INIT()
        self.ADD_SUBSUBSECTION(subsubsection_title, self.AppendixContent, numbered)
        
    def AppendixAddParagraph(self, paragraph):
        self.APPENDIX_INIT()
        self.ADD_PARAGRAPH(paragraph, self.AppendixContent)
        
    def AppendixAddEquation(self, equation, equation_type="equation", label = None, numbered = True):
        self.APPENDIX_INIT()
        self.ADD_EQUATION(equation, self.AppendixContent, equation_type, label, numbered)
        
    def AppendixAddTable(self, *args, horiz_lines = False, vert_lines = False, both_lines = False, bold_header = False, centered = True):
        self.APPENDIX_INIT()
        self.ADD_TABLE(*args, self.AppendixContent, horiz_lines, vert_lines, both_lines, bold_header, centered)
        
    def AppendixAddFigure(self, figpath, caption = None, label = None, figsettings = None):
        self.ADD_FIGURE(self, figpath, caption, label, self.AppendixContent, figsettings)
        
    def AppendixAddNomenclature(self, symbol, description, prefix = None):
        self.APPENDIX_INIT()
        self.ADD_NOMENCLATURE(symbol, description, self.AppendixContent, prefix)
        
    ###################################################################################################
    #### Build + Compile Methods ######################################################################
    
    def GetTeX(self):
        tex = list()
        print(self.Type)
        tex.append(r"\documentclass{" + self.Type + "}")
        if not self.DEBUG: tex.append(r"\batchmode") # reduces compiler output
        if self.HAS_EQUATION:
            tex.append(r"\usepackage{amsmath}")
            tex.append(r"\usepackage{amssymb}")
            tex.append(r"\usepackage{amsfonts}")
        tex.append(r"\usepackage[english]{babel}")
        tex.append(r"\usepackage" + str(self.Geometry) + "{geometry}")
        if self.HAS_FIGURE: tex.append(r"\usepackage{graphicx}")
        if self.HAS_SUBFIGURE:
            tex.append(r"\usepackage{caption}")
            tex.append(r"\usepackage{subcaption}")
        if self.HAS_NOMENCLATURE:
            tex.append(r"\usepackage{nomencl}")
            tex.append(r"\makenomenclature")
        tex.append(r"")
        tex.append(r"\title{" + self.Title + "}")
        tex.append(r"\author{" + self.Author + "}")
        tex.append(r"\date{" + self.Date + "}")
        tex.append(r"")

        for s in self.ExtraPreamble:
            tex.append(s)
        
        tex.append(r"\begin{document}")

        if (self.MAKETITLE): tex.append(r"\maketitle")

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

        if (self.HAS_EQUATION): rebuild = True
            
        if (rebuild):
            print("\n\n********************************************************")
            print("**** Penultimate Build *********************************\n")
            sp.call("pdflatex " + self.OutputName + ".tex", shell = True)
        
            print("\n\n********************************************************")
            print("**** Final build ***************************************\n")
            sp.call("pdflatex " + self.OutputName + ".tex", shell = True)

        if not self.DEBUG: 
            print("\n\nTidying up....")
            sp.call("rm -rf *.aux *.log *.bbl *.blg *~ *.ilg *.nls *.nlo *.tex", shell = True)
    
class LaTeX_Article(LATEX_PROTO_DOC):

    Type = "article"

    def AddChapter(self,  *args, **kwargs):
        raise InvalidDocException("You cannot add a chapter to an article.")

    def AppendixAddChapter(self, *args, **kwargs):
        raise InvalidDocException("You cannot add a chapter to an article.")

class LaTeX_Report(LATEX_PROTO_DOC):

    Type = "report"

class LaTeX_Book(LATEX_PROTO_DOC):
        
    Type = "book"
