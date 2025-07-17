### This is the software made to generate conterfactual explanations based on user input. The explainability pipeline, the analysis and the presentation are the final output from the internship

#### This explanation pipeline is composed of:

├── Agent  
│   └── XAI_Agent.py  &#8594; Agent responsible for the analysis of the datasets on the pipeline  
├── Models  &#8594; Custom exceptions and modules for the pipeline  
│   ├── ProjectNotFoundException.py  
│   ├── Project.py  
├── Modules  &#8594; Modules responsibles for each specific analysis on the dataset  
│   ├── ElectionModule  &#8594; Module responsible for calculating the general status of the election  
│   │   ├── ELECMOD.py  
│   ├── FileProcessingModule  &#8594; Module responsible for file processing, more specifically structural file checking    
│   │   ├── FPMOD.py  
│   ├── OverlappingModule  &#8594; Module responsible for calculating the overlap between votebases for each project  
│   │   ├── OVERMOD.py  
│   │   └── voter_matrix  
│   │       └── voter_project_matrix.csv  &#8594; votes dataset  
│   ├── ProjectModule  &#8594; Module responsible for retrieving information about the projects in the election context  
│   │   ├── project_details  
│   │   │   └── project_details.csv  &#8594; project details dataset  
│   │   ├── PROJMOD.py  
│   └── SimilarityModule  &#8594; Module responsible for calculating the similarity between projects (this module contains the embedding model used as base)  
│       └── SMOD.py  
├── XAIConf  &#8594; Folder used to store the .ini configurations that controls some thresholds of the explanation  
│   └── XAI.ini  
└── XAI_Interface.py  &#8594; Main interaction venue for the pipeline  

### XAI.ini attributes
[OVERLAPPING]  &#8594; Thresholds for the overlapping analysis  

[SIMILARITY]  &#8594; Thresholds for the overlapping analysis and embedding model name used to calculate similarity  

[LOOSER_TOLERANCE]  &#8594; Thresholds for the looser project charachterization   

### This pipeline is very experimental and early work, there are a lot of rooms for improvement, here are some suggestions:
- **Enhance the file processing modules**: This can be done very quickly and this task would be composed of a automatic detection of the necessary files and if not present their automatic generation based on a .pb file. This can improve the user friendliness of the software
- **Enhance the logic of overlapping**: The overlapping module considers only the jaccard distance between the voters of two specific projects, this could be further improved by more creative work on the analysis of overlapping. This task would be more of a intellectual/research task than pure programming
- **Enhance the similiarity logic**: The similiarity logic is working for now but when we have more information about a project we truncate it to avoid embedding errors, a more sound and robust strategy should be implemented to guarantee that we do not have loss of information.
- **APIzation of the pipeline**: The pipeline is already conceptualized in a modular format but it can be more useful or easier to integrate in other systems if a REST-API is build based on this.