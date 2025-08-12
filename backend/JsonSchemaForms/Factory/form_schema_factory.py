from abc import ABC, abstractmethod
from typing import Dict, List, Union
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
    
    def create_form_creator(self, models: Dict[str, Model], form_id: str = None,
                          form_title: str = None, **kwargs) -> JsonFormCreator:
        """Create a multi model form creator."""
        return MultiModelFormCreator(
            models=models,
            form_id=form_id,
            form_title=form_title
        )

# Factory method for easy access
def get_form_factory(factory_type: str) -> FormSchemaFactory:
    """Get appropriate factory based on type."""
    factories = {
        'single': SingleModelFormFactory(),
        'multi': MultiModelFormFactory()
    }
    
    if factory_type not in factories:
        raise ValueError(f"Unknown factory type: {factory_type}")
    
    return factories[factory_type]