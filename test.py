from pylatex import *

r = LaTeX_Document()
r.AddParagraph(r"Hello, World!")

r.Output("test.tex")
r.Compile()
