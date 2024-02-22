import googleapiclient.discovery
import pandas as pd
import re
class YouTubeCommentScraper:
    def __init__(self, ):
        self.api_key = 'apiyoutube'
        self.youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey='apiyoutube')

    def get_video_info(self, video_id):
        request = self.youtube.videos().list(part='snippet', id=video_id)
        response = request.execute()

        if 'items' in response:
            video = response['items'][0]
            title = video['snippet']['title']
            description = video['snippet']['description']
            print(f'Title: {title}\nDescription: {description}')

    def get_comments_df_for_video(self, video_url,max_results=20):
        # Extraire l'ID de la vidéo à partir de l'URL
        video_id_match = re.search(r'(?:youtu\.be/|youtube\.com/watch\?v=|youtube\.com/embed/|youtube\.com/v/|youtube\.com/e/|youtube\.com/user/[^/]+/u/|v=)([^"&?/ ]{11})', video_url)
        if video_id_match:
            video_id = video_id_match.group(1)
        else:
            raise ValueError("L'URL de la vidéo YouTube est invalide.")

        comments_request = self.youtube.commentThreads().list(
                part='snippet,replies',
                videoId=video_id,
                textFormat='plainText',
                maxResults=max_results
            )
        comments_response = comments_request.execute()
        comments_info = []
        for item in comments_response['items']:
                snippet = item['snippet']['topLevelComment']['snippet']
                comments_info.append({
                    'Video Title': snippet.get('videoOwnerChannelInfo', {}).get('videoOwnerChannelTitle', ''),
                    'Comment Date': snippet.get('publishedAt', ''),
                    'Comment': snippet.get('textDisplay', ''),
                    'Likes': snippet.get('likeCount', 0),
                    'Dislikes': snippet.get('dislikeCount', 0)
                })

        return pd.DataFrame(comments_info)


    def get_comments_info_for_topic(self, topic, max_results=10):
        search_request = self.youtube.search().list(
            q=topic,
            part='id',
            type='video',
            maxResults=max_results
        )
        search_response = search_request.execute()

        video_ids = [item['id']['videoId'] for item in search_response['items']]

        comments_info = []
        for video_id in video_ids:
            comments_request = self.youtube.commentThreads().list(
                part='snippet,replies',
                videoId=video_id,
                textFormat='plainText',
                maxResults=max_results
            )
            comments_response = comments_request.execute()

            for item in comments_response['items']:
                snippet = item['snippet']['topLevelComment']['snippet']
                comments_info.append({
                    'Video Title': snippet.get('videoOwnerChannelInfo', {}).get('videoOwnerChannelTitle', ''),
                    'Comment Date': snippet.get('publishedAt', ''),
                    'Comment': snippet.get('textDisplay', ''),
                    'Likes': snippet.get('likeCount', 0),
                    'Dislikes': snippet.get('dislikeCount', 0)
                })

        return comments_info

    def get_comments_df_for_topic(self, topic, max_results=10):
        comments_info = self.get_comments_info_for_topic(topic, max_results)
        return pd.DataFrame(comments_info)


