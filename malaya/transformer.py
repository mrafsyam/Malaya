from herpetologist import check_type

_availability = {
    'bert': ['base'],
    'xlnet': ['base'],
    'alxlnet': ['base'],
    'albert': ['base', 'large'],
}


def available_model():
    """
    List available transformer models.
    """
    return _availability


@check_type
def load(
    size: str = 'base', model: str = 'xlnet', pool_mode: str = 'last', **kwargs
):

    """
    Load transformer model.

    Parameters
    ----------
    model : str, optional (default='bert')
        Model architecture supported. Allowed values:

        * ``'bert'`` - BERT architecture from google.
        * ``'xlnet'`` - XLNET architecture from google.
        * ``'alxlnet'`` - XLNET architecture from google + Malaya.
        * ``'albert'`` - ALBERT architecture from google.
    size : str, optional (default='base')
        Model size supported. Allowed values:

        * ``'base'`` - BASE size.
        * ``'small'`` - SMALL size.
        * ``'large'`` - LARGE size.
    pool_mode : str, optional (default='last')
        Model logits architecture supported. Only usable if model = 'xlnet'. Allowed values:

        * ``'last'`` - last of the sequence.
        * ``'first'`` - first of the sequence.
        * ``'mean'`` - mean of the sequence.
        * ``'attn'`` - attention of the sequence.

    Returns
    -------
    TRANSFORMER: malaya.transformer class
    """

    model = model.lower()
    size = size.lower()
    if model not in _availability:
        raise Exception(
            'model not supported, please check supported models from malaya.transformer.available_model()'
        )
    if size not in _availability[model]:
        raise Exception(
            'size not supported, please check supported models from malaya.transformer.available_model()'
        )
    if model == 'bert':
        from ._transformer import _bert

        return _bert.bert(model = size, **kwargs)
    if model == 'albert':
        from ._transformer import _albert

        return _albert.albert(model = size, **kwargs)
    if model == 'xlnet':
        from ._transformer import _xlnet

        return _xlnet.xlnet(model = size, pool_mode = pool_mode, **kwargs)

    if model == 'alxlnet':
        from ._transformer import _alxlnet

        return _alxlnet.alxlnet(model = size, pool_mode = pool_mode, **kwargs)
