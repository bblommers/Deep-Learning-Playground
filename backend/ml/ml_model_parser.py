from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier

def get_object_ml(element):
    """
    Given a string representation of a model object, return the properly
    instantiated object

    Args:
        element (string): string representation of the model with parameters

    return:
        Instantiated object behind with the parameters passed in
    """
    return eval(
        element
    )  # takes in the string representation and returns the "instantiated object"

