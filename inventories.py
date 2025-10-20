class Inventories:
    """
    Inventory of Canadian municipal open data ArcGIS endpoints.
    Organized by province and city.
    """

    data = {
        'British Columbia': {
            'Kelowna': 'https://geoportal.kelowna.ca/arcgis/rest/services/ArcGISOnline/OpenData_Environment/MapServer/17/query?outFields=*&where=1%3D1',
            'Maple Ridge': 'https://geoservices.mapleridge.ca/server/rest/services/DataCatalog/Environment/MapServer/5/query?outFields=*&where=1%3D1',
            'New Westminster': 'https://services3.arcgis.com/A7O8YnTNtzRPIn7T/arcgis/rest/services/Tree_Inventory_(PROD)_4_view/FeatureServer/0/query?outFields=*&where=1%3D1',
            'Vancouver': 'https://opendata.vancouver.ca/api/explore/v2.1/catalog/datasets/public-trees/records?limit=20',
            'Victoria': 'https://maps.victoria.ca/server/rest/services/OpenData/OpenData_Parks/MapServer/15/query?outFields=*&where=1%3D1',
        },

        'Alberta': {
            'Calgary': 'https://data.calgary.ca/api/v3/views/tfs4-3wwa/query.csv',
            'Edmonton': 'https://data.edmonton.ca/api/v3/views/eecg-fc54/query.csv',
            'Lethbridge': 'https://gis.lethbridge.ca/gisopendata/rest/services/OpenData/odl_trees/MapServer/0/query?outFields=*&where=1%3D1',
            'Strathcona County': 'https://services.arcgis.com/B7ZrK1Hv4P1dsm9R/arcgis/rest/services/Trees1/FeatureServer/0/query?outFields=*&where=1%3D1',
        },

        'Saskatchewan': {
            'Regina': 'https://opengis.regina.ca/arcgis/rest/services/CGISViewer/TreeWebApp/MapServer?f=pjson',
        },

        'Manitoba': {
            'Winnipeg': 'https://data.winnipeg.ca/api/v3/views/hfwk-jp4h/query.csv',
        },

        'Ontario': {
            # 'Toronto': 'https://example.com/toronto/opendata/query?outFields=*&where=1%3D1',
        },

        'Quebec': {
            'Longueuil': 'https://services2.arcgis.com/h4XWvDXfYYyD6jNu/arcgis/rest/services/DO_Arbres/FeatureServer/0/query?outFields=*&where=1%3D1',
            'Montreal': 'https://donnees.montreal.ca/api/3/action/datastore_search',
            'Quebec': 'https://www.donneesquebec.ca/recherche/dataset/34103a43-3712-4a29-92e1-039e9188e915/resource/13a51853-a5b5-4add-8791-02ccba5c1be7/download/vdq-arbrerepertorie.csv',
        },

        'New Brunswick': {
            'Fredericton': 'https://services2.arcgis.com/iLWAxhpxafhOza2U/arcgis/rest/services/Tree_Inventory/FeatureServer/37/query?outFields=*&where=1%3D1',
            'Moncton': 'https://services1.arcgis.com/E26PuSoie2Y7bbyI/arcgis/rest/services/Trees/FeatureServer/0/query?outFields=*&where=1%3D1',
        },

        'Nova Scotia': {
            'Halifax': 'https://services2.arcgis.com/11XBiaBYA9Ep0yNJ/arcgis/rest/services/Public_Trees/FeatureServer/0/query?outFields=*&where=1%3D1',
        },
    }