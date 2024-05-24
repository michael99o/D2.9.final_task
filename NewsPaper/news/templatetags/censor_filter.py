from django import template

register = template.Library()

CENSOR_WORDS = [
    'дурак', 'придурок', 'идиот',
]


@register.filter()
def censor(text):
    words = text.split()
    for i, word in enumerate(words):
        if word.lower().replace(',', '').replace('.', '').replace('!', '').replace('?', '') in CENSOR_WORDS:
            words[i] = word[0] + '*' * (len(word) - 1)

    return " ".join(words)
