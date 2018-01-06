from pylatex import *

r = LaTeX_Article()

# You can use the standard maketitle attributes
r.Title = r"Example PyLaTeX Article"
r.Author = "M. Python"
r.Date = "January 2018"
r.MakeTitle()

# If stuff stops working, or you want more information about the compilation,
# turn on debug mode to show more information.
# r.Debug()

r.AddSection("Introduction")
r.AddParagraph("PyLaTeX is an easy way to build up a write up at the same time as the calculation. It has similar features to a simple \LaTeX document.")

# You can add equations
r.AddEquation(r"a^2 = b^2 + c^2", label = "pythagoras_theorem")

# You can use nomenclature
r.AddNomenclature("a", "The long side of a right-angled triangle")
r.AddNomenclature("b", "One of the two shorter sides of a right-angled triangle")
r.AddNomenclature("c", "One of the two shorter sides of a right-angled triangle")

r.AddParagraph(r"Equation \ref{pythagoras_theorem} is an example of an equation. Equations can also have data substituted in from a list of values:")
r.AddEquation(r"a^2 = b^2 + c^2 = #0^2 + #1^2 = #2 + #3 = #4", label = "pythagoras_theorem_filled", subslist = [3, 4, 9, 16, 25])
r.AddParagraph(r"Hash symbols (\#) followed by an integer indicates a substitution.")

# You can add appendices too
r.AppendixAddSection("Appendix A", numbered = False)
r.AppendixAddParagraph("Appendices can be added at any point, they will always be at the end of the document.")

# When you're done, write it out or compile it (or both)
r.Output("report")  # No need to add '.tex' to the file name, but it doesn't matter if you do.
r.Compile()
