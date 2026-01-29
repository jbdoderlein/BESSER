import os
import pytest
from besser.generators.langium import LangiumGenerator
from besser.BUML.metamodel.structural import (
    Class, DomainModel, Enumeration, EnumerationLiteral,
    DateType, StringType, IntegerType, FloatType, BooleanType, Property, BinaryAssociation,
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

    # Check for inheritance syntax - both keywords should appear together
    assert "extends" in generated_code
    assert "parent=[Animal:ID]" in generated_code


def test_langium_generator_multi_valued_attributes(tmpdir):
    """Test Langium generation with multi-valued attributes."""
    Person = Class(name="Person")
    Person_name = Property(name="name", type=StringType)
    Person_hobbies = Property(name="hobbies", type=StringType, multiplicity=Multiplicity(0, "*"))
    Person.attributes = {Person_name, Person_hobbies}

    model = DomainModel(
        name="PersonDomain",
        types={Person},
        associations=set(),
        generalizations=set()
    )

    output_dir = tmpdir.mkdir("output")
    generator = LangiumGenerator(model=model, output_dir=str(output_dir))
    generator.generate()

    output_file = os.path.join(str(output_dir), "PersonDomain.langium")
    with open(output_file, "r", encoding="utf-8") as f:
        generated_code = f.read()

    # Check that multi-valued attributes have required array notation
    assert "hobbies" in generated_code
    # Array brackets should be present for multi-valued attributes
    assert "('[' ']')" in generated_code or "[ ]" in generated_code


def test_langium_generator_non_navigable_associations(tmpdir):
    """Test that non-navigable association ends don't generate reference rules."""
    Car = Class(name="Car")
    Car_model = Property(name="model", type=StringType)
    Car.attributes = {Car_model}

    Owner = Class(name="Owner")
    Owner_name = Property(name="name", type=StringType)
    Owner.attributes = {Owner_name}

    # Create association with only one navigable end
    ownership = BinaryAssociation(
        name="Ownership",
        ends={
            Property(name="car", type=Car, multiplicity=Multiplicity(1, 1), is_navigable=True),
            Property(name="owner", type=Owner, multiplicity=Multiplicity(1, 1), is_navigable=False)
        }
    )

    model = DomainModel(
        name="CarDomain",
        types={Car, Owner},
        associations={ownership},
        generalizations=set()
    )

    output_dir = tmpdir.mkdir("output")
    generator = LangiumGenerator(model=model, output_dir=str(output_dir))
    generator.generate()

    output_file = os.path.join(str(output_dir), "CarDomain.langium")
    with open(output_file, "r", encoding="utf-8") as f:
        generated_code = f.read()

    # Owner should have an inline reference to Car using association name (navigable)
    assert "'Ownership' ':' Ownership=[Car:ID]" in generated_code
    
    # Car should NOT have a reference to Owner (non-navigable)
    # Check that Car class doesn't contain 'owner' or 'Ownership' reference
    car_section = generated_code.split("// Owner class definition")[0]
    assert "'owner'" not in car_section or "owner=" not in car_section


def test_langium_generator_empty_model(tmpdir):
    """Test Langium generation with a model that has no classes."""
    model = DomainModel(
        name="EmptyDomain",
        types=set(),
        associations=set(),
        generalizations=set()
    )

    output_dir = tmpdir.mkdir("output")
    generator = LangiumGenerator(model=model, output_dir=str(output_dir))
    generator.generate()

    output_file = os.path.join(str(output_dir), "EmptyDomain.langium")
    assert os.path.isfile(output_file)
    
    with open(output_file, "r", encoding="utf-8") as f:
        generated_code = f.read()

    # Should have a valid ModelElement rule even with no classes
    assert "ModelElement:" in generated_code
    # Should generate a fallback element
    assert "EmptyElement" in generated_code


def test_langium_terminal_types_for_primitives(tmpdir):
    """Test that primitive types map to proper Langium terminals."""
    Product = Class(name="Product")
    Product.attributes = {
        Property(name="name", type=StringType),
        Property(name="price", type=IntegerType),
        Property(name="weight", type=FloatType),
        Property(name="inStock", type=BooleanType),
        Property(name="releaseDate", type=DateType)
    }

    model = DomainModel(
        name="ProductDomain",
        types={Product},
        associations=set(),
        generalizations=set()
    )

    output_dir = tmpdir.mkdir("output")
    generator = LangiumGenerator(model=model, output_dir=str(output_dir))
    generator.generate()

    output_file = os.path.join(str(output_dir), "ProductDomain.langium")
    with open(output_file, "r", encoding="utf-8") as f:
        generated_code = f.read()

    # Should use terminal references in inline format, not raw type names
    assert "name=STRING" in generated_code
    assert "price=INT" in generated_code
    assert "weight=FLOAT" in generated_code
    assert "inStock=BOOLEAN" in generated_code
    assert "releaseDate=DATE" in generated_code
    
    # Should NOT have raw type names
    assert "=str" not in generated_code
    assert "=int " not in generated_code  # space after to avoid matching "=INT"
    assert "=date " not in generated_code  # space after to avoid matching "=DATE"


def test_langium_multi_valued_references_use_plus_equals(tmpdir):
    """Test that multi-valued references use += operator instead of =."""
    Product = Class(name="Product")
    Product.attributes = {Property(name="name", type=StringType)}

    Category = Class(name="Category")
    Category.attributes = {Property(name="title", type=StringType)}

    # Multi-valued association (should use +=)
    product_categories = BinaryAssociation(
        name="ProductCategories",
        ends={
            Property(name="products", type=Product, multiplicity=Multiplicity(0, "*")),
            Property(name="categories", type=Category, multiplicity=Multiplicity(1, "*"))
        }
    )

    model = DomainModel(
        name="ECommerce",
        types={Product, Category},
        associations={product_categories},
        generalizations=set()
    )

    output_dir = tmpdir.mkdir("output")
    generator = LangiumGenerator(model=model, output_dir=str(output_dir))
    generator.generate()

    output_file = os.path.join(str(output_dir), "ECommerce.langium")
    with open(output_file, "r", encoding="utf-8") as f:
        generated_code = f.read()

    # Multi-valued references should use += operator with association name
    assert "ProductCategories+=[Product:ID]" in generated_code
    assert "ProductCategories+=[Category:ID]" in generated_code
    
    # Should have the repeated assignment pattern with += for the same field
    assert "(',' ProductCategories+=[Product:ID])" in generated_code
    assert "(',' ProductCategories+=[Category:ID])" in generated_code
