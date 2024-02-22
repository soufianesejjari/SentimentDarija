from flask import Flask, request, jsonify
from YouTubeCommentScraper import YouTubeCommentScraper
from DataAnalyste import DataAnalyste
import re
from flask_cors import CORS  # Importez l'extension CORS
from FaccebookScraper import  FacebookScraper
from urllib.parse import unquote

app = Flask(__name__)
CORS(app)  # Activez CORS pour l'ensemble de l'application

# Créez une instance de la classe d'analyse des sentiments
sentiment_analysis = DataAnalyste()
youtube_scraper = YouTubeCommentScraper()
facebook_scraper = FacebookScraper()


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@app.route('/help', methods=['GET'])
def api_help():
    help_message = {
        "instructions": "Bienvenue dans l'API de Feedback Vidéo.",
        "endpoints": [
            {"endpoint": "/",
             "method": "GET",
             "description": "Renvoie une chaîne de caractères 'Hello World!'."},
            {"endpoint": "/analyse_feedback_video?videoLink=VOTRE_LIEN",
             "method": "GET",
             "description": "Analyse les commentaires associés à une vidéo YouTube ou à un post Facebook. Le paramètre 'videoLink' doit être fourni."},
            {"endpoint": "/help",
             "method": "GET",
             "description": "Fournit des instructions sur l'utilisation de l'API."}
        ]
    }
    return jsonify(help_message)
@app.route('/analyse_feedback_video', methods=['GET'])
def analyse_feedback_video():
    try:
        # Obtenez le lien de la vidéo depuis la requête GET
        # Obtenez le lien de la vidéo depuis la requête GET
        video_link_encoded = request.args.get('videoLink')

        # Décodez l'URL (supporte les caractères arabes)
        video_link = unquote(video_link_encoded)        # video_url = 'https://www.youtube.com/watch?v=Nlw6a-qhKEI&list=RDe-OkWMuETvs&index=26&ab_channel=DizzyDROS'  # Remplacez par l'URL de la vidéo que vous souhaitez
        # video_comments_df = youtube_scraper.get_comments_df_for_video(video_url)
        if "facebook" in video_link.lower():
            comments_df = facebook_scraper.getPostData(video_link)
            cleaned_comments = sentiment_analysis.clean_facebook_comments(comments_df)
        elif("youtube" in video_link.lower()):
            comments_df = youtube_scraper.get_comments_df_for_video(video_link)
            cleaned_comments = sentiment_analysis.clean_youtube_comments(comments_df)
        elif "topic" in video_link.lower():
            # Supprime le mot "topic" depuis le lien
            video_link = video_link.replace("topic", "")
            comments_df = youtube_scraper.get_comments_df_for_topic(video_link)
            cleaned_comments = sentiment_analysis.clean_youtube_comments(comments_df)
        else:
            return jsonify({'error': 'Lien non pris en charge ou format incorrect.'}), 400
            # df=clean_youtube_comments(video_comments_df)
        # Analysez les commentaires de la vidéo

        # Nettoyez les commentaires

        # Prédisez les sentiments
        predictions = sentiment_analysis.analyze_sentiment(cleaned_comments['Comment'])

        # Générez le rapport
        report = sentiment_analysis.generate_report(cleaned_comments, predictions)

        return jsonify(report)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run()
