from com_dayoung_api.ext.db import db
# from com_dayoung_api.user.dto import UserDto
# from com_dayoung_api.movie.dto import MovieDto

class ReviewDto(db.Model):
    __tablename__ = "reviews"
    __table_args__ = {'mysql_collate':'utf8_general_ci'}
    
    id: int = db.Column(db.Integer, primary_key=True, index=True)
    title: str = db.Column(db.String(100))
    content: str = db.Column(db.String(500))
    
    userid: str = db.Column(db.String(30))#, db.ForeignKey(UserDto.userid))
    movie_id: int = db.Column(db.Integer)#, db.ForeignKey(MovieDto.id))
    
    def __init__(self, title, content, userid, movie_id):
        self.title = title
        self.content = content
        self.userid = userid
        self.movie_id = movie_id
        
    def __repr__(self):
                return f'id={self.id}, user_id={self.userid}, movie_id={self.movie_id},\
            title={self.title}, content={self.content}'
            
    @property
    def json(self):
        return {
            'id': self.id,
            'userid' : self.userid,
            'movie_id' : self.movie_id,
            'title' : self.title,
            'content' : self.content
        }
        
    def save(self):
        db.session.add(self)
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()