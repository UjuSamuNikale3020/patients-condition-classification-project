{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 43,
   "id": "e2487077",
   "metadata": {
    "ExecuteTime": {
     "end_time": "2023-04-15T09:53:15.538869Z",
     "start_time": "2023-04-15T09:53:05.887162Z"
    }
   },
   "outputs": [],
   "source": [
    "import streamlit as st\n",
    "import pandas as pd\n",
    "from sklearn.feature_extraction.text import TfidfVectorizer\n",
    "from sklearn.metrics.pairwise import cosine_similarity\n",
    "from nltk.corpus import stopwords\n",
    "from nltk.stem import WordNetLemmatizer\n",
    "from bs4 import BeautifulSoup\n",
    "import re\n",
    "import string\n",
    "\n",
    "# Load the dataset\n",
    "df = pd.read_csv('drugsCom_raw (1).csv', encoding='Latin-1')\n",
    "df = df.drop(['Unnamed: 0', 'date', 'usefulCount'], axis=1)\n",
    "df = df[(df['condition'] == 'Depression') | (df['condition'] == 'High Blood Pressure') | (df['condition'] == 'Diabetes, Type 2')]\n",
    "df.dropna(axis=0, inplace=True)\n",
    "\n",
    "# Define the conditions we want to focus on\n",
    "CONDITIONS = {\n",
    "    'Depression': ['Depression','antidepressant','mood swing'],\n",
    "    'High Blood Pressure': ['High Blood Pressure', 'blood pressure','hypertension'],\n",
    "    'Diabetes, Type 2': ['Diabetes, Type 2','diarrhea gas', 'diagnosed']\n",
    "}\n",
    "\n",
    "stop = set(stopwords.words('english'))\n",
    "lemmatizer = WordNetLemmatizer()\n",
    "\n",
    "def review_to_words(raw_review):\n",
    "    # Delete HTML tags\n",
    "    review_text = BeautifulSoup(raw_review, 'html.parser').get_text()\n",
    "\n",
    "    # Remove punctuation and convert to lowercase\n",
    "    review_text = review_text.translate(str.maketrans('', '', string.punctuation))\n",
    "    review_text = review_text.lower()\n",
    "\n",
    "    # Remove numbers and other non-letter characters\n",
    "    review_text = re.sub('[^a-zA-Z]', ' ', review_text)\n",
    "\n",
    "    # Remove stopwords and lemmatize words\n",
    "    words = review_text.split()\n",
    "    meaningful_words = [w for w in words if not w in stop]\n",
    "    lemmatized_words = [lemmatizer.lemmatize(w) for w in meaningful_words]\n",
    "\n",
    "    # Return the cleaned review text\n",
    "    return ' '.join(lemmatized_words)\n",
    "\n",
    "df['review_clean'] = df['review'].apply(review_to_words)\n",
    "\n",
    "def get_top_drugs(review_text, num=5):\n",
    "    # Preprocess the review\n",
    "    review_clean = review_to_words(review_text)\n",
    "\n",
    "    # Filter the dataset based on the condition of the input review\n",
    "    condition = None\n",
    "    for key, values in CONDITIONS.items():\n",
    "        for value in values:\n",
    "            if value.lower() in review_clean.lower():\n",
    "                condition = key\n",
    "                break\n",
    "        if condition:\n",
    "            break\n",
    "    if condition:\n",
    "        df_condition = df[df['condition'] == condition]\n",
    "    else:\n",
    "        return []\n",
    "\n",
    "    # Create a TF-IDF matrix for the reviews\n",
    "    tfidf_vectorizer = TfidfVectorizer(ngram_range=(1, 3), max_features=1000)\n",
    "    tfidf_matrix = tfidf_vectorizer.fit_transform(df_condition['review_clean'])\n",
    "\n",
    "    # Compute the cosine similarity matrix for the reviews\n",
    "    cosine_sim = cosine_similarity(tfidf_matrix.T, tfidf_matrix.T)\n",
    "\n",
    "    # Get the indices of the top recommended drugs\n",
    "    indices = pd.Series(df_condition.index)\n",
    "    indices_sorted = indices[cosine_sim[-1].argsort()[::-1]]\n",
    "    top_indices = indices_sorted[1:num+1]\n",
    "\n",
    "    # Get the top recommended drugs and their corresponding conditions\n",
    "    top_drugs = df_condition.loc[top_indices, ['drugName', 'condition']].values.tolist()\n",
    "\n",
    "    return top_drugs\n",
    "\n",
    "\n",
    "# Define the Streamlit app\n",
    "st.title('Drug Recommender')\n",
    "\n",
    "# Get the review text from the user\n",
    "review = st.text_input('Enter your review:')\n",
    "\n",
    "# Show the input review\n",
    "st.write('Input review:', review)\n",
    "\n",
    "# Show the recommended drugs\n",
    "if st.button('Get recommendations'):\n",
    "    try:\n",
    "        top_drugs = get_top_drugs(review)\n",
    "        if len(top_drugs) > 0:\n",
    "            st.write('Top recommended drugs:')\n",
    "            for drug, condition in top_drugs:\n",
    "                st.write(f'{drug} (for {condition})')\n",
    "        else:\n",
    "            st.write('No recommendations found for the input review.')\n",
    "    except Exception as e:\n",
    "        st.write('Error:', e)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 44,
   "id": "c5fb1934",
   "metadata": {
    "ExecuteTime": {
     "end_time": "2023-04-15T09:55:01.753172Z",
     "start_time": "2023-04-15T09:55:01.737514Z"
    }
   },
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "fb9509b1",
   "metadata": {
    "ExecuteTime": {
     "end_time": "2023-04-15T09:55:06.510781Z",
     "start_time": "2023-04-15T09:55:06.466586Z"
    }
   },
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "0fcd32bd",
   "metadata": {
    "ExecuteTime": {
     "end_time": "2023-04-15T09:50:21.118632Z",
     "start_time": "2023-04-15T09:50:21.092671Z"
    }
   },
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "c761417e",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.9.13"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
