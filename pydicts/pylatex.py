"""
    This class is used with the pylatex module to generate table from pydicts structures
    You only have to import pylatex if you're testing
"""


from pylatex import LongTabularx, MultiColumn
from pylatex.basic import NewLine
from pylatex.utils import NoEscape, bold, escape_latex
from pydicts import lod
def pylatex_table(
    doc, 
    lod_, 
    code_=None, 
    text_no_results="No data to show", 
):
    """
    Creates a table in a pylatex document

    @param doc pylatex document object
    @param lod 
    @param code_ |c|r|l|
    """
    
    keys= lod.lod_keys(lod_)
    if keys is None:
        doc.append(text_no_results)
        doc.append(NewLine())
        return
        
    headers=[]
    for key in keys:
        headers.append(NoEscape(bold(key)))
    
    # Generate data table
    number=0.9/len(headers)
    if code_ is None:
        code_=f"|p{{{number}\\linewidth}}"*len(headers)+"|"
        
    with doc.create(LongTabularx(code_)) as data_table:
        data_table.add_hline()
        data_table.add_row(headers)
        data_table.add_hline()
        data_table.end_table_header()
        data_table.add_hline()
        data_table.add_row((MultiColumn(len(headers), align='r', data='La tabla continúa en la siguiente página'),))
        data_table.end_table_footer()
        data_table.end_table_last_footer()

        escaped_list=[]
        for list_ in lod.lod2lol(lod_):
            row=[]
            for column in range(len(headers)):
                row.append(escape_latex(list_[column]))#Escape values
            escaped_list.append(row)

        for list_ in escaped_list:
            data_table.add_row(list_)
            data_table.add_hline()

    
def pylatex_table_with_matched_values(
    doc, 
    values_to_match, 
    lod_, 
    code_=None, 
    text_no_results="No data to show", 
    match_color="teal", 
    unmatch_color="red"
):
    """
    Creates a table in a pylatex document
    
    This function needs to have xcolor package loaded in document with
    doc.packages.append(Package('xcolor'))

    @param doc pylatex document object
    @param values_to_match Values to match is a list
    @param lod 
    @param code_ |c|r|l|   Para usar wrapping |p{.20\\linewidth\p{.80\\linewidth}|
    """
    keys= lod.lod_keys(lod_)
    if keys is None:
        doc.append(text_no_results)
        doc.append(NewLine())
        return
        
    headers=[]
    for key in keys:
        headers.append(NoEscape(bold(key)))
  
    # Generate data table
    number=0.9/len(headers)
    if code_ is None:
        code_=f"|p{{{number}\\linewidth}}"*len(headers)+"|"
        
    with doc.create(LongTabularx(code_)) as data_table:
        data_table.add_hline()
        data_table.add_row(headers)
        data_table.add_hline()
        data_table.end_table_header()
        data_table.add_hline()
        data_table.add_row((MultiColumn(len(headers), align='r', data='La tabla continúa en la siguiente página'),))
        data_table.end_table_footer()
        data_table.end_table_last_footer()

        #Prepare cells
        matched_list=[]
        for list_ in lod.lod2lol(lod_):
            row=[]
            for column in range(len(headers)):
                if list_[column]==values_to_match[column]:
                    row.append(NoEscape(f"\\textcolor{{{match_color}}}{{{escape_latex(list_[column])}}}"))
                else:
                    row.append(NoEscape(f"\\textcolor{{{unmatch_color}}}{{{escape_latex(list_[column])}}}"))
            matched_list.append(row)
                
        
        for list_ in matched_list:
            data_table.add_row(list_)
            data_table.add_hline()
            

#    doc.append(NewLine())
