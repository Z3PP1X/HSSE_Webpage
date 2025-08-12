from abc import ABC, abstractmethod
from typing import Dict, List, Union
from django.db import models
from django.forms.models import fields_for_model
from django.core.exceptions import FieldDoesNotExist

class JsonFormCreator(ABC):
    """Abstract base class for JSON form creators."""
    
    def __init__(self, form_id: str, form_title: str):
        self.form_id = form_id
        self.form_title = form_title
        self.schema = {
            "form_id": form_id,
            "form_title": form_title,
            "shared_configs": {
                "ajax_configs": {}
            },
            "structure": []
        }
    
    @abstractmethod
    def build(self) -> dict:
        """Build and return the complete form schema."""
        pass
    
    def add_ajax_config(self, key: str, endpoint: str, method: str = "GET", 
                       events: List[str] = None, debounce: int = 300):
        """Add AJAX configuration to the schema."""
        if events is None:
            events = ["change", "blur"]
            
        self.schema["shared_configs"]["ajax_configs"][key] = {
            "endpoint": endpoint,
            "method": method,
            "triggerEvents": events,
            "debounceTime": debounce
        }
        return self
    
    def add_category(self, key: str, title: str, fields: List[dict] = None):
        """Add a category with fields to the form structure."""
        category = {
            "key": key,
            "title": title,
            "isCategory": True,
            "fields": fields or []
        }
        self.schema["structure"].append(category)
        return self

class ModelMetadataProvider(ABC):
    """Abstract provider for model metadata extraction."""
    
    @abstractmethod
    def _get_model_metadata(self, model_class: models.Model) -> Dict[str, dict]:
        """Extract metadata from a Django model."""
        pass

    def _get_field_type(self, field) -> str:
        """Convert Django field type to form field type."""
        field_class = field.__class__.__name__
        field_type_map = {
            'CharField': 'text',
            'TextField': 'textarea',
            'BooleanField': 'checkbox',
            'DateField': 'date',
            'DateTimeField': 'datetime',
            'IntegerField': 'number',
            'FloatField': 'number',
            'DecimalField': 'number',
            'EmailField': 'email',
            'URLField': 'url',
            'FileField': 'file',
            'ImageField': 'image',
            'ForeignKey': 'select',
            'ManyToManyField': 'multiselect',
        }
        return field_type_map.get(field_class, 'text')

    def _get_field_choices(self, field) -> Union[List[dict], None]:
        """Extract choices from field if available."""
        if hasattr(field, 'choices') and field.choices:
            return [{"value": key, "label": label} for key, label in field.choices]
        return None

class SingleModelFormCreator(JsonFormCreator, ModelMetadataProvider):
    """Creator for forms based on a single Django model."""
    
    def __init__(self, model_class: models.Model, form_id: str = None, 
                 form_title: str = None):
        self.model_class = model_class
        model_name = model_class.__name__
        
        super().__init__(
            form_id=form_id or f"{model_name.lower()}_form",
            form_title=form_title or f"{model_name} Form"
        )
        
        self.model_fields = {}
        self._extract_model_fields()
    
    def _get_model_metadata(self, model_class: models.Model = None) -> Dict[str, dict]:
        """Extract metadata from the model."""
        if model_class is None:
            model_class = self.model_class
            
        form_fields = fields_for_model(model_class)
        metadata = {}
        
        for field_name, form_field in form_fields.items():
            try:
                model_field = model_class._meta.get_field(field_name)
                metadata[field_name] = {
                    "key": field_name,
                    "label": model_field.verbose_name or field_name.replace('_', ' ').title(),
                    "help_text": model_field.help_text or "",
                    "required": not model_field.blank,
                    "field_type": self._get_field_type(model_field),
                    "choices": self._get_field_choices(model_field),
                    "model": model_class.__name__
                }
            except FieldDoesNotExist:
                continue
                
        return metadata
    
    def _extract_model_fields(self):
        """Extract field metadata from the model."""
        self.model_fields = self._get_model_metadata()
    
    def configure_from_dict(self, config: dict):
        """Configure the form schema from a dictionary."""
        # Apply AJAX configs
        if 'ajax_configs' in config:
            for key, cfg in config['ajax_configs'].items():
                self.add_ajax_config(
                    key, 
                    cfg['endpoint'], 
                    method=cfg.get('method', 'GET'),
                    events=cfg.get('events'),
                    debounce=cfg.get('debounce', 300)
                )
        
        # Handle categories
        if 'categories' in config:
            for cat in config['categories']:
                field_configs = []
                
                for field_name in cat.get('fields', []):
                    if field_name in self.model_fields:
                        field_info = self.model_fields[field_name].copy()
                        
                        # Apply field overrides
                        if 'field_overrides' in config and field_name in config['field_overrides']:
                            field_info.update(config['field_overrides'][field_name])
                        
                        field_configs.append(field_info)
                
                self.add_category(cat['key'], cat['title'], field_configs)
        
        return self
    
    def build(self) -> dict:
        """Build and return the complete form schema."""
        return self.schema

class MultiModelFormCreator(JsonFormCreator, ModelMetadataProvider):
    """Creator for forms based on multiple Django models."""
    
    def __init__(self, models: Dict[str, models.Model], form_id: str = None, 
                 form_title: str = None):
        self.models = models
        
        super().__init__(
            form_id=form_id or "multi_model_form",
            form_title=form_title or "Multi Model Form"
        )
        
        self.all_model_fields = {}
        self._extract_all_model_fields()
    
    def _get_model_metadata(self, model_class: models.Model) -> Dict[str, dict]:
        """Extract metadata from a specific model."""
        form_fields = fields_for_model(model_class)
        metadata = {}
        
        for field_name, form_field in form_fields.items():
            try:
                model_field = model_class._meta.get_field(field_name)
                # Prefix field name with model name to avoid conflicts
                prefixed_name = f"{model_class.__name__.lower()}_{field_name}"
                
                metadata[prefixed_name] = {
                    "key": prefixed_name,
                    "original_key": field_name,
                    "label": model_field.verbose_name or field_name.replace('_', ' ').title(),
                    "help_text": model_field.help_text or "",
                    "required": not model_field.blank,
                    "field_type": self._get_field_type(model_field),
                    "choices": self._get_field_choices(model_field),
                    "model": model_class.__name__
                }
            except FieldDoesNotExist:
                continue
                
        return metadata
    
    def _extract_all_model_fields(self):
        """Extract field metadata from all models."""
        for model_name, model_class in self.models.items():
            model_metadata = self._get_model_metadata(model_class)
            self.all_model_fields.update(model_metadata)
    
    def configure_from_dict(self, config: dict):
        """Configure the form schema from a dictionary."""
        # Apply AJAX configs
        if 'ajax_configs' in config:
            for key, cfg in config['ajax_configs'].items():
                self.add_ajax_config(
                    key, 
                    cfg['endpoint'], 
                    method=cfg.get('method', 'GET'),
                    events=cfg.get('events'),
                    debounce=cfg.get('debounce', 300)
                )
        
        # Handle categories with model-specific field mapping
        if 'categories' in config:
            for cat in config['categories']:
                field_configs = []
                
                for field_spec in cat.get('fields', []):
                    # Field spec can be either string or dict with model info
                    if isinstance(field_spec, str):
                        # Try to find field in all models
                        if field_spec in self.all_model_fields:
                            field_info = self.all_model_fields[field_spec].copy()
                            field_configs.append(field_info)
                    elif isinstance(field_spec, dict):
                        # Explicit model.field specification
                        model_name = field_spec.get('model')
                        field_name = field_spec.get('field')
                        
                        if model_name and field_name:
                            prefixed_name = f"{model_name.lower()}_{field_name}"
                            if prefixed_name in self.all_model_fields:
                                field_info = self.all_model_fields[prefixed_name].copy()
                                
                                # Apply any field-specific overrides
                                if 'overrides' in field_spec:
                                    field_info.update(field_spec['overrides'])
                                
                                field_configs.append(field_info)
                
                self.add_category(cat['key'], cat['title'], field_configs)
        
        return self
    
    def build(self) -> dict:
        """Build and return the complete form schema."""
        return self.schema