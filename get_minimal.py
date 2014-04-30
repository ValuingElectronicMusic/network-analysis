import add_data as ad
import get_soundcloud_data as gsd

def user_dicts(resource):
    return {u.obj['id']:u.obj for u in resource.data}

def starting_user(user_id):
    return gsd.client.get('/users/' + str(user_id)).obj

def from_user(user_id):
    user_id=str(user_id)
    follows = user_dicts(gsd.client.get('/users/'+ user_id +'/followings'))
    followed_by = user_dicts(gsd.client.get('/users/'+ user_id +'/followers'))
    x_follows_y={}
    for y in follows:
        x_follows_y.add((user_id,y))
    for x in followed_by:
        x_follows_y.add((x,user_id))
    follows.update(followed_by)
    return x_follows_y,follows

def from_users(user_list,x_follows_y,users):
    for user in user_list:
        xfy,us = from_user(user)
        x_follows_y.update(xfy)
        users.update(us)
    return x_follows_y, users

def test(start_at):
    user_data={start_at:starting_user(start_at)}
    folls_collected={[]}
    x_follows_y=set([])
    for i in range(2):
        to_collect = [u for u in user_data if u not in folls_collected]
        
        
