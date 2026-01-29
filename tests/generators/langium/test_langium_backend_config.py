"""
Test the Langium generator backend configuration.
"""
import pytest


def test_langium_generator_is_registered():
    """Test that the Langium generator is properly registered in the backend."""
    from besser.utilities.web_modeling_editor.backend.config.generators import (
        SUPPORTED_GENERATORS,
        get_generator_info,
        get_filename_for_generator,
        is_generator_supported
    )
    
    # Test that langium is supported
    assert is_generator_supported("langium")
    assert "langium" in SUPPORTED_GENERATORS
    
    # Test generator info
    info = get_generator_info("langium")
    assert info is not None
    assert info.generator_class.__name__ == "LangiumGenerator"
    assert info.output_type == "file"
    assert info.file_extension == ".langium"
    assert info.category == "language_engineering"
    assert info.requires_class_diagram is True
    
    # Test filename generation
    filename = get_filename_for_generator("langium", "MyModel")
    assert filename == "MyModel.langium"
    
    # Test with default base name
    filename_default = get_filename_for_generator("langium")
    assert filename_default == "output.langium"


def test_langium_generator_class_import():
    """Test that the LangiumGenerator class can be imported from config."""
    from besser.utilities.web_modeling_editor.backend.config.generators import SUPPORTED_GENERATORS
    from besser.generators.langium import LangiumGenerator
    
    langium_info = SUPPORTED_GENERATORS["langium"]
    assert langium_info.generator_class is LangiumGenerator
