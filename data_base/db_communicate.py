import os

from sqlalchemy import create_engine, Column, String, Integer, and_, ForeignKey, Boolean, Index, not_, union_all, select
from sqlalchemy.orm import sessionmaker, declarative_base

db_path = os.path.join(os.path.dirname(__file__), 'anketa_user.db')
print(db_path)
db = create_engine(f'sqlite:///{db_path}', echo=True)

Session = sessionmaker(bind=db)
session = Session()
DataBase = declarative_base()

class Anketa(DataBase):
    __tablename__ = "anketa"
    id = Column(Integer, primary_key=True, index=True)
    id_telegramm = Column(Integer, index=True)
    name = Column(String)
    age = Column(Integer)
    sex = Column(String)
    search = Column(String)
    search_age_start = Column(Integer)
    search_age_finish = Column(Integer)
    about_me = Column(String)
    photo = Column(String)

    def __repr__(self):
        return (f"<Anketa(id_telegramm='{self.id_telegramm}', name='{self.name}', age='{self.age}', sex='{self.sex}',"
                f" search='{self.search}',search_age_start='{self.search_age_start}', search_age_finish='{
                self.search_age_finish}', about_me='{self.about_me}', photo='{self.photo}')>")

    # def __str__(self):
    #     return (f"Имя:{self.name}\n"
    #             f"Возраст:{self.age}\n"
    #             f"Информация:{self.about_me}\n"
    #             f"Фото:{self.photo}\n")


class LikeAnkets(DataBase):
    __tablename__ = "like"
    id = Column(Integer, primary_key=True, index=True)
    from_telegram_id = Column(Integer, ForeignKey("anketa.id_telegramm"),index=True)
    to_telegram_id = Column(Integer, ForeignKey("anketa.id_telegramm"),index=True)
    is_match = Column(Boolean, default=False)
    def __repr__(self):
        return (f"<LikeAnkets(from_telegram_id='{self.from_telegram_id}', to_telegram_id='{self.to_telegram_id}', is_match = '{self.is_match}')>")

class DislikeAnkets(DataBase):
    __tablename__ = "deslike"
    id = Column(Integer, primary_key=True, index=True)
    from_telegram_id = Column(Integer, ForeignKey("anketa.id_telegramm"),index=True)
    to_telegram_id = Column(Integer, ForeignKey("anketa.id_telegramm"),index=True)
    def __repr__(self):
        return (f"<DislikeAnkets(from_telegram_id='{self.from_telegram_id}', to_telegram_id='{self.to_telegram_id}')>")

Index("id_like_user",LikeAnkets.from_telegram_id, LikeAnkets.to_telegram_id)
Index("deslike_user",DislikeAnkets.from_telegram_id, DislikeAnkets.to_telegram_id)
DataBase.metadata.create_all(db)


async def create_profile(id_telegramm, name, age, sex, search, search_age_start, search_age_finish, about_me, photo):
    anketa = Anketa(id_telegramm=id_telegramm, name=name, age=age, sex=sex, search=search,
                    search_age_start=search_age_start, search_age_finish=search_age_finish,
                    about_me=about_me, photo=photo)
    session.add(anketa)
    session.commit()


async def get_needed_profile(start_search, finish_search, sex_search, user_id):
    subquery_likes = session.query(LikeAnkets.to_telegram_id).filter(LikeAnkets.from_telegram_id == user_id)
    subquery_dislikes = session.query(DislikeAnkets.to_telegram_id).filter(DislikeAnkets.from_telegram_id == user_id)

    all_needed_profiles = session.query(Anketa).filter(
        and_(
            Anketa.age >= start_search,
            Anketa.age <= finish_search,
            Anketa.sex == sex_search,
            not_(Anketa.id_telegramm.in_(subquery_likes)),
            not_(Anketa.id_telegramm.in_(subquery_dislikes)),
            Anketa.id_telegramm != user_id
        )
    ).first()

    return all_needed_profiles


async def get_curent_profile(id_telegram):
    user_profile = session.query(Anketa).filter(Anketa.id_telegramm == id_telegram).first()
    if user_profile:
        start_search = user_profile.search_age_start
        finish_search = user_profile.search_age_finish
        sex_search = user_profile.search
        get_needed_profile_result = await get_needed_profile(start_search, finish_search, sex_search, id_telegram)
        return get_needed_profile_result
    return None


async def send_like_ancet(from_telegram_id, to_telegram_id):
    proverka = session.query(LikeAnkets).filter (and_(LikeAnkets.from_telegram_id == to_telegram_id,
                                                      LikeAnkets.to_telegram_id == from_telegram_id)).first()
    print(proverka)
    if not proverka:
        like_to_like = LikeAnkets(from_telegram_id=from_telegram_id, to_telegram_id=to_telegram_id)
        session.add(like_to_like)
    else:
        proverka.is_match = True
        session.add(proverka)
        like_to_like = LikeAnkets(from_telegram_id=from_telegram_id, to_telegram_id=to_telegram_id, is_match=True)
        session.add(like_to_like)

    session.commit()

async def send_dislike_ancet(from_telegram_id, to_telegram_id):
    dis_like_ancet = DislikeAnkets(from_telegram_id=from_telegram_id, to_telegram_id=to_telegram_id)
    session.add(dis_like_ancet)
    session.commit()


async def acket_union_acket(from_telegram_id):
    match_user_id = session.query(LikeAnkets.to_telegram_id).filter(and_(
        LikeAnkets.is_match, LikeAnkets.from_telegram_id == from_telegram_id)).first()[0]
    print("match_user_id",match_user_id)
    get_ancet = session.query(Anketa).filter(Anketa.id_telegramm == match_user_id).first()
    return get_ancet












