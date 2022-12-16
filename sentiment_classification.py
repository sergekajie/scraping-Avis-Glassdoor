"""
Sentiment analysis of general appreciation using transformers.
You can also use textblob
"""

from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import pipeline

loaded_model = AutoModelForSequenceClassification.from_pretrained("nlptown/flaubert_small_cased_sentiment")
tokenizer = AutoTokenizer.from_pretrained("flaubert/flaubert_small_cased")
nlp = pipeline("sentiment-analysis", model=loaded_model, tokenizer=tokenizer)




def get_sentiment(appreciation):
    results = nlp(appreciation
                  .replace("Plutôt bon cabinet", "bon cabinet")
                  .replace("Pas mal", "bon")
                  .replace("Une expérience traumatisante", "mauvaise expérience")
                  )
    return results[0].get('label')


# import textblob
# from textblob_fr import PatternTagger, PatternAnalyzer

# def appreciation_processing_with_textblob(df_reviews):
#     """

#     :param df_reviews:
#     :return:
#     """
#     def get_popularity(text):
#         return textblob.TextBlob(text=text, pos_tagger=PatternTagger(), analyzer=PatternAnalyzer()).sentiment[0]

#     def get_subjectivity(text):
#         return textblob.TextBlob(text=text, pos_tagger=PatternTagger(), analyzer=PatternAnalyzer()).sentiment[1]

#     df_reviews["sentiment_polarity"] = df_reviews["appreciation_generale"].apply(get_popularity)
#     df_reviews["sentiment_subjectivity"] = df_reviews["appreciation_generale"].apply(get_subjectivity)

#     # manual correction
#     positive_words = ["good", "proximité", "épanouir", "bien", "format", "positif", "motivant", "top", "dynamique"]
#     df_reviews.loc[df_reviews.sentiment_polarity==0, "positif"] = df_reviews.appreciation_generale.apply(lambda text: any([word in text.lower() for word in positive_words]))

#     df_reviews["sentiment_class"] = df_reviews["sentiment_polarity"].apply(lambda sent:
#                                                                              "positif"
#                                                                              if sent > 0
#                                                                              else ("négatif" if sent < 0 else "neutre")
#                                                                              )

#     return df_reviews

