class Project:
    def __init__(self,id, title, description, cost, category, district_code,district, vote_count):
        self.id = id
        self.title=title
        self.description=description
        self.cost=cost
        self.category=category
        self.district_code = district_code
        self.district = district
        self.vote_count = vote_count

    def __str__(self):
        return f"""
Project nommé: '{self.title}'
Quartier: {self.district}
        """
    
    def to_string(self):
        return f"""
        Title:{self.description},
        Description:{self.description}
        Cost:{self.cost}
        Category: {self.category}
        District_code: {self.district_code}
        District: {self.district}
        """

    def __eq__(self, other):
        if not isinstance(other, Project):
            return NotImplemented
        
        return self.id == other.id
    
    def __hash__(self):
        return hash((self.id))