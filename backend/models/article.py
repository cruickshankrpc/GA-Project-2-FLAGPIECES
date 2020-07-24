# comments
from app import db, ma
from models.base import BaseModel, BaseSchema
from marshmallow import fields
from models.user import User


articles_reactions = db.Table('articles_reactions', db.Column('reaction_id', db.Integer, db.ForeignKey(
                                  'reactions.id'), primary_key=True)
                              db.Column('article_id', db.Integer, db.ForeignKey(
                                  'articles.id'), primary_key=True)
                              )


class Article(db.Model, BaseModel):

    __tablename__ = 'articles'

    title = db.Column(db.String(80), nullable=False)
    # name is the news source (e.g. BBC News)
    name = db.Column(db.String(40), nullable=False)
    url = db.Column(db.String(40), nullable=False)
    urlToImage = db.Column(db.String(40), nullable=False)
    publishedAt = (db.Integer, nullable=False)
    content = db.Column(db.Text, nullable=False)
    reactions = db.relationship(
        'Reaction', secondary=articles_reactions, backref='articles')

    reader_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    reader = db.relationship('User', backref='reader_id')


class Comment(db.Model, BaseModel):

    __tablename__ = 'comments'

    content = db.Column(db.Text, nullable=False)

    article_id = db.Column(db.Integer, db.ForeignKey('articles.id'))
    article = db.relationship('Reaction', backref='comments')


class Flag(db.Model, BaseModel):

    __tablename__ = 'flags'

    flag_image = db.Column(db.String(25), nullable=False)

    map_id = db.Column(db.Integer, db.ForeignKey('map.id'))
    map = db.relationship('Map', backref='flag')



 class Map(db.Model, BaseModel):

    __tablename__ = 'maps'

   places = db.Column(db.String(80), nullable=False)
   longitude = db.Column(db.Integer, nullable=False )
   latitidue = db.Column(db.Integer, nullable=False )



class Reaction(db.Model, BaseModel):

    __tablename__ = 'reactions'

    reaction_name = db.Column(db.String(25), nullable=False)

    reaction_image = db.Column(db.String(25), nullable=False
    count = db.Column(db.Integer, nullable=False)


class ArticleSchema(ma.SQLAlchemyAutoSchema, BaseSchema):

    class Meta:
        model=Article
        load_instance=True

    comments=fields.Nested('CommentSchema', many=True)

    reactions=reactions.Nested('ReactionSchema', many=True)

    reader=fields.Nested('UserSchema', only=('id', 'username'))
    reader_id=fields.Integer()



class CommentSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model=Comment
        load_instance=True



class FlagSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model=Flag
        load_instance=True


class ReactionSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model=Reaction
        load_instance=True
