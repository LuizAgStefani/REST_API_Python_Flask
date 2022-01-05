from sql_alchemy import banco


class SiteModel(banco.Model):
    __tablename__ = 'sites'

    site_id = banco.Column(banco.Integer, primary_key=True)
    url = banco.Column(banco.String(80))
    hoteis = banco.relationship('HotelModel')   # lista de objetos hoteis

    def __init__(self, url):
        self.url = url

    def json(self):
        return {
            'site_id': self.site_id,
            'url': self.url,
            'hoteis': [hotel.json() for hotel in self.hoteis]
        }

    @classmethod
    def find_site(cls, url):
        # SELECT * FROM hoteis where hotel_id = $id
        site = cls.query.filter_by(url=url).first()
        if site:
            return site
        return None

    @classmethod
    def find_by_id(cls, id):
        site = cls.query.filter_by(site_id=id).first()
        if site:
            return site
        return None

    def save_site(self):
        # Adicionando novo hotel = INSERT
        banco.session.add(self)
        banco.session.commit()

    def delete_site(self):
        # deletando todos os hotéis associados ao site
        [hotel.delete_hotel() for hotel in self.hoteis]

        banco.session.delete(self)
        banco.session.commit()
