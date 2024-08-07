import solara
from components.state import State
from tools.dataframe_filter import *
from typing import Optional, cast
from components.main_sidebar import Sidebar

download_all = solara.reactive(cast(Optional[bool], False))
download_redacted = solara.reactive(cast(Optional[bool], True))
download_columns = solara.reactive(cast(Optional[list], []))
download_all_entities = solara.reactive(cast(Optional[bool],False))
download_entities = solara.reactive(cast(Optional[list],[]))
sample_size = solara.reactive(cast(Optional[int],0))
matched_entities = solara.reactive(cast(Optional[list], []))

@solara.component
def Page():
    if download_all.value:
        download_redacted.set(False)
    if State.dataset.value is not None:
        with solara.Columns([2,1]):
            with solara.Column():
                    solara.DataFrame(State.dataset.value)
            with solara.Column():
                with solara.Card("Download options"):
                    solara.Checkbox(label="Download all", value=download_all)
                    solara.Checkbox(label="Download redacted", value=download_redacted, disabled=download_all.value)
                    with solara.Row():
                        columns = State.dataset.value.columns.to_list()
                        solara.SelectMultiple(label="Download columns", values=download_columns, all_values=columns,
                                              disabled=download_all.value or download_redacted.value)
                    with solara.Row():
                            solara.Checkbox(label="Download all entity  matches", value=download_all_entities)
                    if State.entity_stats.value is not None:
                        with solara.Row():
                            matched_entities.set(State.entity_stats.value["index"].to_list())
                            solara.SelectMultiple(label="Download entities", values=download_entities, all_values=matched_entities.value,
                                                  disabled=download_all_entities.value)
                        with solara.Row():
                            solara.InputInt(label="Sample size", value=sample_size)


                    def get_data():
                        df = filter_dataframe();
                        return df.to_csv(index=False)

                    with solara.Row(margin=3):
                        solara.FileDownload(get_data, label=f"Download csv", filename="download.csv")

def filter_dataframe():
    df = State.dataset.value
    column = State.anony_column.value
    red_column = create_redacted_column(column)
    ## Filter the entities
    if not download_all_entities.value:
        df = df.query(create_entity_query())
    ## Filter the download columns
    if download_redacted.value:
        df = df[[column,red_column]]
    elif not download_all.value:
        df = df[[download_columns.value]]
    if sample_size.value > 0 & len(df) > sample_size.value:
        df = df.sample(sample_size.value)
    return df

def create_entity_query():
    query =  " & ".join([entity + "==True" for entity in matched_entities.value])
    return query