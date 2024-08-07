# from components.state import State
# import solara
#
# @solara.component
# def EntityStats():
#     """
#         Display the aggregated entity stats found in the input text
#     """
#     # with solara.lab.Tabs():
#     # with solara.lab.Tab("Entity Stats", disabled=State.entity_stats.value is None):
#     entity_stats = State.entity_stats.value
#     with solara.Columns(1,1):
#         if entity_stats is not None:
#             with solara.Column():
#                     solara.DataFrame(entity_stats)
#             with solara.Column():
#                 def get_data():
#                     return entity_stats.to_csv(index=False)
#                 with solara.Row(margin=3):
#                     solara.FileDownload(get_data, label=f"Download {len(entity_stats):,} csv",
#                                 filename="anonymised_texts.csv")
#
#
#
#
#
#
