from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd
from bidi.algorithm import get_display
import arabic_reshaper
import re
from LaodedModel import loaded_model
import base64
from io import BytesIO


class DataAnalyste:
    def __init__(self, ):
        self.api_key = 'AIzaSyAcq7ba-UVWTTVI3z3jkP7EU8ZaGb-e5rU'

    def analyze_sentiment(self, sentences):
        # Utilisez le modèle chargé pour faire des prédictions
        predictions = loaded_model.predict(sentences)
        return predictions

    def clean_youtube_comments(self, df):
        cleaned_comments = []
        arabic_letters_pattern = re.compile('[\u0600-\u06FF\s]+')  # Expression régulière pour les lettres en arabe
        french_letters_pattern = re.compile('[a-zA-Z]+')  # Expression régulière pour les lettres en français

        cleaned_data = {'Comment': [], 'Date': []}

        for index, row in df.iterrows():
            # Supprimer les hashtags et ne garder que les lettres en arabe
            comment_text = re.sub(r'#\w+', '', row['Comment'])
            arabic_text = ''.join(arabic_letters_pattern.findall(comment_text))

            # Ajouter le commentaire nettoyé uniquement s'il contient des lettres en arabe et n'est pas vide
            if arabic_text and len(arabic_text.strip()) > 0:
                # Supprimer les commentaires avec plus de 10 lettres en français
                french_text = ''.join(french_letters_pattern.findall(comment_text))
                if len(french_text) <= 10:
                    cleaned_data['Comment'].append(arabic_text)
                    cleaned_data['Date'].append(row['Comment Date'])

        cleaned_df = pd.DataFrame(cleaned_data)
        return cleaned_df

    def clean_facebook_comments(self,df):
        cleaned_data = {'Comment': [], 'Date': []}
        arabic_letters_pattern = re.compile('[\u0600-\u06FF\s]+')  # Expression régulière pour les lettres en arabe
        french_letters_pattern = re.compile('[a-zA-Z]+')  # Expression régulière pour les lettres en français

        for index, row in df.iterrows():
            # Ajouter le commentaire nettoyé uniquement s'il contient des lettres en arabe et n'est pas vide
            comment_text = row['comment_text']
            arabic_text = ''.join(arabic_letters_pattern.findall(comment_text))

            if arabic_text and len(arabic_text.strip()) > 0:
                # Supprimer les commentaires avec plus de 10 lettres en français
                french_text = ''.join(french_letters_pattern.findall(comment_text))
                if len(french_text) <= 10:
                    cleaned_data['Comment'].append(arabic_text)
                    cleaned_data['Date'].append(row['comment_time'])

        cleaned_df = pd.DataFrame(cleaned_data)
        return cleaned_df

    def generate_report(self, comments_df, predictions):
        # Ajoutez les prédictions au DataFrame des commentaires
        comments_df['Sentiment'] = predictions

        # Calculez le taux de feedback global
        global_sentiment_rate = comments_df['Sentiment'].mean()

        # Calculez le taux de feedback par jour
        comments_df['Date'] = comments_df['Date'].astype(str)
        daily_sentiment_rate = comments_df.groupby('Date')['Sentiment'].mean().to_dict()

        # Générez le nuage de mots pour le sentiment positif
        positive_comments = comments_df[comments_df['Sentiment'] == 1]['Comment']
        positive_wordcloud = self.generate_wordcloud(positive_comments)

        # Générez le nuage de mots pour le sentiment négatif
        negative_comments = comments_df[comments_df['Sentiment'] == 0]['Comment']
        negative_wordcloud = self.generate_wordcloud(negative_comments)

        report = {
            'global_sentiment_rate': global_sentiment_rate,
            'daily_sentiment_rate': daily_sentiment_rate,
            'positive_wordcloud': positive_wordcloud,
            'negative_wordcloud': negative_wordcloud
        }

        return report

    def generate_wordcloud(self, comments):
        # Combinez tous les commentaires en une seule chaîne de caractères
        all_comments = ' '.join(comments)

        # Appliquez la fonction reshape_arabic_text pour réorganiser les caractères arabes
        reshaped_comments = self.reshape_arabic_text(all_comments)

        # Créez un objet WordCloud
        wordcloud = WordCloud(
            font_path='notonaskharabic-regular.ttf',
            background_color='white',
            width=800,
            height=400
        ).generate(reshaped_comments)

        # Convertissez l'image en base64
        img_buf = BytesIO()
        wordcloud.to_image().save(img_buf, format='PNG')
        img_str = base64.b64encode(img_buf.getvalue()).decode('utf-8')

        return img_str

    def reshape_arabic_text(self, text):
        # Utilisez arabic_reshaper pour réorganiser correctement les caractères arabes
        reshaped_text = arabic_reshaper.reshape(text)
        # Utilisez get_display pour gérer correctement les caractères de droite à gauche
        bidi_text = get_display(reshaped_text)
        return bidi_text
