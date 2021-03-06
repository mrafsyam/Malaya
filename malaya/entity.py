from malaya.supervised import tag
from malaya.path import PATH_ENTITIES, S3_PATH_ENTITIES
from malaya.text.entity import _Entity_regex
from herpetologist import check_type

_availability = [
    'bert',
    'tiny-bert',
    'albert',
    'tiny-albert',
    'xlnet',
    'alxlnet',
]


def available_transformer_model():
    """
    List available transformer Entity Tagging models.
    """
    return _availability


@check_type
def transformer(model: str = 'xlnet', **kwargs):
    """
    Load Transformer Entity Tagging model, transfer learning Transformer + CRF.

    Parameters
    ----------
    model : str, optional (default='bert')
        Model architecture supported. Allowed values:

        * ``'bert'`` - BERT architecture from google.
        * ``'tiny-bert'`` - BERT architecture from google with smaller parameters.
        * ``'albert'`` - ALBERT architecture from google.
        * ``'tiny-albert'`` - ALBERT architecture from google with smaller parameters.
        * ``'xlnet'`` - XLNET architecture from google.
        * ``'alxlnet'`` - XLNET architecture from google + Malaya.

    Returns
    -------
    MODEL : Transformer class
    """

    model = model.lower()
    size = size.lower()
    if model not in _availability:
        raise Exception(
            'model not supported, please check supported models from malaya.entity.available_transformer_model()'
        )
    return tag.transformer(
        PATH_ENTITIES,
        S3_PATH_ENTITIES,
        'entity',
        model = model,
        size = size,
        **kwargs,
    )


def general_entity(model = None):
    """
    Load Regex based general entities tagging along with another supervised entity tagging model.

    Parameters
    ----------
    model : object
        model must has `predict` method. Make sure the `predict` method returned [(string, label), (string, label)].

    Returns
    -------
    _Entity_regex: malaya.texts._entity._Entity_regex class
    """
    if not hasattr(model, 'predict') and model is not None:
        raise ValueError('model must has `predict` method')
    return _Entity_regex(model = model)
