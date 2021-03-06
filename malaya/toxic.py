from malaya.function import (
    check_file,
    load_graph,
    check_available,
    generate_session,
)
from malaya.text.bpe import (
    sentencepiece_tokenizer_bert,
    sentencepiece_tokenizer_xlnet,
)
from malaya.path import PATH_TOXIC, S3_PATH_TOXIC
from malaya.model.ml import MULTILABEL_BAYES
from malaya.model.bert import SIGMOID_BERT
from malaya.model.xlnet import SIGMOID_XLNET

from malaya.transformer.bert import bert_num_layers
from herpetologist import check_type

_label_toxic = [
    'toxic',
    'severe_toxic',
    'obscene',
    'threat',
    'insult',
    'identity_hate',
]


_availability = {
    'bert': ['base', 'small'],
    'xlnet': ['base'],
    'albert': ['base'],
}


def available_transformer_model():
    """
    List available transformer toxicity analysis models.
    """
    return _availability


def multinomial(**kwargs):
    """
    Load multinomial toxicity model.

    Parameters
    ----------
    validate: bool, optional (default=True)
        if True, malaya will check model availability and download if not available.

    Returns
    -------
    BAYES : malaya._models._sklearn_model.MULTILABEL_BAYES class
    """
    import pickle

    check_file(
        PATH_TOXIC['multinomial'], S3_PATH_TOXIC['multinomial'], **kwargs
    )

    try:
        with open(PATH_TOXIC['multinomial']['model'], 'rb') as fopen:
            multinomial = pickle.load(fopen)
        with open(PATH_TOXIC['multinomial']['vector'], 'rb') as fopen:
            vectorize = pickle.load(fopen)
    except:
        raise Exception(
            "model corrupted due to some reasons, please run malaya.clear_cache('toxic/multinomial') and try again"
        )
    from .stem import _classification_textcleaning_stemmer

    return MULTILABEL_BAYES(
        models = multinomial,
        vectors = vectorize,
        cleaning = _classification_textcleaning_stemmer,
    )


@check_type
def transformer(model: str = 'xlnet', size: str = 'base', **kwargs):
    """
    Load Transformer emotion model.

    Parameters
    ----------
    model : str, optional (default='bert')
        Model architecture supported. Allowed values:

        * ``'bert'`` - BERT architecture from google.
        * ``'xlnet'`` - XLNET architecture from google.
        * ``'albert'`` - ALBERT architecture from google.
    size : str, optional (default='base')
        Model size supported. Allowed values:

        * ``'base'`` - BASE size.
        * ``'small'`` - SMALL size.

    Returns
    -------
    BERT : malaya._models._bert_model.BINARY_BERT class
    """

    model = model.lower()
    size = size.lower()
    if model not in _availability:
        raise Exception(
            'model not supported, please check supported models from malaya.sentiment.available_transformer_model()'
        )
    if size not in _availability[model]:
        raise Exception(
            'size not supported, please check supported models from malaya.sentiment.available_transformer_model()'
        )

    check_file(PATH_TOXIC[model][size], S3_PATH_TOXIC[model][size], **kwargs)
    g = load_graph(PATH_TOXIC[model][size]['model'])

    if model in ['albert', 'bert']:
        if model == 'bert':
            from ._transformer._bert import _extract_attention_weights_import
        if model == 'albert':
            from ._transformer._albert import _extract_attention_weights_import

        tokenizer, cls, sep = sentencepiece_tokenizer_bert(
            PATH_TOXIC[model][size]['tokenizer'],
            PATH_TOXIC[model][size]['vocab'],
        )

        return SIGMOID_BERT(
            X = g.get_tensor_by_name('import/Placeholder:0'),
            segment_ids = None,
            input_masks = None,
            logits = g.get_tensor_by_name('import/logits:0'),
            logits_seq = g.get_tensor_by_name('import/logits_seq:0'),
            sess = generate_session(graph = g),
            tokenizer = tokenizer,
            label = _label_toxic,
            cls = cls,
            sep = sep,
            attns = _extract_attention_weights_import(bert_num_layers[size], g),
            class_name = 'toxic',
        )
    if model in ['xlnet']:
        from ._transformer._xlnet import _extract_attention_weights_import

        tokenizer = sentencepiece_tokenizer_xlnet(
            PATH_TOXIC[model][size]['tokenizer']
        )

        return SIGMOID_XLNET(
            X = g.get_tensor_by_name('import/Placeholder:0'),
            segment_ids = g.get_tensor_by_name('import/Placeholder_1:0'),
            input_masks = g.get_tensor_by_name('import/Placeholder_2:0'),
            logits = g.get_tensor_by_name('import/logits:0'),
            logits_seq = g.get_tensor_by_name('import/logits_seq:0'),
            sess = generate_session(graph = g),
            tokenizer = tokenizer,
            label = _label_toxic,
            attns = _extract_attention_weights_import(g),
            class_name = 'toxic',
        )
