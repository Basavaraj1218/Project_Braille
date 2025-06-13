
from flask import Flask, request, render_template_string


KEY_TO_DOT = {'D': '1', 'W': '2', 'Q': '3', 'K': '4', 'O': '5', 'P': '6'}


BRAILLE_MAP = {
    'a': ['D'],
    'b': ['D', 'W'],
    'c': ['D', 'Q'],
    'd': ['D', 'Q', 'K'],
    'e': ['D', 'K'],
    'f': ['D', 'W', 'Q'],
    'g': ['D', 'W', 'Q', 'K'],
    'h': ['D', 'W', 'K'],
    'i': ['W', 'Q'],
    'j': ['W', 'Q', 'K'],
    'k': ['D', 'O'],
    'l': ['D', 'W', 'O'],
    'm': ['D', 'Q', 'O'],
    'n': ['D', 'Q', 'K', 'O'],
    'o': ['D', 'K', 'O'],
    'p': ['D', 'W', 'Q', 'O'],
    'q': ['D', 'W', 'Q', 'K', 'O'],
    'r': ['D', 'W', 'K', 'O'],
    's': ['W', 'Q', 'O'],
    't': ['W', 'Q', 'K', 'O'],
    'u': ['D', 'O', 'P'],
    'v': ['D', 'W', 'O', 'P'],
    'w': ['W', 'Q', 'K', 'P'],
    'x': ['D', 'Q', 'O', 'P'],
    'y': ['D', 'Q', 'K', 'O', 'P'],
    'z': ['D', 'K', 'O', 'P'],
}


# dictionary
WORD_DICTIONARY = ["cat", "cab", "bat", "car", "bar", "dog", "rat"]

def normalize_cell(keys):
    return ''.join(sorted(keys.upper()))

def word_to_braille(word):
    try:
        return [''.join(sorted(BRAILLE_MAP[c])) for c in word]
    except KeyError:
        return []

def levenshtein(a, b):
    n, m = len(a), len(b)
    if n > m:
        a, b = b, a
        n, m = m, n
    current = list(range(n + 1))
    for i in range(1, m + 1):
        previous, current = current, [i] + [0] * n
        for j in range(1, n + 1):
            add, delete, change = previous[j] + 1, current[j - 1] + 1, previous[j - 1]
            if a[j - 1] != b[i - 1]:
                change += 1
            current[j] = min(add, delete, change)
    return current[n]

def suggest_word(input_seq):
    suggestions = []
    for word in WORD_DICTIONARY:
        word_seq = word_to_braille(word)
        if word_seq:
            dist = levenshtein(input_seq, word_seq)
            suggestions.append((word, dist))
    return sorted(suggestions, key=lambda x: x[1])[:3]


app = Flask(__name__)

HTML_TEMPLATE = """
<!doctype html>
<title>Braille Autocorrect System</title>
<h2>Braille Autocorrect System (QWERTY Input)</h2>
<form method=post>
  <label>Enter Braille Cells (e.g., DK W KO):</label><br>
  <input type=text name=input_seq size=50><br><br>
  <input type=submit value=Suggest>
</form>
{% if suggestions %}
  <h3>Suggestions:</h3>
  <ul>
  {% for word, score in suggestions %}
    <li>{{ word }} (score {{ score }})</li>
  {% endfor %}
  </ul>
{% endif %}
"""

@app.route('/', methods=['GET', 'POST'])
def home():
    suggestions = []
    if request.method == 'POST':
        raw_input = request.form['input_seq'].strip().split()
        input_seq = [normalize_cell(cell) for cell in raw_input]
        suggestions = suggest_word(input_seq)
    return render_template_string(HTML_TEMPLATE, suggestions=suggestions)

if __name__ == '__main__':
    app.run(debug=True)
