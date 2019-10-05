REPLIES = {
    'en': {
        'greetings': ['Hi there.', 'Hello!', 'Hi, how are you doing?'],
    },
    'ar': {
        'greetings': ['مرحبا'],
    }
}

DICTIONARY = {
    r'hi(\W|$).*': 'en.greetings',
    r'hello(\W|$).*': 'en.greetings',
    r'hey(\W|$).*': 'en.greetings',
    r'مرحبا(\W|$).*': 'ar.greetings',
}

