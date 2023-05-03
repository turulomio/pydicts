"""
    This class is used with the pylatex module to generate table from pydicts structures
    You only have to import pylatex if you're testing
"""


from pylatex import Tabular
from pylatex.basic import NewLine
from pylatex.utils import NoEscape
from pydicts import lod
def pylatex_table_header(
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
    
    headers=lod.lod_keys(lod_)
    
    if headers is None:
        doc.append(text_no_results)
        doc.append(NewLine())
        return
    
    
    # Generate data table
    if code_ is None:
        code_="|l"*len(headers)+"|"
        
    with doc.create(Tabular(code_)) as data_table:
        data_table.add_hline()
        data_table.add_row(headers)
        data_table.add_hline()
        for list_ in lod.lod2lol(lod_):
            data_table.add_row(list_)
            data_table.add_hline()

    doc.append(NewLine())
    
def pylatex_table_with_matched_values(
    doc, 
    values_to_match, 
    lod_, 
    code_=None, 
    text_no_results="No data to show", 
    match_color="green", 
    unmatch_color="black"
):
    """
    Creates a table in a pylatex document
    
    This function needs to have xcolor package loaded in document with
    doc.packages.append(Package('xcolor'))

    @param doc pylatex document object
    @param values_to_match Values to match is a list
    @param lod 
    @param code_ |c|r|l|
    """
    
    headers=lod.lod_keys(lod_)
    
    if headers is None:
        doc.append(text_no_results)
        doc.append(NewLine())
        return
    
    
    # Generate data table
    if code_ is None:
        code_="|l"*len(headers)+"|"
        
    with doc.create(Tabular(code_)) as data_table:
        data_table.add_hline()
        data_table.add_row(headers)
        data_table.add_hline()
        
        #Prepare cells
        matched_list=[]
        for list_ in lod.lod2lol(lod_):
            row=[]
            for column in range(len(headers)):
                if list_[column]==values_to_match[column]:
                    row.append(NoEscape(f"\\textcolor{{{match_color}}}{{{values_to_match[column]}}}"))
                else:
                    row.append(NoEscape(f"\\textcolor{{{unmatch_color}}}{{{values_to_match[column]}}}"))
            matched_list.append(row)
                
        
        for list_ in matched_list:
            data_table.add_row(list_)
            data_table.add_hline()
            

    doc.append(NewLine())
