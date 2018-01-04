#!/usr/bin/env python3

import subprocess as sp
from enum import Enum

class LaTeX_DocType(Enum):
    ARTICLE = "article"
    REPORT = "report"

class LaTeX_Document(object):

    def __init__(self, title = "", doctype = LaTeX_DocType.ARTICLE, bibfile = "", bibstyle = "apalike", author = "", date = " ", extra_preamble = list()):
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
        self.maketitle = False
        self.indentparagraphs = True
        self.doublespaceparagraphs = False
        self.nomenclature_used = False
        self.debug = False

    def __repr__(self):
        rv = "LaTeX " + self.Type.capitalize() + " (" + str(len(self.Content)) + " ish lines)"
        return rv

    def MakeTitle(self):
        self.maketitle = True

    def Debug(self):
        self.debug = True

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

        assert(type(subsection_title) is str)
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

        if (self.doublespaceparagraphs):
            self.Content.append(r"\newline\newline")
        if (not self.indentparagraphs):
            self.Content.append(r"\noindent")
        self.Content.append(paragraph)
        self.Content.append("")
        
    def AddEquation(self, equation, equation_type="equation", label = None, numbered = True):

        if (type(equation) is str):
            equation = [equation]
        elif (type(equation) is list):
            assert(type(equation[0]) is str)
        else:
            assert(type(equation) is str)  # will fail
        assert(type(equation_type) is str)
        assert(((type(label) is str) or (label == None)))
        assert(type(numbered is bool))

        if not numbered and not "*" in equation_type: equation_type += "*"

        line = r"\begin{" + equation_type + "}"
        if (label != None):
            line += r"\label{" + label + "}"
        self.Content.append(line)
        for s in equation:
            self.Content.append(s)
        self.Content.append(r"\end{" + equation_type + "}")

    def AddTable(self, *args, horiz_lines = False, vert_lines = False, both_lines = False, bold_header = False, centered = True):
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

        if (centered): self.Content.append(r"\begin{center}")
            
        line = r"\begin{tabular}{"
        if (horiz_lines): line += "|"
        for i in range(lcols):
            line += "c "
            if (horiz_lines): line += "|"
        line += "}"
        
        self.Content.append(line)
        if (vert_lines): self.Content.append(r"\hline")
        for a in args:
            line = ""
            for c in a:
                line += str(c) + "&"
            line = line[:-1] + r"\\"
            if (bold_header and args[0] == a): line += r"\hline"
            self.Content.append(line)
            if (vert_lines): self.Content.append(r"\hline")
        self.Content.append(r"\end{tabular}")
        if (centered): self.Content.append(r"\end{center}")

    def AddNomenclature(self, symbol, description, prefix = None):
        line = r"\nomenclature"
        if (prefix != None):
            line += "[" + prefix + "]"
        line += "{" + symbol + "}{" + description + "}"
        self.Content.append(line)
        self.nomenclature_used = True
    
    def GetTeX(self):
        tex = list()
        tex.append(r"\documentclass{" + self.Type + "}")
        if not self.debug: tex.append(r"\batchmode") # reduces compiler output
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

        if (self.nomenclature_used): tex.append(r"\printnomenclature")
            
        if (self.Bibfile):
            tex.append(r"\bibliography{" + self.Bibfile + "}")
            tex.append(r"\bibliographystyle{" + self.Bibstyle + "}")
            
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
        print("**** Initial build *************************************\n")
        sp.call("pdflatex " + self.OutputName + ".tex", shell = True)
        print("\n\n********************************************************")
        print("**** Bibliography **************************************\n")
        sp.call("bibtex " + self.OutputName, shell = True)
        if (self.nomenclature_used):
            print("\n\n********************************************************")
            print("**** Nomenclature **************************************\n")
            sp.call("makeindex " + self.OutputName + ".nlo -s " + "nomencl.ist -o " + self.OutputName + ".nls", shell = True)
        
        print("\n\n********************************************************")
        print("**** Penultimate Build *********************************\n")
        sp.call("pdflatex " + self.OutputName + ".tex", shell = True)
        
        print("\n\n********************************************************")
        print("**** Final build ***************************************\n")
        sp.call("pdflatex " + self.OutputName + ".tex", shell = True)
        sp.call("rm -rf *.aux *.log *.bbl *.blg *~ *.ilg *.nls *.nlo", shell = True)

def TeX_Replace(string, *args):

    assert(string.count("##") == len(args))

    for a in args:
        if (type(a) is float):
            a = "{:.3f}".format(a)
        string = string.replace("##", str(a), 1)

    return string
