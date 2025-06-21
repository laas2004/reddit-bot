import praw
import config 
import time 
import os
   
def bot_login():
    print("logging in ...")
    r = praw.Reddit(username = config.username,
            password = config.password,
             client_id = config.client_id,
              client_secret = config.client_secret,
               user_agent = "dogs_comment_check bot v1.0 by /u/lazyveg1" )
    print("logged in")

    return r

def run_bot(r, comments_replied_to):      #We will define parameters here, which is r
    print("fetching 10 comments...")

    for comment in r.subreddit('test').comments(limit=10):
        print(f"\nchecking comment ID: {comment.id}")
        print(f"author: {comment.author}")
        print(f"subreddit: {comment.subreddit.display_name}")
        print(f"body: {comment.body[:50]}")  # Prints first 50 chars only

        if "dogs" in comment.body.lower() and comment.id not in comments_replied_to and not comment.author != r.user.me():
            print(f"Keyword 'dogs' found in comment {comment.id}!")

            try:
                comment.reply("I love dogs! [Here](https://i.redd.it/sxotuk5ikn3f1.jpeg) is an image of one.")
                print(f"Replied to comment {comment.id}")
                comments_replied_to.append(comment.id)
            except Exception as e:
                print(f"Error replying to comment {comment.id}: {e}")
        else:
            print(f"No reply: already replied or keyword not found.")
            with open("comments_replied_to.txt", "a") as f:
                f.write(comment.id + "\n")

    print("Sleeping for 10 seconds...\n")
    time.sleep(10)    #Sleeps/pauses for 10 seconds. After pause, it restarts the process of logging in and running run_bot(r)

def get_saved_comments():    #This is a function with no parameters to retrieve previously replied comment IDs
    if not os.path.isfile("comments_replied_to.txt"):
        comments_replied_to= []
    else:
        with open("comments_replied_to.txt","r") as f:    # Opens the file in read mode as 'f'
            comments_replied_to = f.read()     # Reads the entire file content into a string
        comments_replied_to = comments_replied_to.split("\n")   # Splits the string into a list using newline as separator
        comments_replied_to = filter(None,comments_replied_to)   #It filters the 1st argument(None) from the second argument(comments_replied_to)
    return comments_replied_to
    
r = bot_login()    #We are calling the function "bot_login" here
comments_replied_to = get_saved_comments()
print(comments_replied_to)

while True:    #Using while loops makes it run forever rather than us doing it manually for each time
    run_bot(r, comments_replied_to)   #We are calling the function "run_bot" here

