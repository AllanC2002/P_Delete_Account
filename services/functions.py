from models.models import User, Profile
from conections.mysql import conection_accounts, conection_userprofile

def delete_user(user_id: int):
    # BD Accounts
    session_accounts = conection_accounts()
    user = session_accounts.query(User).filter_by(Id_User=user_id, Status=1).first()

    if not user:
        session_accounts.close()
        return {"error": "User not found or already inactive"}, 404

    user.Status = 0
    session_accounts.commit()
    session_accounts.close()

    # BD Userprofile
    session_userprofile = conection_userprofile()
    profile = session_userprofile.query(Profile).filter_by(Id_User=user_id, Status_account=1).first()

    if profile:
        profile.Status_account = 0
        session_userprofile.commit()

    session_userprofile.close()

    return {"message": f"User {user_id} successfully deleted logically"}, 200
