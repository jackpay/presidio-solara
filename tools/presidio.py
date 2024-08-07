import pandas
from collections import Counter
from presidio_analyzer import AnalyzerEngine, PatternRecognizer, Pattern
from presidio_anonymizer import AnonymizerEngine
from components.state import State
from tools.dataframe_filter import *
## NB: Not used currently but may become important!!!
from presidio_anonymizer.entities import OperatorConfig

from solara.lab import task

## Removed crypto analyser as it always breaks
entities = ["PHONE_NUMBER","PERSON","URL", "CREDIT_CARD", "EMAIL_ADDRESS","IP_ADDRESS", "IBAN_CODE", "NRP","LOCATION", "MEDICAL_LICENSE", "US_BANK_NUMBER", "US_DRIVER_LICENSE", "US_ITIN", "US_PASSPORT", "US_SSN", "UK_NHS","HANDLES","HASHES"]

class PresidioWrapper():

    def __init__(self, minmium_confidence=0.33):
        self.analyser = AnalyzerEngine(default_score_threshold=minmium_confidence)
        self.anonymiser = AnonymizerEngine()
        self._add_handle_recognisers()
    def _add_handle_recognisers(self):
        """
            Creates and adds a recogniser for @ and #
        """
        self.analyser.registry.add_recognizer(create_handles_recogniser())
        self.analyser.registry.add_recognizer(create_hash_recogniser())

    def analyse_text(self, text, detect_entities=entities):
        """
            Analyses and detects the required entities in the text
            :param text The text to be analysed
            :param detect_entities The (default Presidio) entities to look for. If None all are detected
        """
        return self.analyser.analyze(text,entities=detect_entities, language='en')


    def anonymise_text(self, text, results):
        """
            Takes the results of the analyser and anonmises the text
            :param text The text to anonymise
            :param results The results produced by the analyser
            :return The original text with the discovered entities redacted
        """
        return self.anonymiser.anonymize(text=text, analyzer_results=results)


    def find_most_likely_set(self, analyser_results):
        """
            Finds the set of non-conflicted, most-likely analyser results.
            A conflict occurs when the same span of text is labelled with multiple entities
            :param analyser_results:
            :return: The set of non-conflicted, most-likely analyser results.
        """
        if len(analyser_results) <= 1:
            nonconflicted = analyser_results
        else:
            nonconflicted = set([y if x.has_conflict(y) else x for i,x in enumerate(analyser_results) for j,y in enumerate(analyser_results) if i != j])
        return list(nonconflicted)


def create_handles_recogniser():
    # Define the regex pattern in a Presidio `Pattern` object:
    handles_pattern = Pattern(name="handles_pattern", regex="@[\w\d]+", score=0.5)

    # Define the recognizer with one or more patterns
    return PatternRecognizer(
        supported_entity="HANDLES", patterns=[handles_pattern]
    )

def create_hash_recogniser():
    # Define the regex pattern in a Presidio `Pattern` object:
    handles_pattern = Pattern(name="hash_pattern", regex="#[\w\d]+", score=0.5)

    # Define the recognizer with one or more patterns
    return PatternRecognizer(
        supported_entity="HASHES", patterns=[handles_pattern]
    )

def aggregate_entities(entity_lists):
    """
        Creates an aggregated table of detected entities and counts
    :param entity_lists: The full dataset results of the presidio analysis
    :return: DataFrame tabulating entity and detection counts
    """
    aggregated_ents = Counter()
    [[aggregated_ents.update([x.entity_type]) for x in y] for y in entity_lists]
    return pandas.DataFrame.from_dict(aggregated_ents, orient='index').reset_index()

def annotate_entity_detections(presidio_analysis_results):
    """
    :param presidio_analysis_results:
    :return: a Dictionary of all entities paired with True if found else False
    """
    found_entities = set([x.entity_type for x in presidio_analysis_results])
    return {entity : (True if entity in found_entities else False) for entity in entities}

## Can't seem to use the @task attribute on class functions (can't find self)
@task
def analyse_and_anonymise_texts(dataframe, column, minimum_confidence=0.33, detect_entities=entities, allow_list=None, context_words=None):
    """
        Use the configured analyser to detect entities in the selected free-text columns of a dataframe
        :param dataframe:
        :param column: The free-text columns to analyse
        :param detect_entities: The entities to find
        :param allow_list: List of words to ignore
        :param context_words: words used to enhance the confidence score when found
        :return: The original dataframe appended with the discovered entities and redacted text
    """
    presidio = PresidioWrapper(minimum_confidence)
    results_col = create_results_column(column)
    redact_col = create_redacted_column(column)
    def process_row(row):
        text = row[column]
        results = presidio.analyse_text(text,detect_entities)
        results = presidio.find_most_likely_set(results)
        entity_annotations = annotate_entity_detections(results)
        anonymised_text = presidio.anonymise_text(text,results)
        analyse_and_anonymise_texts.progress = (row.name/len(dataframe))*100
        analysis_output = {results_col:results, redact_col:anonymised_text}
        analysis_output.update(entity_annotations)
        return pandas.Series(analysis_output)
    dataframe[[results_col,redact_col] + entities] = dataframe.apply(lambda x: process_row(x),axis=1)
    ## The dataframe with redacted data and entity counts
    # df = analyse_and_anonymise_texts.result.value
    entity_stats = aggregate_entities(dataframe[create_results_column(State.anony_column.value)].to_list())
    State.dataset.value = dataframe
    State.entity_stats.value = entity_stats
    analyse_and_anonymise_texts.progress = False
    return dataframe