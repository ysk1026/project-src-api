from com_sba_api.ext.db import db

class ItemDto(db.Model):
    __tablename__='items'
    __table_args__={'mysql_collate':'utf8_general_ci'}

    id : int = db.Column(db.Integer, primary_key=True, index=True)
    name : str = db.Column(db.String(30))
    price : str = db.Column(db.String(30))

    articles = db.relationship('ArticleDto', lazy='dynamic')

    def __init__(self, id, name, price):
        self.id = id
        self.name = name
        self.price = price


    def __repr__(self):
        return f'Item(id={self.id}, name={self.name}, price={self.price})'

    @property
    def json(self):
        return {'id': self.id, 'name': self.name, 'price': self.price}

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        





    