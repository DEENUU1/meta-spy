from typing import Optional
from ..database import get_session
from ..models import InstagramAccount


def account_exists(username: str) -> bool:
    session = get_session()
    account = session.query(InstagramAccount).filter_by(username=username).first()
    return account is not None


def get_account(username: str) -> Optional[InstagramAccount]:
    session = get_session()
    return session.query(InstagramAccount).filter_by(username=username).first()


def create_account(username: str) -> Optional[InstagramAccount]:
    session = get_session()
    if not account_exists(username):
        account = InstagramAccount(username=username)
        session.add(account)
        session.commit()
        return account
    return None


def update_account(
    username: str,
    number_of_posts: int = None,
    number_of_followers: str = None,
    number_of_following: str = None,
) -> bool:
    session = get_session()
    account = session.query(InstagramAccount).filter_by(username=username).first()
    if account is None:
        return False

    if number_of_posts:
        account.number_of_posts = number_of_posts
    if number_of_followers:
        account.number_of_followers = number_of_followers
    if number_of_following:
        account.number_of_following = number_of_following

    session.commit()
    session.close()
    return True
