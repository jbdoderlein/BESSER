import os
from jinja2 import Environment, FileSystemLoader
from besser.BUML.metamodel.structural import DomainModel
from besser.generators import GeneratorInterface


class LangiumGenerator(GeneratorInterface):
    """
    LangiumGenerator is a class that implements the GeneratorInterface and is responsible
    for generating Langium grammar files based on the input B-UML model.

    Langium is a language engineering framework for building Domain-Specific Languages (DSLs)
    with IDE support. This generator transforms B-UML structural models into Langium grammar
    definitions that can be used to create language tooling.

    Args:
        model (DomainModel): An instance of the DomainModel class representing the B-UML model.
        output_dir (str, optional): The output directory where the generated grammar will be 
            saved. Defaults to None.
        grammar_name (str, optional): The name of the Langium grammar. Defaults to the model name.
    """
    def __init__(self, model: DomainModel, output_dir: str = None, grammar_name: str = None):
        super().__init__(model, output_dir)
        self.grammar_name = grammar_name if grammar_name else model.name

    def generate(self):
        """
        Generates a Langium grammar file based on the provided B-UML model and saves it to 
        the specified output directory.
        If the output directory was not specified, the grammar will be stored in the 
        <current directory>/output folder.

        The generated grammar includes:
        - Entry rule for the model
        - Rules for each class in the domain model
        - Enumerations
        - Type definitions for primitive types
        - Cross-references for associations

        Returns:
            None, but stores the generated grammar as a file named <grammar_name>.langium
        """
        # Use the grammar name for the filename, with .langium extension
        file_name = f"{self.grammar_name}.langium"
        file_path = self.build_generation_path(file_name=file_name)
        
        templates_path = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), "templates")
        env = Environment(loader=FileSystemLoader(templates_path), 
                         trim_blocks=True, lstrip_blocks=True)
        template = env.get_template('langium_grammar.j2')
        
        with open(file_path, mode="w", encoding='utf-8') as f:
            generated_code = template.render(
                model=self.model,
                grammar_name=self.grammar_name
            )
            f.write(generated_code)
            print(f"Langium grammar generated in the location: {file_path}")
