import solara

from components.state import State


@solara.component
def Sidebar():
    df = State.dataset.value
    with solara.Sidebar():
        with solara.Card("Data upload", margin=1, elevation=1):
            with solara.Row(margin=3):
                if 0 < State.upload_progress.value < 100:
                    solara.ProgressLinear(value=State.upload_progress.value)
                else:
                    solara.ProgressLinear(False)
            with solara.Column():
                with solara.Row():
                    # solara.Button("Sample dataset", color="primary", text=True, outlined=True, on_click=State.load_sample, disabled=len(dataframes) > 0)
                    solara.Button("Clear", color="primary", text=True, outlined=True, on_click=State.reset, disabled=df is None)
                solara.FileDrop(on_file=State.load_from_file, on_total_progress=State.upload_progress.set, label=State.path.value)
