import requests     # importing for http request
import urllib       # importing for downloading images
from keys import ACCESS_TOKEN
from textblob import TextBlob   #TextBlob is imported as it provides api for NLP tasks
from textblob.sentiments import NaiveBayesAnalyzer  #sentiment analysis
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator

BASE_URL = 'https://api.instagram.com/v1/'

def self_info():    # getting self information
    request_url = (BASE_URL + 'users/self/?access_token=%s') %(ACCESS_TOKEN)
    print 'Requesting info for %s' %(request_url)
    my_info = requests.get(request_url)
    my_info = my_info.json()    # json object created

    if my_info['meta']['code'] == 200:      # checking whether request is ok
        if len(my_info['data']):
            print 'My info is:' + str(my_info)
            print 'Number of followers:%d' %(my_info['data']['counts']['followed_by'])
            print 'I follows %d number of people' %(my_info['data']['counts']['follows'])
        else:
            print 'There is no data for the user.'
    else:
        print 'code other than 200 received'

    return None


def get_user_id(insta_username):    # function to access id of a user
    request_url = (BASE_URL + 'users/search?q=%s&access_token=%s') %(insta_username, ACCESS_TOKEN)
    print 'getting request for:' + request_url
    search_result = requests.get(request_url)
    search_result = search_result.json()
    if search_result['meta']['code'] == 200:    # checking if request is ok
        if len(search_result['data']):
           user_id = search_result['data'][0]['id']
           print 'User id : ' + user_id
        else:
            print 'user does not exist'
    else:
        print 'Status code other tha 200 recieved'

    return user_id


def user_info(insta_username):  #getting info of a user by taking username as input
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User doesnot exist.'
        exit()
    request_url = (BASE_URL + 'users/%s/?access_token=%s') %(user_id, ACCESS_TOKEN)
    print 'requesting info for: '+ request_url
    user_inform = requests.get(request_url)
    user_inform = user_inform.json()    #json object created
    if user_inform['meta']['code'] == 200:
        if len(user_inform['data']):
            print user_inform
            print 'username:%s' %(user_inform['data']['username'])
            print 'no. of followers:%d' %(user_inform['data']['counts']['followed_by'])
            print 'no.of people %s followed:%d' %(insta_username,user_inform['data']['counts']['follows'])
        else:
            print 'There is no user data'
    else:
            print 'Status code other than 200 received'


def get_self_recent_post(insta_username): #getting self recent post and download it, return post id
    request_url = (BASE_URL + 'users/self/media/recent?access_token=%s') %(ACCESS_TOKEN)
    print 'requesting recent post for: ' + request_url
    rec_post = requests.get(request_url)
    rec_post = rec_post.json()

    if rec_post['meta']['code'] == 200:
        if len(rec_post['data']):
            image_name = rec_post['data'][0]['id'] + 'jpg'
            image_url = rec_post['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)   #downloading image
            print 'Post successfully downloaded.'
            return rec_post['data'][0]['id']            #returning post id
        else:
            print 'There is no recent post..'
    else:
        print 'Code other than 200 received.'

    return None


def get_user_recent_post(insta_username):   #getting recent post by taking username as input
    User_ID = get_user_id(insta_username)
    if User_ID == None:
        print 'user do not exists.'
    else:
        print 'User exists'

    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') %(User_ID, ACCESS_TOKEN)
    print 'Requesting post info for: ' + request_url

    user_rec_post = requests.get(request_url).json()

    if user_rec_post['meta']['code'] == 200:
        if len(user_rec_post['data']):
            image_name = user_rec_post['data'][0]['id'] + 'jpeg'
            image_url = user_rec_post['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)       #downloading image
            print 'Post successfully downloaded.'
            return user_rec_post['data'][0]['id']

        else:
            print 'No recent post.'
    else:
        print 'Code other than 200 exists.'

    return None


def self_media_liked(insta_username):   #getting recent post liked by user
    request_url = (BASE_URL + 'users/self/media/liked?access_token=%s') %(ACCESS_TOKEN)
    print 'getting media liked for : ' + request_url

    med_liked = requests.get(request_url).json()

    if med_liked['meta']['code'] == 200:
        if len(med_liked['data']):
            img_url = med_liked['data'][0]['images']['standard_resolution']['url']
            img_name = med_liked['data'][0]['id'] + 'jpeg'
            urllib.urlretrieve(img_url, img_name)
            print 'Image downloaded which is recently liked by user.'
        else:
            print 'No image liked by user'
    else:
        print 'Code other than 200 received.'

    return None


def get_post_id(insta_username):    #getting a post id,username as input
    User_ID = get_user_id(insta_username)   #getting user id
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') %(User_ID, ACCESS_TOKEN)
    print 'getting post id for : ' + request_url

    post_id = requests.get(request_url).json()

    if post_id['meta']['code'] == 200:
        if len(post_id['data']):
            return post_id['data'][0]['id']
        else:
            print 'No such post exists.'
    else:
        print 'code other than 200 received.'

    return None


def like_a_post(insta_username):  #like a post
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/likes') %(media_id)
    payload = {'access_token': ACCESS_TOKEN}
    print 'Liking post for:' + request_url
    post_a_like = requests.post(request_url, payload).json()    # post request to like the post
    if post_a_like['meta']['code'] == 200:
         print 'You successfully liked the post.'
    else:
        print 'your like was unsuccessful..Please try again.'
        exit()


def list_of_likes(insta_username):  # get list of likes on the recent post
    user_id = get_user_id(insta_username)   # get user id to access media id
    media_id = get_post_id(insta_username)  # get recent media id
    request_url = (BASE_URL + 'media/%s/likes?access_token=%s') %(media_id, ACCESS_TOKEN)
    print 'Getting info for: ' + request_url

    list_likes = requests.get(request_url).json()   # json object created

    if list_likes['meta']['code'] == 200:
        if len(list_likes['data']):
            for x in range(0, len(list_likes['data'])):
                print list_likes['data'][0]['username']     # print names of users who had liked the recent post
        else:
            print 'No one has liked this post.'
    else:
        print 'Code other than 200 received.'


def remove_like(insta_username):    # remove like from recent post
    user_id = get_user_id(insta_username)   # get user id to access media id
    media_id = get_post_id(insta_username)  # get recent media id
    request_url = (BASE_URL + 'media/%s/likes?access_token=%s') %(media_id, ACCESS_TOKEN)
    print 'Getting info for: ' + request_url

    rem_like = requests.delete(request_url).json()

    if rem_like['meta']['code'] == 200:
        print 'Like successfully removed from the post.'
    else:
        print 'Unable to remove like from the post.Try again !!'


def search_tagname():   # search post by their tag name
    tag_name = raw_input('Write the tag name for which you want to search.')
    request_url = (BASE_URL + 'tags/search?q=%s&access_token=%s') %(tag_name, ACCESS_TOKEN)
    print 'Getting info for: ' + request_url

    tag_search = requests.get(request_url).json()

    if tag_search['meta']['code'] == 200:
        if len(tag_search['data']):
            for x in range(0, len(tag_search['data'])):
                print 'Name: ' + str(tag_search['data'][x]['name'].encode('utf-8'))
                print 'Media-count: ' + str(tag_search['data'][x]['media_count'])
    return None


def recent_tag():   # search recent post by tag name
    tag_name = raw_input('Write tag name for which you want to search: ')
    request_url = (BASE_URL + 'tags/%s/media/recent?access_token=%s') %(tag_name, ACCESS_TOKEN)
    print 'Getting info for: ' + request_url

    rec_tag_search = requests.get(request_url).json()

    if rec_tag_search['meta']['code'] == 200:
        if len(rec_tag_search['data']):
            print 'Number of likes: ' + str(rec_tag_search['data'][0]['likes']['count'])
            text = rec_tag_search['data'][0]['caption']['text']
            print 'Text: ' + str(text)
            return text
        else:
            print 'No data exists for this tag.'
    else:
        print 'Code other than 200 received.'


def post_a_comment(insta_username):   # posting comment
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/comments') %(media_id)
    comment = raw_input('Write your comment:')
    payload = {'access_token':ACCESS_TOKEN, 'text':comment}
    print 'posting comment for:' + request_url
    post_comment = requests.post(request_url,payload).json()

    if post_comment['meta']['code'] == 200:
        print 'comment successfully posted.'
    else:
        print 'your comment does not posted successfully...Please try again.'
        exit()


def list_of_comment(insta_username):    #getting list of comment on a post
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/comments?access_token=%s') %(media_id, ACCESS_TOKEN)
    print 'Requesting list of comments for:' + request_url
    list_comments = requests.get(request_url).json()

    if list_comments['meta']['code'] == 200:
        if len(list_comments['data']):
            for x in range(0, len(list_comments['data'])):
                a = list_comments['data'][x]['text']
                print a.encode("utf-8")

        else:
            print 'No comments exists.'
    else:
        print 'Code other than 200 received.'


def word_cloud():   # function to create word cloud for the description of a tag
    text = recent_tag() # get the tag description whose word cloud is to made
    if len(text):
        path = raw_input('Write the path of image : ')
        # write the path of any image which is in your computer.
        # for example: path = 'C:\\Users\\Lenovo\Desktop\\emoji.png'
        # this image is used and word cloud is made in the shape of this image

        # read the mask / color image taken from
        coloring = np.array(Image.open(path))

        wc = WordCloud(background_color="white", max_words=2000, mask=coloring,
                    max_font_size=40, random_state=42)

        # generate word cloud
        wc.generate(text)

        # create coloring from image
        image_colors = ImageColorGenerator(coloring)

        # show
        plt.imshow(wc, interpolation="bilinear")
        plt.axis("off")
        plt.figure()

        # recolor wordcloud and show
        plt.imshow(wc.recolor(color_func=image_colors), interpolation="bilinear")
        plt.axis("off")
        plt.figure()

        plt.imshow(coloring, cmap=plt.cm.gray, interpolation="bilinear")
        plt.axis("off")
        plt.show()

    else:
        print 'No description is there for the tag.'
        print 'Hence no word cloud generated.'


def del_negative_comment(insta_username):   #delete negative comments using NaiveBayesAnalyzer
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/comments/?access_token=%s') % (media_id, ACCESS_TOKEN)
    print 'GET request url : ' + request_url
    comment_info = requests.get(request_url).json()

    if comment_info['meta']['code'] == 200:
        if len(comment_info['data']):
            # naive implementation to delete negative comments
            for x in range(0, len(comment_info['data'])):
                comment_id = comment_info['data'][x]['id']
                comment_text = comment_info['data'][x]['text']
                blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())
                if (blob.sentiment.p_neg > blob.sentiment.p_pos):
                    print 'Negative comment : %s' % (comment_text)
                    delete_url = (BASE_URL + 'media/%s/comments/%s/?access_token=%s') % (media_id, comment_id, ACCESS_TOKEN)
                    print 'DELETE request url : %s' % (delete_url)
                    delete_info = requests.delete(delete_url).json()

                    if delete_info['meta']['code'] == 200:
                        print 'Comment successfully deleted!\n'
                    else:
                        print 'Unable to delete comment!'
                else:
                    print 'Positive comment : %s\n' % (comment_text)
        else:
            print 'There are no existing comments on the post!'
    else:
        print 'Status code other than 200 received!'


def start_insta_bot():  #starting  our instabot

    select = 'y'

    while select == 'y':
        print 'Insta bot welcomes you.'
        print 'Lets get started....'
        print 'Following are the Menu Options for Insta Bot.'
        print '1.  Get your details.'
        print '2.  Get details of other users by username. '
        print '3.  Get userid.'
        print '4.  Get recent media liked by user.'
        print '5.  Get a post id.'
        print '6.  Get your recent post.'
        print '7.  Get the recent post of the user.'
        print '8.  Like the post.'
        print '9.  Get list of comments on a post.'
        print '10.  Make comments on a post.'
        print '11.  Get list of likes'
        print '12. Remove like from a post.'
        print '13. Search tag by tag name.'
        print '14. Search recent tag by tag name.'
        print '15. Get Word Cloud for the description of a tag.'
        print '16. Delete negative comments from instagram post.'
        print '17. Exit Insta_Bot.'

        choice = int(raw_input('Enter your choice:'))

        if choice != 13 and choice != 14 and choice != 15 and choice != 17:
            insta_username = raw_input('Enter the name of person whose details you want to see:')
        else:
            pass

        if choice == 1:
            self_info()
        elif choice == 2:
            user_info(insta_username)
        elif choice == 3:
            get_user_id(insta_username)
        elif choice == 4:
            self_media_liked(insta_username)
        elif choice == 5:
            get_post_id(insta_username)
        elif choice == 6:
            get_self_recent_post(insta_username)
        elif choice == 7:
            get_user_recent_post(insta_username)
        elif choice == 8:
            like_a_post(insta_username)
        elif choice == 9:
            list_of_comment(insta_username)
        elif choice == 10:
            post_a_comment(insta_username)
        elif choice == 11:
            list_of_likes(insta_username)
        elif choice == 12:
            remove_like(insta_username)
        elif choice == 13:
            search_tagname()
        elif choice == 14:
            recent_tag()
        elif choice == 15:
            word_cloud()
        elif choice == 16:
            del_negative_comment(insta_username)
        elif choice == 17:
            print 'You decided to close application.'
            exit()
        else:
            print 'You have chosen wrong option !!!'
            exit()
        select = raw_input('Do you want to continue(y/n)?')

start_insta_bot()



