from vaderSentiment_fr.vaderSentiment import SentimentIntensityAnalyzer

if __name__ == '__main__':
    analyzer = SentimentIntensityAnalyzer()
    phrase = "Une phrase très cool à analyser"

    score = analyzer.polarity_scores(phrase)
    print(score)
