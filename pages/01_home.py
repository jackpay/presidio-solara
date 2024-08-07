from components.main_sidebar import Sidebar
from tools.presidio import *
import solara


@solara.component
def Page():
    # Data upload options
    Sidebar()
    df = State.dataset.value
    with solara.Columns([2,1]):
        with solara.Column():
            ## Dataset to process
            if df is not None:
                solara.DataFrame(df)

        with solara.Column():
            ## Processing progres
            if analyse_and_anonymise_texts.not_called:
                solara.ProgressLinear(False)
            else:
                solara.ProgressLinear(analyse_and_anonymise_texts.progress)

            ## Processing params
            with solara.Card():
                if df is not None:
                    solara.Select(label="Anonymise column", value=State.anony_column, values=df.columns.to_list())
                solara.Checkbox(label="Find all entities", value=State.anonymise_all)
                solara.SelectMultiple(label="Entities", values=State.anony_entities, all_values=entities, disabled=State.anonymise_all.value)
                with solara.Row():
                    solara.SliderFloat(label="Acceptance Threshold:", value=State.threshold, min=0.01, max=1.0, step=0.01)

                solara.Button("Process texts", on_click=process_texts, disabled=df is None)
        # # if analyse_and_anonymise_texts.finished:
        # with solara.lab.Tab("Entity Stats", disabled=State.entity_stats.value is None):
        #     if State.entity_stats.value is not None:
        #         EntityStats()
        # with solara.lab.Tab("Download", disabled=State.dataset.value is None):
        #     if State.dataset.value is not None:
        #         Download()
            # """
            #     Display the aggregated entity stats found in the input text
            # """
            # entity_stats = State.entity_stats.value
            # with solara.Columns(1, 1):
            #     if entity_stats is not None:
            #         with solara.Column():
            #             solara.DataFrame(entity_stats)
            #         with solara.Column():
            #             def get_data():
            #                 return entity_stats.to_csv(index=False)
            #
            #             with solara.Row(margin=3):
            #                 solara.FileDownload(get_data, label=f"Download {len(entity_stats):,} csv",
            #                                     filename="anonymised_texts.csv")


def process_texts():
    """
        Use the selected anonymiser tool to redact PII from the input text
    """
    df = State.dataset.value
    column = State.anony_column.value
    ents = entities if State.anonymise_all.value else State.anony_entities.value
    min_conf = State.threshold.value
    analyse_and_anonymise_texts(dataframe=df,column=column,minimum_confidence=min_conf,detect_entities=ents)







