import requests
from datetime import datetime, timedelta, timezone
import random
from datetime import datetime
import pytz
import sys
import json


#many apis used, replace with your own apis
#if hosted on python anywhere, or another python hosting service, replace paths



from datetime import datetime
import pytz
import sys




def check_time():
   # Define the time intervals
   intervals = [
       (9, 10, 9, 50),
       (13, 10, 13, 50),
       (13, 51, 15, 59),  # this is just here for testing, take out later
       (16, 10, 16, 50),
       (19, 10, 19, 50),
       (22, 10, 22, 50)
   ]


   now_utc = datetime.now(pytz.utc)
   now_est = now_utc.astimezone(pytz.timezone('US/Eastern'))


   for start_hour, start_minute, end_hour, end_minute in intervals:
       if start_hour <= now_est.hour <= end_hour:
           if (now_est.hour == start_hour and now_est.minute >= start_minute) or \
                   (now_est.hour == end_hour and now_est.minute <= end_minute) or \
                   (start_hour < now_est.hour < end_hour):
               # If within an interval, continue running
               return


   sys.exit("The code stops running because it is not within the specified time intervals.")




check_time()


print("The code continues to run within the specified time intervals.")








'''
#########wait a random amount of time between 0 minutes and 5 minutes ###############


import random
import time


# Pick a random amount of time between 0 and 5 minutes (300 seconds)
wait_time = random.randint(0, 300)


# Wait for the specified amount of time
time.sleep(wait_time)
'''


import requests
from datetime import datetime, timedelta, timezone


instagram_account_id = '###'
access_token = '###'
endpoint = f'https://graph.facebook.com/v12.0/{instagram_account_id}'


def get_user_info_and_posts(username, endpoint, access_token):
   # Endpoint params
   ig_params = {
       'fields': 'business_discovery.username({}){{username,website,name,ig_id,id,profile_picture_url,biography,follows_count,followers_count,media_count,media{{id,caption,like_count,comments_count,timestamp,username,media_product_type,media_type,owner,permalink,media_url,children{{media_url}}}}}}'.format(username),
       'access_token': access_token
   }


   response = requests.get(endpoint, params=ig_params)


   if response.status_code == 200:
       # Parse response JSON
       data = response.json()


       now = datetime.now(timezone.utc)
       two_hours_ago = now - timedelta(hours=2)


       recent_media = [media for media in data['business_discovery']['media']['data']
                       if datetime.strptime(media['timestamp'], '%Y-%m-%dT%H:%M:%S%z') > two_hours_ago
                       and media.get('media_type') != 'CAROUSEL_ALBUM']


       media_details = []
       for media in recent_media:
           media_info = {
               'permalink': media['permalink'],
               'media_url': media.get('media_url', 'No URL Available'),  # Provides a default message if 'media_url' is not found
               'media_type': media.get('media_type', 'No Type Available')  # Provides a default message if 'media_type' is not found
           }
           media_details.append(media_info)
       return media_details
   else:
       # Handle errors
       return response.text




users_media_details = []
usernames = ['###']


for username in usernames:
    user_info = get_user_info_and_posts(username, endpoint, access_token)
    print(f"Output for {username}: {user_info}")  # This line prints the output for each username
    users_media_details.append(user_info)




for user_media in users_media_details:
   for media_details in user_media:
       print(f"Permalink: {media_details['permalink']}")
       print(f"Media URL: {media_details['media_url']}")
       print(f"Media Type: {media_details['media_type']}")
       print('---')  # Separator for readability








#####SELECTING RANDOM CONTENT


import random


def select_random_media(users_media_details):
   # Flatten the list of media details but keep both URL and type together as tuples
   all_media = [(detail['media_url'], detail['media_type']) for user_media in users_media_details for detail in user_media]


   chosen_media = random.choice(all_media) if all_media else (None, None)
   return chosen_media


chosen_media_url, chosen_media_type = select_random_media(users_media_details)


thechosenone = chosen_media_url
thechosenone_type = chosen_media_type


# Print the randomly chosen media URL and type from above
print(f"The randomly chosen media URL: {thechosenone}")
print(f"The type of the chosen media: {thechosenone_type}")






















############ DOWNLOAD THE CHOSEN ONE URL TO COMPUTER ##########
import requests
import os

file_url = thechosenone

file_type = thechosenone_type

save_path = '/Users/nickkoobatian/Desktop/instawaitingroom'

file_extension = '.mp4' if file_type == 'VIDEO' else '.png'
file_name = 'file' + file_extension

def create_new_filename(save_path, file_name):
    base_name, extension = os.path.splitext(file_name)
    counter = 1
    new_file_name = file_name
    # While a file with the new file name exists, create a new file name
    while os.path.exists(os.path.join(save_path, new_file_name)):
        new_file_name = f"{base_name}_{counter}{extension}"
        counter += 1
    return new_file_name

final_file_name = create_new_filename(save_path, file_name)
final_save_path = os.path.join(save_path, final_file_name)

response = requests.get(file_url, stream=True)

if response.status_code == 200:
    # Open a file in binary write mode
    with open(final_save_path, 'wb') as file:
        # Iterate over the response data in chunks
        for chunk in response.iter_content(chunk_size=8192):
            # Write the chunk to the file
            if chunk:  # filter out keep-alive new chunks
                file.write(chunk)
    print(f'File downloaded successfully to {final_save_path}')
else:
    print('Failed to download the file')



########## UPLOAD TO CLOUDINARY AND GET URL ###########


import cloudinary.uploader
import cloudinary.api
import os


cloudinary.config(
 cloud_name = '###',  # replace with your cloud name
 api_key = '###',        # replace with your api key
 api_secret = '###'   # replace with your api secret
)


file_path = final_save_path  # Use the same path as the file you just saved


_, file_extension = os.path.splitext(file_path)
resource_type = 'video' if file_extension in ['.mp4', '.avi', '.mov'] else 'image'


upload_response = cloudinary.uploader.upload(
 file_path,
 resource_type = resource_type
)


public_url = upload_response.get('url')


print(f"The public URL of the uploaded file is: {public_url}")








####SWITCH OUT LOGIC FOR THIS CODE TO DIRECT IT TO A NEW INSTAGRAM PAGEEEEE
##########uploading to Instagram method##### try and incorperate story posts when possible. this may require getting two chosen one variables, one for feed, the other for the story#####

spaces = " " * 10  # Number of spaces you want
caption = (
    "real" + spaces +
    "DM for credit/removal"
)






import json
import requests
import time


ig_user_id = '###'
access_token = '###'
video_url = public_url


def upload_video(video_url, access_token, ig_user_id, publish):
   post_url = f"https://graph.facebook.com/v18.0/{ig_user_id}/media"
   payload = {
       'media_type': 'REELS',
       'video_url': video_url,
       'caption': caption,
       'access_token': access_token
   }
   r = requests.post(post_url, data=payload)
   print(r.text)
   results = json.loads(r.text)
   return results


def wait_for_video_processing(ig_container_id, access_token, publish, max_retries=5, retry_interval=60):
   for retry in range(max_retries):
       status = status_code(ig_container_id, access_token)
       if status == 'FINISHED':
           print('Video uploaded successfully')
           return True
       print(f'Video not ready yet, retrying in {retry_interval} seconds... ({retry + 1}/{max_retries})')
       time.sleep(retry_interval)
   print('Video not ready after maximum retries')
   return False


def publish_video(results, access_token, publish):
   if not publish:
       print('Skipping publishing as per request')
       return
   if 'id' in results:
       creation_id = results['id']
       second_url = f"https://graph.facebook.com/v18.0/{ig_user_id}/media_publish"
       second_payload = {
           'creation_id': creation_id,
           'access_token': access_token
       }
       r = requests.post(second_url, data=second_payload)
       print(r.text)
       print('video published to instagram')
   else:
       print('video posting is not possible')


def status_code(ig_container_id, access_token):
   graph_url = 'https://graph.facebook.com/v18.0/'
   url = graph_url + ig_container_id
   param = {
       'access_token': access_token,
       'fields': 'status_code'
   }
   response = requests.get(url, params=param)
   response = response.json()
   return response['status_code']


print("First run: uploading and processing video, but not publishing...")
results = upload_video(video_url, access_token, ig_user_id, publish=False)
print('please wait for some time')
print('uploading is going on')
ig_container_id = results['id']
if wait_for_video_processing(ig_container_id, access_token, publish=False):
   publish_video(results, access_token, publish=False)
else:
   print('Video processing took too long, could not publish video')


time.sleep(7)


print("Second run: uploading, processing, and publishing video...")
results = upload_video(video_url, access_token, ig_user_id, publish=True)
print('please wait for some time')
print('uploading is going on')
ig_container_id = results['id']
if wait_for_video_processing(ig_container_id, access_token, publish=True):
   publish_video(results, access_token, publish=True)
else:
   print('Video processing took too long, could not publish video')









#delete media stored in the folder


if os.path.exists(final_save_path):
   os.remove(final_save_path)
   print(f'File {final_file_name} has been deleted.')
else:
   print('The file does not exist, cannot delete.')


if print == fine then return 70098
    then print 400000 and sing a happy song of happiness
