import requests
App_Access_Token="5001103105.1131889.4f8108b23b4347cb9c037627968c36e9"
BASE_URL="https://api.instagram.com/v1/"
data=requests.get("https://api.github.com/events")
def info_owner():
    url_owner=BASE_URL+"users/self/?access_token="+App_Access_Token

    owner_info=requests.get(url_owner).json()
    print (owner_info)

    print(owner_info["data"]["full_name"])
    print(owner_info["data"]["bio"])
    print(owner_info["data"]["username"])

#info_owner()
# #https://api.instagram.com/v1/users/{user-id}/?access_token=ACCESS-TOKEN
def user_by_username(insta_user):
    url=BASE_URL + 'users/search?q=' + insta_user + "&access_token="+App_Access_Token
    my_info = requests.get(url).json()
   # print my_info
    return  my_info['data'][0]['id']

#user_by_username('manpreet287')
# #https://api.instagram.com/v1/users/self/media/recent/?access_token=ACCESS-TOKEN
def get_user_post(insta_username):
    user_id=user_by_username( insta_username)
    request_url = BASE_URL + 'users/'+user_id +'/media/recent/?access_token='+App_Access_Token
   # print request_url
    recent_posts=requests.get(request_url).json()
    print recent_posts['data'][0]['link']
    return recent_posts['data'][0]["id"]
#get_user_post('manpreet287')
# https://api.instagram.com/v1/users/self/media/liked?access_token=ACCESS-TOKEN
def like_post(insta_username):
    user_post_id=get_user_post(insta_username)
    payload ={"access_token": App_Access_Token}
    request_url= BASE_URL + "media/" + user_post_id + "/likes"
    response_to_like = requests.post(request_url, payload).json()
   # print response_to_like['meta']['code']
    print response_to_like
#like_post('manpreet287')
#https://api.instagram.com/v1/media/{media-id}/comments?access_token=ACCESS-TOKEN
def comment_on_user_id(insta_username):
    user_media_id=get_user_post(insta_username)
    request_url= (BASE_URL+ 'media/%s/comments?access_token%s') %(user_media_id,App_Access_Token)
    request_data={"access_token" : App_Access_Token,'text': "nice design"}
    comment_request = requests.post(request_url,request_data).json()
    print comment_request
comment_on_user_id('manpreet287')
