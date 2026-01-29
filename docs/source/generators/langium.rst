Langium Grammar Generator
==========================

The Langium grammar generator transforms B-UML structural models into Langium grammar files. Langium is a modern 
language engineering framework for building Domain-Specific Languages (DSLs) with full IDE support, particularly 
for VS Code and web-based editors.

What is Langium?
----------------

Langium is a TypeScript-based language workbench that allows you to create custom DSLs with features like:

- Syntax highlighting
- Auto-completion
- Error checking
- Cross-references
- Language servers

The generator creates ``.langium`` grammar files that can be used as the foundation for building your own 
domain-specific language based on your UML model.

Usage
-----

To generate a Langium grammar from your :doc:`../buml_language/model_types/structural`, create a 
``LangiumGenerator`` object and use the ``generate`` method:

.. code-block:: python
    
    from besser.generators.langium import LangiumGenerator
    
    # Generate using model name as grammar name
    generator = LangiumGenerator(model=library_model)
    generator.generate()
    
    # Or specify a custom grammar name
    generator = LangiumGenerator(model=library_model, grammar_name="LibraryDSL")
    generator.generate()

The generated ``.langium`` file will be created in the ``<<current_directory>>/output`` folder by default. 
You can specify a custom output directory:

.. code-block:: python
    
    generator = LangiumGenerator(model=library_model, output_dir="./my_langium_project")
    generator.generate()

Generated Grammar Structure
----------------------------

The generated Langium grammar includes:

**1. Enumerations**

UML enumerations are mapped to Langium type definitions:

.. code-block:: langium

    type MemberType = 'ADULT' | 'SENIOR' | 'STUDENT' | 'CHILD';

**2. Entry Rule**

A top-level model entry point:

.. code-block:: langium

    entry Model:
        'model' name=ID '{'
            (elements+=ModelElement)*
        '}';

**3. Class Rules**

Each UML class becomes a Langium grammar rule:

.. code-block:: langium

    Book:
        'book' name=ID '{'
            (
                properties+=BookProperty | 
                references+=BookReference
            )*
        '}';

**4. Properties**

Attributes are mapped to properties with their types:

.. code-block:: langium

    BookProperty:
        title=TitleProperty | pages=PagesProperty;
    
    TitleProperty:
        'title' ':' value=str ';';

**5. References**

Associations become cross-references in Langium:

.. code-block:: langium

    AuthorsReference:
        'authors' ':' target=[Author:ID] (',' target=[Author:ID])* ';';

**6. Inheritance**

Class inheritance is represented using the ``extends`` keyword:

.. code-block:: langium

    Dog:
        'dog' name=ID ('extends' parent=[Animal:ID])? '{'
            (properties+=DogProperty)*
        '}';

**7. Terminal Rules**

Standard terminal rules for identifiers, whitespace, and comments are included:

.. code-block:: langium

    terminal ID: /[_a-zA-Z][\w_]*/;
    hidden terminal WS: /\s+/;
    hidden terminal ML_COMMENT: /\/\*[\s\S]*?\*\//;
    hidden terminal SL_COMMENT: /\/\/[^\n\r]*/;

Example
-------

Given a simple library model with classes ``Book``, ``Author``, and an enumeration ``MemberType``, 
the generator produces a complete Langium grammar file that can be used to:

1. Create a Langium language server project
2. Build a VS Code extension for your DSL
3. Implement custom validation rules
4. Add semantic analysis

Using the Generated Grammar
----------------------------

After generating the ``.langium`` file, you can use it in a Langium project:

1. **Create a Langium project:**

   .. code-block:: bash

       npm init -y
       npm install langium langium-cli

2. **Place your grammar:**

   Copy the generated ``.langium`` file to your project's grammar directory.

3. **Generate language artifacts:**

   .. code-block:: bash

       npx langium generate

4. **Build your language tooling:**

   The Langium CLI will generate TypeScript code for your AST, parser, and language server.

References
----------

- `Langium Official Documentation <https://langium.org/docs/>`_
- `Langium GitHub Repository <https://github.com/langium/langium>`_
- `Building Language Servers with Langium <https://langium.org/docs/learn/workflow/>`_

For inspiration on UML to Langium transformation, see the 
`uml2langium project <https://github.com/NathanLeGuillou/uml2langium>`_.
