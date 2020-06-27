
# POSTGRESQL & MYSQL & MSSQL 
## insert  

    query = Model().insert('deneme', {0: {'username': 'user1', 'pass': 'pass1'},  
                                      1: {'username': 'user2', 'pass': 'pass2'},  
                                      2: {'username': 'user3', 'pass': 'pass3'},  
                                      3: {'username': 'user4', 'pass': 'pass4'},  
                                      4: {'username': 'user5', 'pass': 'pass5'}}).data()  
    print(query)  

## update  

    query = Model().update('deneme', {'SET': {'username': 'ali', 'pass': 'veli'},  
                                      'CONDITION': {0: {'col': 'username', 'operator': '=', 'value': 'user2',  
                                                        'combiner': 'AND', 'scope': 0},  
                                                    1: {'col': 'pass', 'operator': '=', 'value': 'pass2',  
                                                        'combiner': 'OR', 'scope': 1},  
                                                    2: {'col': 'username', 'operator': '=', 'value': '1',  
                                                        'combiner': 'AND', 'scope': 0},  
                                                    3: {'col': 'pass', 'operator': '=', 'value': '1',  
                                                        'scope': 1}}}).data()  
    print(query)  

## select  

    query = Model().select('deneme', 'username,pass',  
                           {0: {'col': 'username', 'operator': '=', 'value': 'ali', 'combiner': 'AND', 'scope': 0},  
                            1: {'col': 'pass', 'operator': '=', 'value': 'veli', 'combiner': 'OR', 'scope': 1},  
                            2: {'col': 'username', 'operator': '=', 'value': '1'}},  
                           'username desc'  
                           ).data()  
      print(query)  

## select pagination count

  
    query,count,total_page = Model().select('deneme', 'username,pass',  
                           {0: {'col': 'username', 'operator': '=', 'value': 'ali', 'combiner': 'AND', 'scope': 0},  
                            1: {'col': 'pass', 'operator': '=', 'value': 'veli', 'combiner': 'OR', 'scope': 1},  
                            2: {'col': 'username', 'operator': '=', 'value': '1'}},  
                           'username desc'  
                           ).pagination(
                            top=10, offset=0).count(10).data()


## delete  

    query = Model().delete('deneme',  
                           {0: {'col': 'username', 'operator': '=', 'value': 'user1', 'combiner': 'AND', 'scope': 0},  
                            1: {'col': 'pass', 'operator': '=', 'value': 'pass1', 'combiner': 'OR', 'scope': 1},  
                            2: {'col': 'username', 'operator': '=', 'value': '1'}}  
                           ).data()  
      print(query)  

  
# KAFKA  
## insert  

    query = Model('ReaKafka').insert('reactor', {0: {'key1': 'user1', 'key2': {  
        "system": {"rest_server": {"host": "127.0.0.1", "port": 443, "debug": False, "sort_json": False}}}}}).data()  
    print(query)

# REDIS  
## insert  

    query = LocalModel('ReaRedis').insert(1, {0: {'username': 'user1', 'pass': 'pass1'},
                                          1: {'username1': 'user2', 'pass1': 'pass2'},
                                          2: {'username2': 'user3', 'pass2': 'pass3'},
                                          3: {'username3': 'user4', 'pass3': 'pass4'},
                                          4: {'username4': 'user5', 'pass4': 'pass5'}}).data()
    print(query)
    
## delete

    query = LocalModel('ReaRedis').delete(1,
                                     {0: {'col': 'username', 'operator': '=', 'value': {'col': 'username', 'operator': '=', 'value': 'user1'}},
                                      1: {'col': 'username1', 'operator': '>', 'value': 19},
                                      2: {'col': 'username4', 'operator': 'LIKE', 'value': '5'}}
                                     ).data()
    print(query)
    
## select

    query = LocalModel('ReaRedis').select(1, None,
                           {0: {'col': '', 'operator': 'LIKE', 'value': '*ali*'},
                            1: {'col': '', 'operator': '>', 'value': 'veli'},
                            2: {'col': 'username', 'operator': '>', 'value': 1}},
                           None
                           ).data()

                           
 ## update                          
     query = LocalModel('ReaRedis').update(1, {'SET': {'ali'},
                                     'CONDITION': {0: {'col': 'username', 'operator': '=', 'value': 'ali'},
                                                   1: {'col': 'pass', 'operator': '=', 'value': 'pass2'}}}).data()
    print(query)
