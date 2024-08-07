"""
    Set of methods to create column headings for dataframe output
"""
_results_column = "_analysis_results"
_redacted_column = "_redacted"
def create_results_column(column):
    return column + _results_column

def create_redacted_column(column):
    return column + _redacted_column

def create_entity_column(column, entity_name):
    return column + "_" + entity_name