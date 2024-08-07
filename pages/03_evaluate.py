from solara.tasks import task

from components.main_sidebar import Sidebar
from components.state import State
from components.anonymisers import Anonymiser
from tools.dataframe_filter import *
from typing import cast, Optional
from pandas import DataFrame

import solara, pandas

one_per_row = solara.reactive(cast(Optional[bool],True))
evaluation_data = solara.reactive(cast(Optional[DataFrame],None))

eval_columns = ["entity_string", "entity_type", "message", "score", "explanation", "meta"]

@solara.component
def Page():
    Sidebar()
    if State.dataset.value is not None:
        df = State.dataset.value
        with solara.Columns([2,1]):
            with solara.Column():
                solara.DataFrame(df)
            with solara.Column():
                solara.ProgressLinear(create_evaluation_data.progress)
                with solara.Card(margin=5):
                    solara.Checkbox(label="One entity per row", value=one_per_row)
                    with solara.Row():
                        solara.Button(label="Create Eval Set", on_click=create_evaluation_data)
                    if create_evaluation_data.finished:
                        with solara.Row(margin=3):
                            def get_data():
                                return evaluation_data.value.to_csv(index=False)
                            solara.FileDownload(get_data, label=f"Download {len(evaluation_data.value):,} csv",
                                                filename="eval_outputs.csv")


@task
def create_evaluation_data():
    create_evaluation_data.progress = True
    output_df = DataFrame(columns=eval_columns)
    df = State.dataset.value
    if df is not None:
        output_df = pandas.concat(list(df.apply(lambda row: get_entity_info(row),axis=1)))
        # output_df = df.apply(lambda row: get_entity_info(row), axis=1)
    evaluation_data.set(output_df)
    create_evaluation_data.progress = False



def get_entity_info(row):
    # can't use defaultdict or it will error if results are empty
    eval_outputs = {col : [] for col in eval_columns}
    column = State.anony_column.value
    results_col = create_results_column(State.anony_column.value)
    if State.anonymiser.value == Anonymiser.PRESIDIO:
        text = row[column]
        results = row[results_col]
        for result in results:
            entity_string = text[result.start:result.end]
            eval_outputs["entity_type"].append(result.entity_type)
            eval_outputs["entity_string"].append(entity_string)
            eval_outputs["score"].append(result.score)
            eval_outputs["meta"].append(result.recognition_metadata)
            eval_outputs["explanation"].append(result.analysis_explanation)
            eval_outputs["message"].append(text)
    return pandas.DataFrame.from_dict(eval_outputs)














