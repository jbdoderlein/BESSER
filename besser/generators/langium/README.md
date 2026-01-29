# Langium Grammar Generator

This generator transforms B-UML structural models into Langium grammar files.

## Quick Example

```python
from besser.generators.langium import LangiumGenerator
from besser.BUML.metamodel.structural import Class, DomainModel, StringType, Property

# Create a simple model
Book = Class(name="Book")
Book.attributes = {Property(name="title", type=StringType)}

model = DomainModel(name="Library", types={Book}, associations=set(), generalizations=set())

# Generate Langium grammar
generator = LangiumGenerator(model=model)
generator.generate()
```

This generates a `Library.langium` file in the `./output` directory.

## Features

- **Classes** → Langium rules
- **Attributes** → Properties with types
- **Enumerations** → Type unions
- **Associations** → Cross-references
- **Inheritance** → Extends clauses
- **Multi-valued attributes** → Array notation

## Generated Grammar Structure

The generator creates a complete Langium grammar with:

1. Entry rule for the model
2. Class rules for each UML class
3. Property rules for attributes
4. Reference rules for associations
5. Type definitions for enumerations
6. Terminal rules (ID, STRING, etc.)

See the [documentation](../../docs/source/generators/langium.rst) for detailed usage and examples.
