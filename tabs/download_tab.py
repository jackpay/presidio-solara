# import solara
# from components.state import State
# from typing import Optional, cast
# from tools.dataframe_filter import *
#
# download_all = solara.reactive(cast(Optional[bool], False))
# download_redacted = solara.reactive(cast(Optional[bool], True))
# download_columns = solara.reactive(cast(Optional[list], []))
# download_all_entities = solara.reactive(cast(Optional[bool],False))
# download_entities = solara.reactive(cast(Optional[list],[]))
#
# @solara.component
# def Download():
#     with solara.Columns([2,1]):
#         with solara.Column():
#             solara.DataFrame(State.dataset.value)
#         with solara.Column():
#             with solara.Card("Download options"):
#                 solara.Checkbox(label="Download all", value=download_all)
#                 solara.Checkbox(label="Download redacted", value=download_redacted, disabled=download_all.value)
#                 with solara.Row():
#                     columns = State.dataset.value.columns
#                     solara.SelectMultiple(label="Download columns", values=download_columns, all_values=columns,
#                                           disabled=download_all.value or download_redacted.value)
#                 with solara.Row():
#                     if State.entity_stats.value is not None:
#                         solara.Checkbox(label="Download all entity  matches", value=download_all_entities)
#                         matched_entities = State.entity_stats.value.columns.to_list()
#                         solara.SelectMultiple(label="Download entities", values=download_entities, all_values=matched_entities,
#                                               disabled=download_all_entities.value)
#
#         def get_data():
#             df = filter_dataframe();
#             return df.to_csv(index=False)
#
#         with solara.Row(margin=3):
#             solara.FileDownload(get_data, label=f"Download csv", filename="anonymised_texts.csv")
#
# def filter_dataframe():
#     df = State.dataset.value
#     ## Filter the entities
#     if not download_all_entities.value:
#         df = df.query(create_entity_query())
#     ## Filter the download columns
#     if download_redacted.value:
#         red_column = create_redacted_column(State.anony_column.value)
#         df = df[red_column]
#     elif not download_all:
#         df = df[[download_columns.value]]
#     return df
#
# def create_entity_query():
#     " & ".join([entity + "==True" for entity in download_entities.value])