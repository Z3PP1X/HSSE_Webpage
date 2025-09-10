from abc import ABC, abstractmethod
from typing import Dict, Optional
from django.db.models import Model
from .json_form_creator import JsonFormCreator, SingleModelFormCreator, MultiModelFormCreator


class FormSchemaFactory(ABC):
    """Abstract factory for creating form schemas."""

    @abstractmethod
    def create_form_creator(self, **kwargs) -> JsonFormCreator:
        """Create appropriate form creator instance."""
        pass


class SingleModelFormFactory(FormSchemaFactory):
    """Factory for creating forms from a single Django model."""

    def create_form_creator(self, model_class: Model, form_id: str = None,
                            form_title: str = None, **kwargs) -> JsonFormCreator:
        """Create a single model form creator."""
        return SingleModelFormCreator(
            model_class=model_class,
            form_id=form_id,
            form_title=form_title
        )


class MultiModelFormFactory(FormSchemaFactory):
    """Factory for creating forms from multiple Django models."""

    def __init__(self, config: Optional[Dict] = None):
        """Initialize with optional configuration for new config-based approach."""
        self.config = config

    def create_form_creator(self, models: Dict[str, Model] = None,
                            config: Dict = None, form_id: str = None,
                            form_title: str = None, **kwargs) -> JsonFormCreator:
        """Create a multi model form creator with support for both legacy and new approaches."""
        # Use factory-level config if no config provided in method call
        effective_config = config or self.config

        return MultiModelFormCreator(
            models=models,
            config=effective_config,
            form_id=form_id,
            form_title=form_title
        )


# Factory method for easy access
def get_form_factory(factory_type: str, config: Optional[Dict] = None) -> FormSchemaFactory:
    """Get appropriate factory based on type with optional configuration."""
    if factory_type == 'single':
        return SingleModelFormFactory()
    elif factory_type == 'multi':
        # Don't require config for legacy support
        return MultiModelFormFactory(config)
    else:
        raise ValueError(f"Unknown factory type: {factory_type}")
