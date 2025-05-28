from NLP_class import Article


def main():
    #  Dictionary of article URLs and News Sources
    urls_by_article = {
        "AP News Tufts Article":
            "https://apnews.com/article/rumeysa-ozturk-deportation-tufts-7459607d8585cf0a624fb943a4738be3",
        "CNN Tufts Article":
            "https://www.cnn.com/2025/03/27/us/rumeysa-ozturk-detained-what-we-know/index.html",
        "Fox News Tufts Article":
            "https://www.foxnews.com/us/federal-judge-rules-trump-administration-cannot-immediately-deport-tufts-student",
        "Al Jazeera Tufts Article":
            "https://www.aljazeera.com/news/2025/3/29/tufts-university-student-cant-be-deported-to-turkiye-without-court-order",
        "Fox News Venezuelan Deportation Article":
            "https://www.foxnews.com/politics/justice-department-invoke-state-secrets-act-high-profile-deportation-case",
        "AP News Venezuelan Deportation Article":
            "https://apnews.com/article/el-salvador-trump-tren-de-aragua-venezuela-dde4259e5dcd502101b7b8fbd3c03659",
        "CNN Venezuelan Deportation Article":
            "https://www.cnn.com/2025/03/24/americas/venezuela-us-deportees-flight-latam-intl-hnk/index.html",
        "Al Jazeera Venezuelan Deportation Article":
            "https://www.aljazeera.com/news/2025/3/24/venezuela-resumes-accepting-people-deported-from-us"
    }

    # initialize list of article instances.
    articles = []

    # iterate through each key in the documents and call on the Article class to create an instance of each article.
    for media_source, url in urls_by_article.items():
        article = Article(source=url, media_source=media_source)
        article.load_text()

        # add this instance to the intialized list.
        articles.append(article)

        # print some basic information to make sure the articles are loading in correctly.
        print(f"Source: {article.media_source}")
        print(f"URL: {article.source}")
        print(f"Content: {article.cleaned_content[:500]}...")  # Print first 500 characters
        print("-" * 80)

    # After all articles are loaded, generate the Sankey
    Article.multi_article_sankey(articles, k=15)

    # Plot the distributions in subjectivity.
    Article.plot_subjectivity_distribution(None, articles)

    # plot the co-occurrence network.
    Article.plot_cooccurrence_network(None, articles)

if __name__ == '__main__':
    main()