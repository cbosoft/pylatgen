from pylatex import *

r = LaTeX_Article()
r.AddParagraph(r"Hello, World!")

s = r.GetTeX()
# r.Output("test.tex")
# r.Compile()
