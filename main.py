import nltk
from nltk.corpus import brown
from nltk.util import ngrams
from collections import defaultdict
import random
from spellchecker import SpellChecker

# Download dataset
nltk.download('brown')

# Initialize spell checker
spell = SpellChecker()

# Load big English text
sentences = brown.sents()

# Convert to lowercase words
words = []
for sentence in sentences:
    words.extend([word.lower() for word in sentence])

# Create trigrams (2 words -> next word)
trigrams = ngrams(words, 3)

# Build language model
model = defaultdict(list)
for w1, w2, w3 in trigrams:
    model[(w1, w2)].append(w3)

# Autocorrect function
def autocorrect_sentence(text):
    corrected_words = []
    for word in text.split():
        corrected_words.append(spell.correction(word))
    return " ".join(corrected_words)

# Predict next word
def predict_next_word(text):
    words = text.lower().split()

    if len(words) < 2:
        return "Type at least two words"

    last_two = (words[-2], words[-1])

    if last_two in model:
        return random.choice(model[last_two])
    else:
        # fallback: try using only last word
        last_word = words[-1]
        possible = []
        for (w1, w2), next_words in model.items():
            if w2 == last_word:
                possible.extend(next_words)

        if possible:
            return random.choice(possible)
        else:
            return "No prediction found"
while True:
    user_input = input("\nType a sentence (or 'exit'): ")

    if user_input.lower() == "exit":
        break

    corrected = autocorrect_sentence(user_input)
    print("Autocorrected:", corrected)
    print("Next word suggestion:", predict_next_word(corrected))

