# PyLaTeX

Are you like me? Do you write lengthy python scripts to perform a calculation from logged data? Do you then have to copy the information over to a report? Isn't this just the most tiresome thing? PyLaTeX seeks to end this faff!

PyLaTeX is a collection of python classes which represent LaTeX documents (`article`, `report`, `book`). As you go along writing your (lenghty, complex) calculation script you can on the fly write the report/article (as you might comment your code). Then, when the script is done, the report is done too! You can have it automatically compile to pdf, or just output to .tex.

# Quick Usage
```
from pylatex import *

r = LaTeX_Article()
r.AddSection("Introduction")
r.AddSubsection("SubIntro")
r.AddParagraph("Lorem ipsum etc")
r.AddEquation(r"a^2 = b^2 + c^2", label = "pythagoras_theorem")
r.AddParagraph(r"Equation \ref{pythagoras_theorem} is an example of an equation. Equations can also have data inserted from a list of values (similar to python2's str.replace()):")
r.AddEquation(r"a^2 = b^2 + c^2 = #0^2 + #1^2 = #2 + #3 = #4", label = "pythagoras_theorem", subslist = [3, 4, 9, 16, 25])

r.AppendixAddSection("Appendix A", numbered = False)
r.AppendixAddParagraph("Appendices can be added at any point, they will always be at the end of the document.")
```
You get the gist.

# Packages

Bibliographies are supported through `bibtex`

Equations are written in TeX math (using `amsmath`, `amsfont`, and `amssymb`).

Figures can be added (`graphicx` used to add images), with subfigure support through `subcaption` (`caption` is loaded too)

Extra packages can be added in the `ExtraPreamble` attribute of a document. Or, indeed, anything else you could want to add into the preamble.

# License
PyLaTeX is distrubuted under [GPL-3.0](https://www.gnu.org/licenses/gpl-3.0.en.html) so feel free to share, adapt, do whatever to this but be warned it is supplied with no warranty or guarantee that it will work or indeed do anything useful.