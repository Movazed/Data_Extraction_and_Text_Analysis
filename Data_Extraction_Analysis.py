import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
nltk.download('punkt')
nltk.download('stopwords')
import re

# Read the URL file into a pandas DataFrame
df = pd.read_excel('Input.xlsx')

# Ensure the output directory exists
output_dir = "D:/Projects/workspace/Black Coffer/TitleText"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Loop through each row in the df
for index, row in df.iterrows():
    url = row['URL']
    url_id = int(re.search(r'\d+', row['URL_ID']).group())  # Extract numeric part from 'URL_ID'

    # Make a request to the URL
    header = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"}
    try:
        response = requests.get(url, headers=header)
    except:
        print(f"Can't get response for {url_id}")
        continue

    # Create a BeautifulSoup object
    try:
        soup = BeautifulSoup(response.content, 'html.parser')
    except:
        print(f"Can't get page for {url_id}")
        continue

    # Find title
    try:
        title = soup.find('h1').get_text()
    except:
        print(f"Can't get title for {url_id}")
        continue

    # Find text
    article = ""
    try:
        for p in soup.find_all('p'):
            article += p.get_text()
    except:
        print(f"Can't get text for {url_id}")
        continue

    # Write title and text to the file
    file_name = os.path.join(output_dir, f"blackassign{url_id:04d}.txt")
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(title + '\n' + article)

# Directories
text_dir = "D:/Projects/workspace/Black Coffer/TitleText"
stopwords_dir = "D:/Projects/workspace/Black Coffer/StopWords"
sentiment_dir = "D:/Projects/workspace/Black Coffer/MasterDictionary"

# Load all stop words from the stopwords directory and store them in a set
stop_words = set()
for files in os.listdir(stopwords_dir):
    with open(os.path.join(stopwords_dir, files), 'r', encoding='ISO-8859-1') as f:
        stop_words.update(set(f.read().splitlines()))

# Load all text files from the directory and store them in a list (docs)
docs = []
for text_file in os.listdir(text_dir):
    with open(os.path.join(text_dir, text_file), 'r', encoding='utf-8') as f:
        text = f.read()
        # Tokenize the given text file
        words = word_tokenize(text)
        # Remove the stop words from the tokens
        filtered_text = [word for word in words if word.lower() not in stop_words]
        # Add each filtered token of each file into a list
        docs.append(filtered_text)

# Store positive and negative words from the directory
pos = set()
neg = set()

for files in os.listdir(sentiment_dir):
    if files == 'positive-words.txt':
        with open(os.path.join(sentiment_dir, files), 'r', encoding='ISO-8859-1') as f:
            pos.update(f.read().splitlines())
    else:
        with open(os.path.join(sentiment_dir, files), 'r', encoding='ISO-8859-1') as f:
            neg.update(f.read().splitlines())

# Collect the positive and negative words from each file
# Calculate the scores from the positive and negative words
positive_words = []
negative_words = []
positive_score = []
negative_score = []
polarity_score = []
subjectivity_score = []

# Iterate through the list of docs
for doc in docs:
    positive_words.append([word for word in doc if word.lower() in pos])
    negative_words.append([word for word in doc if word.lower() in neg])
    positive_score.append(len(positive_words[-1]))
    negative_score.append(len(negative_words[-1]))
    polarity_score.append((positive_score[-1] - negative_score[-1]) / ((positive_score[-1] + negative_score[-1]) + 0.000001))
    subjectivity_score.append((positive_score[-1] + negative_score[-1]) / (len(doc) + 0.000001))

# Average Sentence Length = the number of words / the number of sentences
# Percentage of Complex words = the number of complex words / the number of words
# Fog Index = 0.4 * (Average Sentence Length + Percentage of Complex words)

avg_sentence_length = []
percentage_of_complex_words = []
fog_index = []
complex_word_count = []
avg_syllable_word_count = []

def measure(file):
    with open(os.path.join(text_dir, file), 'r', encoding='utf-8') as f:
        text = f.read()
        # Remove punctuations
        text = re.sub(r'[^\w\s.]', '', text)
        # Split the given text file into sentences
        sentences = text.split('.')
        # Total number of sentences in a file
        num_sentences = len(sentences)
        # Total words in the file
        words = [word for word in text.split() if word.lower() not in stopwords.words('english')]
        num_words = len(words)

        # Complex words having syllable count greater than 2
        # Complex words are words in the text that contain more than two syllables.
        complex_words = []
        for word in words:
            vowels = 'aeiou'
            syllable_count_word = sum(1 for letter in word if letter.lower() in vowels)
            if syllable_count_word > 2:
                complex_words.append(word)

        # Syllable Count Per Word
        # We count the number of Syllables in each word of the text by counting the vowels present in each word.
        # We also handle some exceptions like words ending with "es","ed" by not counting them as a syllable.
        syllable_count = 0
        syllable_words = []
        for word in words:
            if word.endswith('es'):
                word = word[:-2]
            elif word.endswith('ed'):
                word = word[:-2]
            syllable_count_word = sum(1 for letter in word if letter.lower() in vowels)
            if syllable_count_word >= 1:
                syllable_words.append(word)
                syllable_count += syllable_count_word

        avg_sentence_len = num_words / num_sentences
        avg_syllable_word_count = syllable_count / len(syllable_words)
        percent_complex_words = len(complex_words) / num_words
        fog_index = 0.4 * (avg_sentence_len + percent_complex_words)

        return avg_sentence_len, percent_complex_words, fog_index, len(complex_words), avg_syllable_word_count

# Iterate through each file or doc
for file in os.listdir(text_dir):
    x, y, z, a, b = measure(file)
    avg_sentence_length.append(x)
    percentage_of_complex_words.append(y)
    fog_index.append(z)
    complex_word_count.append(a)
    avg_syllable_word_count.append(b)

# Word Count and Average Word Length Sum of the total number of characters in each word/Total number of words
# We count the total cleaned words present in the text by
# removing the stop words (using stopwords class of nltk package).
# removing any punctuations like ? ! , . from the word before counting.

def cleaned_words(file):
    with open(os.path.join(text_dir, file), 'r', encoding='utf-8') as f:
        text = f.read()
        text = re.sub(r'[^\w\s]', '', text)
        words = [word for word in text.split() if word.lower() not in stopwords.words('english')]
        length = sum(len(word) for word in words)
        average_word_length = length / len(words)
    return len(words), average_word_length

word_count = []
average_word_length = []
for file in os.listdir(text_dir):
    x, y = cleaned_words(file)
    word_count.append(x)
    average_word_length.append(y)

# To calculate Personal Pronouns mentioned in the text, we use regex to find
# the counts of the words - “I,” “we,” “my,” “ours,” and “us”. Special care is taken
# so that the country name US is not included in the list.
def count_personal_pronouns(file):
    with open(os.path.join(text_dir, file), 'r', encoding='utf-8') as f:
        text = f.read()
        personal_pronouns = ["I", "we", "my", "ours", "us"]
        count = 0
        for pronoun in personal_pronouns:
            count += len(re.findall(r"\b" + pronoun + r"\b", text))  # \b is used to match word boundaries
    return count

pp_count = []
for file in os.listdir(text_dir):
    pp_count.append(count_personal_pronouns(file))

# Now create the output DataFrame
output_df = pd.DataFrame()
output_df['URL_ID'] = [int(re.search(r'\d+', file).group()) for file in os.listdir(text_dir)]

variables = [
    positive_score, negative_score, polarity_score, subjectivity_score,
    avg_sentence_length, percentage_of_complex_words, fog_index,
    complex_word_count, avg_syllable_word_count, word_count,
    average_word_length, pp_count
]

columns = [
    "Positive Score", "Negative Score", "Polarity Score", "Subjectivity Score",
    "Average Sentence Length", "Percentage of Complex Words", "Fog Index",
    "Complex Word Count", "Average Syllable Count", "Word Count",
    "Average Word Length", "Personal Pronoun Count"
]

# Debug: Print lengths to ensure they match
print("Length of output_df:", len(output_df))
for i, var in enumerate(variables):
    print(f"Length of {columns[i]}: {len(var)}")

# Assign variables to the DataFrame
for i, var in enumerate(variables):
    if len(var) == len(output_df):
        output_df[columns[i]] = var
    else:
        print(f"Length mismatch for {columns[i]}")

# Save the DataFrame to an Excel file
output_df.to_excel('Output Data Structure.xlsx', index=False) #no index present or didnt entered it for less consumptions of data5
output_df.to_csv('Output.csv')


