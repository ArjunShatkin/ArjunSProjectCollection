import re
from collections import Counter
from nltk.corpus import stopwords
import requests
from bs4 import BeautifulSoup
import os
import plotly.graph_objects as go
from textblob import TextBlob
import seaborn as sns
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import networkx as nx
import matplotlib.pyplot as plt

class Article:
    def __init__(self, source, content=None, media_source=None):
        # initialize core attributes that you can reference in your class functions
        self.source = source
        self.content = content
        self.cleaned_content = None
        self.media_source = media_source
        self.stop_words = set()
        self.word_counts = {}

    def load_stop_words(self, stopfile=None):
        """Load stop words from a file or use NLTK's predefined stopwords."""

        # if the user enters a stopfile, read it and load the stop words into the stops_word class attribute.
        if stopfile is not None:
            # If a stopfile is provided, load stop words from the file
            try:
                with open(stopfile, 'r') as f:
                    file_stopwords = f.read().splitlines()
                    self.stop_words.update(file_stopwords)
            except Exception as e:
                print(f"Error reading stopfile: {e}")

        # if the user does not enter a file, use nltk's embedded stopwords list.
        else:
            self.stop_words = set(stopwords.words('english'))

        # Although "said" is not in most stopwords lists, I want it automatically removed because
        # it provides no meaning when analyzing news articles.
        self.stop_words.add("said")

    def is_local_file(self):
        '''
        verifies whether the file is a txt file or a web url. This is useful in the domain of news articles
        because I could be importing an article as either a url or txt.
        '''
        return os.path.isfile(self.source) and self.source.endswith('.txt')


    def clean_text(self):
        """Clean the text by removing punctuation, numbers, extra whitespace, and stopwords.
        The only punction I do not want removed is sentence ending punctuation. I will keep periods and
        question marks so that I can analyze sentence subjectivity in later stages of the project."""

        # if content exists, clean it accordingly.
        if self.content:
            text = self.content.lower()
            text = re.sub(r'\s+', ' ', text)  # Normalize whitespace
            text = re.sub(r'[0-9]+', '', text)  # Remove numbers
            text = re.sub(r'[^\w\s.!?]', '', text)  # Keep only sentence-ending punctuation

            words = [word for word in text.split() if word not in self.stop_words]

            self.cleaned_content = ' '.join(words)
            self.word_counts = dict(Counter(words))

        else:
            self.cleaned_content = ""
            self.word_counts = {}
            print(f"Warning: No content to clean for Source: {self.source}")

    def load_text(self, parser=None, label=None):
        """Load text content from a file or URL."""
        if not self.content:

            # check if the file is a local file
            if self.is_local_file():
                self.content = self.load_from_file()

            # if it is not a local file, it is most likely a url that needs be web scraped.
            else:
                self.content = self.scrape_article(parser)
        # use the stop words and clean text functions from above to fully clean the content.
        self.load_stop_words()
        self.clean_text()
        self.label = label

    def load_from_file(self):
        """Load text content from a local .txt file."""
        try:
            with open(self.source, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            print(f"Error reading file {self.source}: {e}")
            return ""

    def scrape_article(self, parser=None):
        """Fetch and parse the article content if it is a url file."""
        # get the article url and use beautiful soup to access the code.
        response = requests.get(self.source)
        soup = BeautifulSoup(response.text, parser or 'html.parser')

        # Extracting the main content by finding where the paragraphs are stored.
        paragraphs = soup.find_all('p')

        # join the paragraphs to get a full version of the text/article.
        text = ' '.join([p.get_text() for p in paragraphs])
        return text

    @classmethod
    def multi_article_sankey(self, articles, word_list=None, k=5):
        """
        Creates a Sankey diagram mapping media sources to the top k-words.
        Link thickness represents word frequency in each article.
        """
        # Build counters
        global_counter = Counter()
        article_word_counts = {}

        # iterate through a list of articles and use the cleaned_content to count the amount of each word.
        for article in articles:
            if not hasattr(article, 'word_counts') or not article.word_counts:
                print(f"Skipping {article.media_source} (missing word_counts)")
                continue

            word_counts = article.word_counts
            article_word_counts[article.media_source] = word_counts
            global_counter.update(word_counts)

        # Define word list if the user did not enter a list of word they want to focus on.
        if not word_list:
            word_list = [word for word, _ in global_counter.most_common(k)]

        # Create label list and map the labels.
        article_labels = list(article_word_counts.keys())
        labels = article_labels + word_list
        label_indices = {label: i for i, label in enumerate(labels)}

        # Initialize the Sankey links
        sources = []
        targets = []
        values = []

        # iterate through the articles and find the word counts of popular words.
        for article in article_labels:
            word_counts = article_word_counts[article]

            '''if a word from an article is in the pre-defined word list, add them to the initialized 
            sankey nodes
            '''
            for word in word_list:
                count = word_counts.get(word, 0)
                if count > 0:
                    sources.append(label_indices[article])
                    targets.append(label_indices[word])
                    values.append(count)

        # Plot Sankey
        fig = go.Figure(data=[go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=labels,
                color=["skyblue"] * len(article_labels) + ["lightgreen"] * len(word_list)
            ),
            link=dict(
                source=sources,
                target=targets,
                value=values
            )
        )])

        # title and plot the sankey diagram.
        fig.update_layout(title_text="Multi-Article Word Frequency Sankey", font_size=12)
        fig.show()

    def plot_subjectivity_distribution(self, articles):

        # Create a list of subjectivity scores for all articles
        all_subjectivity_scores = []
        article_labels = []

        # using textblob, iterate through each article and calculate the subjectivity of each sentence.
        for article in articles:
            blob = TextBlob(article.cleaned_content)
            sentences = blob.sentences
            subjectivity_scores = [sentence.sentiment.subjectivity for sentence in sentences]

            # add the list of subjectivity score the the initialize list for all articles.
            all_subjectivity_scores.append(subjectivity_scores)
            article_labels.append(article.media_source)

        # Plotting the violinplot
        plt.figure(figsize=(10, 6))
        sns.violinplot(data=all_subjectivity_scores, palette="Set2")

        # Customizing the plot
        plt.title('Subjectivity Score Distribution by Article Source')
        plt.xlabel('Media Source / Article')
        plt.ylabel('Subjectivity Score')

        # label the correct article to the correct violin plot.
        plt.xticks(ticks=range(len(article_labels)), labels=article_labels, rotation=45, ha='right')
        plt.tight_layout()
        plt.show()

        # I needed to use plt.close so that I could then view the network vis. I was run the code.
        plt.close()

    def plot_cooccurrence_network(self, articles, threshold=3, window_size=5):
        """
        Plots a co-occurrence network for words across multiple articles' cleaned content.
        Only the top 100 connections (based on co-occurrence frequency) are visualized.

        Parameters:
            articles (list): List of Article instances.
            threshold (int): The minimum co-occurrence count to consider an edge between 2 words.
            window_size (int): width of the spaces you want to find cooccurences in.

        Note: While I had the idea of creating a network visualization for these articles,
        I needed measurable help from NetworkX's documentation website and LLMs
        to help me implement this code, as this was the first time I have implemented a network visualization.
        """

        # Collect all words from all articles
        all_words = []
        for article in articles:
            all_words.extend(article.cleaned_content.split())

        word_pairs = []

        # Create pairs of words that co-occur within a window in all articles
        window_size = window_size

        for i in range(len(all_words) - window_size):
            window = all_words[i:i + window_size]

            # if word1 and 2 appear within a window and are not the same, add this to a list of word pairs.
            for word1 in window:
                for word2 in window:
                    if word1 != word2:
                        word_pairs.append(tuple(sorted([word1, word2])))

        # Use the counter function to count the frequency of each word pair (i.e. co-occurrence)
        pair_counts = Counter(word_pairs)

        # Filter out pairs with frequency below the threshold
        filtered_pairs = [pair for pair, count in pair_counts.items() if count >= threshold]

        # Get the top 100 most frequent pairs
        top_pairs = filtered_pairs[:100]

        # Create a graph
        G = nx.Graph()
        G.add_edges_from(top_pairs)
        plt.figure(figsize=(12, 12))

        # this line will adjust the distance between nodes.
        pos = nx.spring_layout(G, k=0.5)

        # Draw nodes, edges, and labels and add the desire formatting.
        nx.draw_networkx_nodes(G, pos, node_size=500, node_color="skyblue", alpha=0.7)
        nx.draw_networkx_edges(G, pos, width=2, alpha=0.6, edge_color="gray")
        nx.draw_networkx_labels(G, pos, font_size=8, font_family="sans-serif", font_weight="bold")

        # Add title
        plt.title(f"Co-occurrence Network (Top Word Pairs)", fontsize=16)

        # Display the plot
        plt.axis("off")
        plt.show()
