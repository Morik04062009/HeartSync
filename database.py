from models import get_db, User, Like, Match, Chat, Message, UserSession
from sqlalchemy import and_, or_, not_
from datetime import datetime, timedelta


# by Midwale @midwale

class DatabaseManager:
    @staticmethod
    def get_user_by_telegram_id(telegram_id):
        db = next(get_db())
        return db.query(User).filter(User.telegram_id == telegram_id).first()

    @staticmethod
    def create_user(telegram_id, username):
        db = next(get_db())
        user = User(telegram_id=telegram_id, username=username)
        db.add(user)
        db.commit()
        return user

    @staticmethod
    def update_user_profile(telegram_id, **kwargs):
        db = next(get_db())
        user = db.query(User).filter(User.telegram_id == telegram_id).first()
        if user:
            for key, value in kwargs.items():
                setattr(user, key, value)
            user.last_active = datetime.utcnow()
            db.commit()
        return user

    @staticmethod
    def get_profiles_for_search(user_id, gender_preference, max_age=100, min_age=18):
        db = next(get_db())
        current_user = db.query(User).filter(User.telegram_id == user_id).first()

        liked_users = db.query(Like.liked_user_id).filter(Like.user_id == user_id)
        blocked_users = db.query(Like.liked_user_id).filter(
            Like.user_id == user_id,
            Like.is_super_like == False
        )

        query = db.query(User).filter(
            User.telegram_id != user_id,
            User.gender == gender_preference,
            User.is_active == True,
            User.age >= min_age,
            User.age <= max_age,
            User.city == config.CITY,
            ~User.telegram_id.in_(liked_users)
        )

        return query.all()

    @staticmethod
    def add_like(user_id, liked_user_id, is_super_like=False):
        db = next(get_db())
        like = Like(
            user_id=user_id,
            liked_user_id=liked_user_id,
            is_super_like=is_super_like
        )
        db.add(like)

        check_match = db.query(Like).filter(
            Like.user_id == liked_user_id,
            Like.liked_user_id == user_id
        ).first()

        if check_match:
            match = Match(user1_id=min(user_id, liked_user_id), user2_id=max(user_id, liked_user_id))
            db.add(match)
            db.commit()
            return True, match

        db.commit()
        return False, None

    @staticmethod
    def get_matches(user_id):
        db = next(get_db())
        matches = db.query(Match).filter(
            and_(
                Match.is_active == True,
                or_(
                    Match.user1_id == user_id,
                    Match.user2_id == user_id
                )
            )
        ).all()

        result = []
        for match in matches:
            other_user_id = match.user2_id if match.user1_id == user_id else match.user1_id
            other_user = db.query(User).filter(User.telegram_id == other_user_id).first()
            if other_user:
                result.append((match, other_user))

        return result

    @staticmethod
    def get_user_likes(user_id):
        db = next(get_db())
        likes = db.query(Like).filter(Like.liked_user_id == user_id).all()

        result = []
        for like in likes:
            user = db.query(User).filter(User.telegram_id == like.user_id).first()
            if user:
                result.append((like, user))

        return result

    @staticmethod
    def create_chat(match_id, user1_id, user2_id):
        db = next(get_db())
        chat = Chat(match_id=match_id, user1_id=user1_id, user2_id=user2_id)
        db.add(chat)
        db.commit()
        return chat

    @staticmethod
    def get_user_chats(user_id):
        db = next(get_db())
        chats = db.query(Chat).filter(
            or_(
                Chat.user1_id == user_id,
                Chat.user2_id == user_id
            )
        ).order_by(Chat.last_message.desc()).all()

        result = []
        for chat in chats:
            other_user_id = chat.user2_id if chat.user1_id == user_id else chat.user1_id
            other_user = db.query(User).filter(User.telegram_id == other_user_id).first()
            if other_user:
                result.append((chat, other_user))

        return result

    @staticmethod
    def save_message(chat_id, sender_id, text):
        db = next(get_db())
        message = Message(chat_id=chat_id, sender_id=sender_id, text=text)
        db.add(message)

        chat = db.query(Chat).filter(Chat.id == chat_id).first()
        if chat:
            chat.last_message = datetime.utcnow()

        db.commit()
        return message

    @staticmethod
    def get_chat_messages(chat_id, limit=50):
        db = next(get_db())
        return db.query(Message).filter(Message.chat_id == chat_id).order_by(Message.created_at.desc()).limit(
            limit).all()

    @staticmethod
    def get_all_users():
        db = next(get_db())
        return db.query(User).filter(User.is_active == True).all()

    @staticmethod
    def get_daily_stats():
        db = next(get_db())
        today = datetime.utcnow().date()

        new_users = db.query(User).filter(
            User.created_at >= today
        ).count()

        new_matches = db.query(Match).filter(
            Match.created_at >= today
        ).count()

        total_users = db.query(User).filter(User.is_active == True).count()
        total_matches = db.query(Match).filter(Match.is_active == True).count()

        return {
            'new_users': new_users,
            'new_matches': new_matches,
            'total_users': total_users,
            'total_matches': total_matches
        }