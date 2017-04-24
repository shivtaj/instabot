import requests
App_Access_Token = "5001103105.1131889.4f8108b23b4347cb9c037627968c36e9"
BASE_URL = "https://api.instagram.com/v1/"
data = requests.get("https://api.github.com/events")

# this function is used for owner info


def info_owner():
    owner_url = BASE_URL + "users/self/?access_token=" + App_Access_Token   #https://api.instagram.com/v1/users/self/?access_token=ACCESS-TOKEN
    owner_info = requests.get(owner_url).json()                             #Get information about the owner of the access_token
    #print owner_info
    print ("_____________owner_info______________")
    print("Name                    : ", owner_info['data']['full_name'])
    print("Username                : ", owner_info['data']['username'])
    print("Link to Profile Picture : ", owner_info['data']['profile_picture'])
    print("Media Shared            : ", owner_info['data']['counts']['media'])
    print("Followed By             : ", owner_info['data']['counts']['followed_by'])
    print("Followers               : ", owner_info['data']['counts']['follows'])
    if owner_info['data']['website'] != '':
        print("Website                 : ", owner_info['data']['website'])
    else:
        print("Website                 :  No Website Available")
    if owner_info['data']['bio'] != '':
        print("Bio                     : ", owner_info['data']['bio'])
    else:
        print("Bio                     :  No Info Available")


# https://api.instagram.com/v1/users/{user-id}/?access_token=ACCESS-TOKEN
# this function is used get the info of user

def user_by_username(insta_user):
    url = BASE_URL + 'users/search?q=' + insta_user + "&access_token="+App_Access_Token
    my_info = requests.get(url).json()
    print my_info
    return my_info['data'][0]['id']

# https://api.instagram.com/v1/users/self/media/recent/?access_token=ACCESS-TOKEN
# this function is used  to get the post of user


def get_user_post(insta_username):
    user_id = user_by_username(insta_username)
    request_url = BASE_URL + 'users/'+user_id + '/media/recent/?access_token='+App_Access_Token
# print request_url
    recent_posts = requests.get(request_url).json()
    success = recent_posts['meta']['code']
    if len(recent_posts['data']) == 0:
        print ("\n no post found for this user!")
    else:
        for post_no in range(0, len(recent_posts['data']), 1):
            post_no
        post_found = str(post_no)
        print('total' + post_found + 'post_of' + insta_username + '\n choose post of  ur choice')
        post_no = raw_input()
        a = int(post_no)
        if success == 200:
            print"user_post is successfully fetched"
        else:
            print"not done plz chk user id"
        return recent_posts["data"][a]["id"]


# https://api.instagram.com/v1/users/self/media/liked?access_token=ACCESS-TOKEN
# this function is used for like on user post
def like_post(insta_username):
    user_post_id = get_user_post(insta_username)
    payload = {"access_token": App_Access_Token}
    request_url = BASE_URL + "media/" + user_post_id + "/likes"
    response_to_like = requests.post(request_url, payload).json()
    success = response_to_like["meta"]["code"]
    if success == 200:
        print"post like successfully"  # make successfull like on user_post
        return
    else:
        print"post not liked plz try again"
        return
# print response_to_like['meta']['code']
# this  function is used for comment on user post


def post_new_comment(insta_username):
    user_media_id = get_user_post(insta_username)
    print "u can write the comment but the following steps should be followed \nNOTE:\n 1.don,t exceed the character to 200 \n 2.can not use tags more then 3 \n 3.comment can not contain all capital letters"
    print " write your comment here:"
    b = str(raw_input())
    request_url = BASE_URL + 'media/'+user_media_id+'/comments'
    request_data = {"access_token": App_Access_Token, 'text': b}
    comment = requests.post(request_url, request_data).json()
    success = comment["meta"]["code"]
    if success == 200:  # it checks the url
        print"comment is successfully done"
        return
    else:
        print"comment not done plz try again"
        return

# this function is used for search comment on any  post of user


def search_comment(insta_username):
    user_post_id = get_user_post(insta_username)
    # print "content related to comment"
    comment_for_search = BASE_URL + "media/" + str(user_post_id) + "/comments?access_token=" + App_Access_Token
    response = requests.get(comment_for_search).json()
    word = raw_input("enter the word u want to search")
    comments = []
    comments_id = []
    for i in response['data']:
        comments.append(i['text'])
        comments_id.append(i['id'])
    comments_found = []
    comments_id_found = []
    for a in range(len(comments)):
        if word in comments[a]:
            comments_found.append(comments[a])
            comments_id_found.append(comments_id[a])
            print"comment found"
    if len(comments_found) == 0:
        print " no comment is found in post "
        again_search = raw_input("enter 'y' or 'Y' for another  word  to search")
        if again_search == 'y'or again_search == 'Y':
            search_comment(insta_username)
        else:
            return 0, user_post_id
    else:
        return comments_id_found, user_post_id

# this function is used to delete the comment from post


def delete_comment(insta_username):
    comments_id_found, user_post_id = search_comment(insta_username)
    print user_post_id
    if comments_id_found != 0:
        for j in range(len(comments_id_found)):
            request_url = BASE_URL + "media/" + str(user_post_id) + "/comments/" + str(comments_id_found[j]) + "?access_token=" + App_Access_Token
            success = requests.delete(request_url).json()
            print success
            if success['meta']['code'] == 200:
                print"comment is successfully deleted from post"
            else:
                print"deletion is not done"
    else:
        print"comment can't be deleted"

# this function is used  to get the average of user's post


def average_post(insta_username):
    no_of_words = 0
    list_of_comments = []
    user_id = user_by_username(insta_username)
    post_id = get_user_post(insta_username)
    url = BASE_URL+"media/"+str(post_id)+"/comments/?access_token="+App_Access_Token
    fetch_info = requests.get(url).json()  # get call to fetch all comments
    if len(fetch_info['data']) == 0:    # if there is no comment done by you on post
        print("there is no comment on this post")
        return
    else:
        for comment in fetch_info['data']:
            list_of_comments.append(comment['text'])  # makes a list of comments
            no_of_words += len(comment['text'].split())  # or calculating the words in comment
        average_words = float(no_of_words)/len(list_of_comments)  # used to calculate the average
        print("average of post = %.2f" % average_words)
        return
print("\n hello user! welcome to instabot")
info_owner()
Input = raw_input("enter 'y' or 'Y'for the user post")
while Input == 'y'or Input == 'Y':
    print("choose the username from following \n 1.manpreet287 \n 2.bajwa_jugnu \n ")
    insta_username = raw_input()
    if insta_username not in ['manpreet287', 'bajwa_jugnu']:
        print "you choice is invalid plz enter a valid user"
    else:
        print"what u want to do with user id"
    enter_choice = raw_input("enter ur choice\n 1.for user_detail\n 2.for get_user_post\n 3.for like\n 4.for comment\n 5.for search comment\n 6.for delete comment \n 7.for average")
    if enter_choice == '1':
        user_by_username(insta_username)
    elif enter_choice == '2':
        get_user_post(insta_username)
    elif enter_choice == '3':
        like_post(insta_username)
    elif enter_choice == '4':
        post_new_comment(insta_username)
    elif enter_choice == '5':
        search_comment(insta_username)
    elif enter_choice == '6':
        delete_comment(insta_username)
    elif enter_choice == '7':
        average_post(insta_username)
    else:
        print"choice not correct plz enter from given option"
        enter_choice = raw_input("enter ur choice 1.for user_detail\n 2.for get_user_post\n 3.for like\n 4.for comment\n 5.for search comment\n 6.for delete comment \n 7.for average")
    print("\n press 'Y' or 'y' to continue or press any key to exit \n")
    Input = raw_input()
else:
    print (".....thnkuu for using instabot....")





