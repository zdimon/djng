




@task 
def clear_offline():
    redis_client = redis.Redis(host='localhost', port=6379, db=0)
    data = {'task': 'gather_active_connections'}
    redis_client.publish('notifications', json.dumps(data))
    time.sleep(1)
    redis_client = redis.Redis(host='localhost', port=6379, db=4)
    redis_online = json.loads(redis_client.get('socket_connections'))
    #print(redis_online)

    
    # if user is online but has not socket
    sid_arr = []
    for redis_connection in redis_online:
        sid_arr.append(redis_connection['socket_id'])
    db_online = []
    for uo in UserOnline.objects.all():
        print(sid_arr)
        print(uo.sid)
        if uo.sid not in sid_arr:
            print('not %s' % uo.sid)
            uo =  UserOnline.objects.filter(token=redis_connection['token'])[0]
            pr = uo.user.userprofile
            pr.is_online = False
            pr.save()


    for redis_connection in redis_online:
        print(redis_connection)
        
        uo =  UserOnline.objects.filter(token=redis_connection['token'])[0]
        pr = uo.user.userprofile
        # if useronline exists and socket exists
        if UserOnline.objects.filter(token=redis_connection['token']).count()>0:
            pr.is_online = True
            pr.save()


        # if user is off but has a socket
        if pr.is_online == False:
            pr.is_online = True
            pr.save()       

        redis_client.publish('notifications',json.dumps({'task': 'user_offline'}))
    '''
    db_online = []
    for uo in UserOnline.objects.all():
        db_online.append({'sid': uo.sid, 'user': uo.user})

    for c in db_online:
        if c['sid'] not in redis_online:
            print('not online !!!! %s' % c)
            set_user_offline({'socket_id': c['sid'], 'user_id': uo.user.id})

    
    # if user is online but not connected by socket
    for pr in UserProfile.objects.filter(is_online=True):
        if UserOnline.objects.filter(user=pr).count()==0:
            pr.is_online = False
            pr.save()
            redis_client.publish('notifications',json.dumps({'task': 'user_offline'}))
    '''

@task
def ping_socket():
    redis_client = redis.Redis(host='localhost', port=6379, db=0)
    data = {'task': 'gather_active_connections'}
    redis_client.publish('notifications', json.dumps(data))
    '''
    time.sleep(2)
    sio = socketio.Client()

    @sio.event
    def connect():
        print("I'm connected!")
        sio.emit('ng-action',{'action': 'get_active_connections'})

    @sio.on('active-connections')
    def on_message(data):
        print('I received a message!')
        print(data)
        users_online = []
        for uo in UserOnline.objects.all():
            users_online.append(uo.sid)
        print(users_online)
        for c in users_online:
            if c not in data:
                print('not online !!!! %s' % c)
                set_user_offline({'socket_id': c})
        print("I'm disconnected!")
        sio.disconnect()


    @sio.event
    def disconnect():
        print("I'm disconnected!")

    sio.connect(SOCKET_SERVER,socketio_path="/websocket")
    '''