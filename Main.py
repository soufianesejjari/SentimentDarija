from flask import Flask, request, jsonify
from YouTubeCommentScraper import YouTubeCommentScraper
from DataAnalyste import DataAnalyste
app = Flask(__name__)
import re

# Créez une instance de la classe d'analyse des sentiments
sentiment_analysis = DataAnalyste()
youtube_scraper = YouTubeCommentScraper()
@app.route('/analyse_feedback_video', methods=['POST'])
def analyse_feedback_video():
    try:
        # Obtenez le lien de la vidéo depuis la requête POST
        video_link = request.json['video_link']

        # video_url = 'https://www.youtube.com/watch?v=Nlw6a-qhKEI&list=RDe-OkWMuETvs&index=26&ab_channel=DizzyDROS'  # Remplacez par l'URL de la vidéo que vous souhaitez
        # video_comments_df = youtube_scraper.get_comments_df_for_video(video_url)

        # df=clean_youtube_comments(video_comments_df)
        # Analysez les commentaires de la vidéo
        comments_df = youtube_scraper.get_comments_df_for_video(video_link)

        # Nettoyez les commentaires
        cleaned_comments = sentiment_analysis.clean_youtube_comments(comments_df)

        # Prédisez les sentiments
        predictions = sentiment_analysis.analyze_sentiment(cleaned_comments['Comment'])

        # Générez le rapport
        report = sentiment_analysis.generate_report(cleaned_comments, predictions)

        return jsonify(report)

    except Exception as e:
        return jsonify({'error': str(e)}), 500
if __name__ == "__main__":
    app.run(debug=True)
