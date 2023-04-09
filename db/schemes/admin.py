def admin_schema(admin:dict)->dict:
    return{
        'id':str(admin['_id']),
        'username':admin['username'],
        'fullname':admin['fullname'],
        'age':admin['age'],
        'email':admin['email'],
        'disable':admin['disable']
    }
    

def admin_db_schema(admin_db:dict)->dict:
    return{
        'id':str(admin_db['_id']),
        'username':admin_db['username'],
        'fullname':admin_db['fullname'],
        'age':admin_db['age'],
        'email':admin_db['email'],
        'disable':admin_db['disable'],
        'password':admin_db['password']
    }