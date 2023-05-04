from pydicts import pylatex
from pylatex import Document, Section, Subsection
from pylatex.package import Package
from pylatex.utils import italic, NoEscape
lod=[
        {"year": 2022, "month": 1, "my_sum": 12},
        {"year": 2021, "month": 2, "my_sum": 123},
        {"year": 2019, "month": 5, "my_sum": 1},
        {"year": 2022, "month": 12, "my_sum": 12},
]
def tests_pylatex_table_header():

    doc = Document()
    doc.packages.append(Package('xcolor'))

    with doc.create(Section('A section')):
        doc.append('Some regular text and some ')
        doc.append(italic('italic text. '))

        with doc.create(Subsection('A subsection')):
            doc.append('Also some crazy characters: $&#{}')
            
    doc.append(NoEscape("\\centering"))
    pylatex.pylatex_table(doc, lod)
    pylatex.pylatex_table(doc, [])
    pylatex.pylatex_table_with_matched_values(doc,  [2022, 2, 12], lod, code_="|l|c|r|", match_color="teal", unmatch_color="red")
    doc.generate_pdf('test_pylatex_table_header', clean_tex=False)
