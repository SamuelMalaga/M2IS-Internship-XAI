class Project:
    def __init__(self,id, title, description, cost, category, district_code,district):
        self.id = id
        self.title=title
        self.description=description
        self.cost=cost
        self.category=category
        self.district_code = district_code
        self.district = district

    def __str__(self):
        return f"""
Project nommé: '{self.title}'
Quartier: {self.district}
        """
