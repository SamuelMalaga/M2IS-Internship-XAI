class Election:

    """
        This class is the responsible to organize and output the objects related to a election
        in the explainability pipeline
    """

    def __init__(self, pb_file_path, project_descritpion_file_path=None):
        self.pb_file_path = pb_file_path
        self.project_descritpion_file_path = project_descritpion_file_path