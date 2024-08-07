from components.state import State
from components.main_sidebar import Sidebar
import solara

@solara.component
def Page():

    Sidebar()
    """
        Display the aggregated entity stats found in the input text
    """
    entity_stats = State.entity_stats.value
    with solara.Columns(1,1):
        if entity_stats is not None:
            with solara.Column():
                    solara.DataFrame(entity_stats)
            with solara.Column():
                def get_data():
                    return entity_stats.to_csv(index=False)
                with solara.Row(margin=3):
                    solara.FileDownload(get_data, label=f"Download {len(entity_stats):,} csv",
                                filename="anonymised_texts.csv")






