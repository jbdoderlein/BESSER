import os
import pytest
from besser.generators.langium import LangiumGenerator
from besser.BUML.metamodel.structural import (
    Class, DomainModel, Enumeration, EnumerationLiteral,
    DateType, StringType, IntegerType, Property, BinaryAssociation,
    Multiplicity, Generalization
)


@pytest.fixture
def domain_model():
    """
    Create a sample domain model for testing the Langium generator.
    This model includes classes, enumerations, attributes, associations, and inheritance.
    """
    # Create an enumeration for member types
    MemberType: Enumeration = Enumeration(
        name="MemberType",
        literals={
            EnumerationLiteral(name="ADULT"),
            EnumerationLiteral(name="SENIOR"),
            EnumerationLiteral(name="STUDENT"),
            EnumerationLiteral(name="CHILD")
        }
    )

    # Define classes
    Book = Class(name="Book")
    Author = Class(name="Author")
    Library = Class(name="Library")

    # Book class attributes
    Book_release: Property = Property(name="release", type=DateType)
    Book_title: Property = Property(name="title", type=StringType)
    Book_pages: Property = Property(name="pages", type=IntegerType)
    Book.attributes = {Book_release, Book_title, Book_pages}

    # Author class attributes
    Author_email: Property = Property(name="email", type=StringType)
    Author_member: Property = Property(name="member", type=MemberType)
    Author.attributes = {Author_email, Author_member}

    # Library class attributes
    Library_name: Property = Property(name="name", type=StringType)
    Library_address: Property = Property(name="address", type=StringType)
    Library.attributes = {Library_name, Library_address}

    # Relationships
    has: BinaryAssociation = BinaryAssociation(
        name="Has",
        ends={
            Property(name="books", type=Book, multiplicity=Multiplicity(0, "*")),
            Property(name="library", type=Library, multiplicity=Multiplicity(1, 1))
        }
    )
    
    book_author_relation: BinaryAssociation = BinaryAssociation(
        name="BookAuthor_Relation",
        ends={
            Property(name="authors", type=Author, multiplicity=Multiplicity(1, "*")),
            Property(name="books", type=Book, multiplicity=Multiplicity(0, "*"))
        }
    )

    # Domain Model
    model = DomainModel(
        name="LibraryDomain",
        types={Book, Author, Library, MemberType},
        associations={has, book_author_relation},
        generalizations=set()
    )

    return model


def test_langium_generator_creates_file(domain_model, tmpdir):
    """Test that the Langium generator creates a grammar file."""
    output_dir = tmpdir.mkdir("output")
    generator = LangiumGenerator(model=domain_model, output_dir=str(output_dir))

    # Generate Langium grammar
    generator.generate()

    # Check if the file was created
    output_file = os.path.join(str(output_dir), "LibraryDomain.langium")
    assert os.path.isfile(output_file)


def test_langium_grammar_contains_grammar_declaration(domain_model, tmpdir):
    """Test that the generated grammar contains the grammar declaration."""
    output_dir = tmpdir.mkdir("output")
    generator = LangiumGenerator(model=domain_model, output_dir=str(output_dir))
    generator.generate()

    output_file = os.path.join(str(output_dir), "LibraryDomain.langium")
    with open(output_file, "r", encoding="utf-8") as f:
        generated_code = f.read()

    assert "grammar LibraryDomain" in generated_code


def test_langium_grammar_contains_classes(domain_model, tmpdir):
    """Test that the generated grammar contains class definitions."""
    output_dir = tmpdir.mkdir("output")
    generator = LangiumGenerator(model=domain_model, output_dir=str(output_dir))
    generator.generate()

    output_file = os.path.join(str(output_dir), "LibraryDomain.langium")
    with open(output_file, "r", encoding="utf-8") as f:
        generated_code = f.read()

    # Check for class rules
    assert "Book:" in generated_code
    assert "Author:" in generated_code
    assert "Library:" in generated_code


def test_langium_grammar_contains_enumerations(domain_model, tmpdir):
    """Test that the generated grammar contains enumeration definitions."""
    output_dir = tmpdir.mkdir("output")
    generator = LangiumGenerator(model=domain_model, output_dir=str(output_dir))
    generator.generate()

    output_file = os.path.join(str(output_dir), "LibraryDomain.langium")
    with open(output_file, "r", encoding="utf-8") as f:
        generated_code = f.read()

    # Check for enumeration
    assert "type MemberType" in generated_code
    assert "'ADULT'" in generated_code
    assert "'SENIOR'" in generated_code
    assert "'STUDENT'" in generated_code
    assert "'CHILD'" in generated_code


def test_langium_grammar_contains_attributes(domain_model, tmpdir):
    """Test that the generated grammar contains attribute definitions."""
    output_dir = tmpdir.mkdir("output")
    generator = LangiumGenerator(model=domain_model, output_dir=str(output_dir))
    generator.generate()

    output_file = os.path.join(str(output_dir), "LibraryDomain.langium")
    with open(output_file, "r", encoding="utf-8") as f:
        generated_code = f.read()

    # Check for attributes
    assert "release" in generated_code
    assert "title" in generated_code
    assert "pages" in generated_code
    assert "email" in generated_code
    assert "name" in generated_code
    assert "address" in generated_code


def test_langium_grammar_contains_terminal_rules(domain_model, tmpdir):
    """Test that the generated grammar contains terminal rules."""
    output_dir = tmpdir.mkdir("output")
    generator = LangiumGenerator(model=domain_model, output_dir=str(output_dir))
    generator.generate()

    output_file = os.path.join(str(output_dir), "LibraryDomain.langium")
    with open(output_file, "r", encoding="utf-8") as f:
        generated_code = f.read()

    # Check for terminal rules
    assert "terminal ID:" in generated_code
    assert "terminal WS:" in generated_code


def test_langium_generator_custom_name(domain_model, tmpdir):
    """Test that the generator respects custom grammar names."""
    output_dir = tmpdir.mkdir("output")
    custom_name = "MyCustomLibrary"
    generator = LangiumGenerator(
        model=domain_model, 
        output_dir=str(output_dir),
        grammar_name=custom_name
    )
    generator.generate()

    # Check if the file was created with custom name
    output_file = os.path.join(str(output_dir), f"{custom_name}.langium")
    assert os.path.isfile(output_file)

    # Check grammar declaration uses custom name
    with open(output_file, "r", encoding="utf-8") as f:
        generated_code = f.read()
    assert f"grammar {custom_name}" in generated_code


def test_langium_generator_with_inheritance(tmpdir):
    """Test Langium generation with class inheritance."""
    # Create classes with inheritance
    Animal = Class(name="Animal")
    Animal_name = Property(name="name", type=StringType)
    Animal.attributes = {Animal_name}

    Dog = Class(name="Dog")
    Dog_breed = Property(name="breed", type=StringType)
    Dog.attributes = {Dog_breed}

    # Set up inheritance
    generalization = Generalization(general=Animal, specific=Dog)

    model = DomainModel(
        name="AnimalDomain",
        types={Animal, Dog},
        associations=set(),
        generalizations={generalization}
    )

    output_dir = tmpdir.mkdir("output")
    generator = LangiumGenerator(model=model, output_dir=str(output_dir))
    generator.generate()

    output_file = os.path.join(str(output_dir), "AnimalDomain.langium")
    with open(output_file, "r", encoding="utf-8") as f:
        generated_code = f.read()

    # Check for inheritance syntax
    assert "Dog:" in generated_code
    assert "extends" in generated_code or "parent=" in generated_code
