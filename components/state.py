from typing import Optional, cast
from components.anonymisers import Anonymiser
from pandas import DataFrame
import solara, pandas as pd, pickle

class State():

    ## The dataset to perform PII removal
    dataset = solara.reactive(cast(Optional[DataFrame], None))

    drag_placeholder = "Drag file here"
    sample_name = "sample"

    error_message = solara.reactive(cast(Optional[str], None))

    # ## Display fields
    # dataset = solara.reactive(cast(Optional[str], None))

    ## Data upload fields
    path = solara.reactive(cast(Optional[str], drag_placeholder))
    upload_progress = solara.reactive(cast(Optional[int], 0))

    ## PII tools
    anonymisers = [e.value for e in Anonymiser]

    ## Presidio params
    # How aggressive to set the threshold for an accepted match
    default_thresh = 0.33
    threshold = solara.reactive(cast(Optional[float], default_thresh))

    # Anonymise all columns
    anonymise_all = solara.reactive(False)
    # Which columns
    anony_column = solara.reactive(cast(Optional[str], None))
    # Which entities
    anony_entities = solara.reactive(cast(Optional[list], []))
    # Aggregated entity stats
    entity_stats = solara.reactive(cast(Optional[DataFrame], None))

    anonymiser = solara.reactive(cast(Optional[Anonymiser],Anonymiser.PRESIDIO))

    @staticmethod
    def load_from_file(file):
        """
            Upload a file for anonymisation
        :param file: The file information and object
        """
        State.error_message.value = None
        df = None
        name = file['name']
        if file['name'].endswith('csv'):
            df = pd.read_csv(file["file_obj"])
        elif file['name'].endswith('.p'):
            df = pickle.load(file['file_obj'])
        else:
            State.error_message.value = "The uploading file-type needs to be csv"
        if df is not None:
            State.dataset.set(df)
            State.path.value = name
        State.upload_progress.value = 0

    @staticmethod
    def reset():
        """
            Reset the main app defaults
        """
        State.dataset.set(None)
        State.path.set(State.drag_placeholder)
        State.threshold.set(State.default_thresh)
        State.entity_stats.set(None)
        State.upload_progress.value = 0