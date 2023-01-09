from flask import abort

from .models import session, profile_schema
from .models import Profile
from .validation import Validation
from .wallet import Wallet
from .errors import *


# user's profile methods

class UserProfile():
    def __init__(self):
        self = self

    # cteate new user

    def create(self, user_information):
        name = user_information['name']
        tg_user_id = user_information['tg_user_id']
        # validation name and telegram ID format
        if Validation().name_validate(name) == None and\
            Validation().tg_user_id_validate(tg_user_id) == None:
            # create new user profile
            new_profile = Profile(name, tg_user_id)
            session.add(new_profile)
            session.commit()
            # crediting of welcome benefit 10000 USDT
            Wallet().hello_user_balance(tg_user_id)
            profile = (profile_schema.dump(session.query(Profile)
                        .filter_by(tg_user_id = str(tg_user_id)).one()))
        return profile

    # get user information: (name, tg_user_id)

    def get_information(self, tg_user_id):
        user_info = (session.query(Profile).filter_by(tg_user_id = tg_user_id)
                    .first())
        if not user_info:
            abort(404, description = "user not found")
        user_info_result = profile_schema.dump(user_info)
        return user_info_result

    # update username
    
    def update(self, user_information, tg_user_id):
        user_info = (session.query(Profile)
                    .filter_by(tg_user_id = str(tg_user_id)).first())
        if not user_info:
            abort(404, description = "user not found")
        new_name = user_information['name']
        # validation of availability a new name 
        if Validation().name_validate(new_name) == None:
            profile_name = (session.query(Profile)
                            .filter_by(tg_user_id = tg_user_id).first())
            profile_name.name = new_name
            session.add(profile_name)
            session.commit()
            user_with_new_name = (profile_schema.dump(session.query(Profile)
                                .filter_by(tg_user_id = tg_user_id).one()))
        return user_with_new_name

    # delete user
    
    def delete(self, tg_user_id):
        user_info = (session.query(Profile).filter_by(tg_user_id = tg_user_id)
                    .first())
        if not user_info:
            abort(404, description = "user not found")
        session.delete(user_info)
        session.commit()
        return None