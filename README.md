# PyLaTeX

Are you like me? Do you write lengthy python scripts to perform a calculation from logged data? Do you then have to copy the information over to a report? Isn't this just the most tiresome thing? PyLaTeX seeks to end this faff!

PyLaTeX is a collection of python classes which represent LaTeX documents (`article`, `report`, `book`). As you go along writing your (lengthy, complex) calculation script you can on the fly write the report/article (as you might comment your code). Then, when the script is done, the report is done too! You can have it automatically compile to pdf, or just output to .tex.

# Example Usage
```python
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
```
You get the gist.

# Packages

Bibliographies are supported through `bibtex`.

Equations are written in TeX math (using `amsmath`, `amsfont`, and `amssymb`).

Figures can be added (`graphicx` used to add images), with subfigure support through `subcaption` (`caption` is loaded too).

Nomenclature is handled by the `nomencl` package.

Extra packages can be added in the `ExtraPreamble` attribute of a document. Or, indeed, anything else you could want to add into the preamble.

# License
PyLaTeX is distrubuted under [GPL-3.0](https://www.gnu.org/licenses/gpl-3.0.en.html) so feel free to share, adapt, do whatever to this but be warned it is supplied with no warranty or guarantee that it will work or indeed do anything useful.