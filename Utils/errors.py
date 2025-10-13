class InputErrors(Exception):
    """
    All Errors that relate to Invalid Input data coming must be child classes of this Exception
    """

    pass


class ProcessingErrors(Exception):
    """
    All Errors that relate to or are raised while processing must be child classes of this Exception
    """

    pass


class RequiredDataMissing(InputErrors):
    """
    If a Required field was missing in the input data
    """

    pass


class RequiredSectionConditionMissing(InputErrors):
    """
    Condition not satisfied for a required section
    """

    pass


class UnRecognizedType(ProcessingErrors):
    pass


class RequiredDataNotProvided(ProcessingErrors):
    pass
