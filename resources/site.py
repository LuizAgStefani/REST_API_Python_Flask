from flask_restful import Resource, reqparse
from models.site import SiteModel


class Sites(Resource):
    def get(self):
        return {'sites': [site.json() for site in SiteModel.query.all()]}


class Site(Resource):

    argumentos = reqparse.RequestParser()
    argumentos

    def get(self, url):
        site = SiteModel.find_site(url)
        if site:
            return site.json()
        return {'message': 'Site Not Found.'}, 404

    def post(self, url):
        if SiteModel.find_site(url):
            return {'message': "A website with URL '{}' already exists.".format(url)}, 400
        site = SiteModel(url)
        try:
            site.save_site()

        except:
            return {'message': 'An internal error ocurred trying to create a new website.'}, 500

        return site.json()

    def delete(self, url):
        site = SiteModel.find_site(url)
        if site:
            try:
                site.delete_site()
            except:
                return {'message': 'An internal error ocurred trying to delete this website'}, 500
            return {'message': 'Site deleted successfully.'}, 200
