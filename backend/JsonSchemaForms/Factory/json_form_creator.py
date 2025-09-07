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
        """Configure the form schema from a dictionary with dynamic AJAX support."""
        
        # Apply global AJAX configs
        if 'ajax_configs' in config:
            for key, cfg in config['ajax_configs'].items():
                self.add_ajax_config(
                    key, 
                    cfg['endpoint'], 
                    method=cfg.get('method', 'GET'),
                    events=cfg.get('events'),
                    debounce=cfg.get('debounce', 300)
                )
        
        # Handle categories with dynamic field configurations
        if 'categories' in config:
            for cat in config['categories']:
                field_configs = []
                
                for field_spec in cat.get('fields', []):
                    if isinstance(field_spec, str):
                        # Simple field name
                        field_name = field_spec
                        field_info = self.model_fields[field_name].copy()
                    elif isinstance(field_spec, dict):
                        # Complex field configuration with potential AJAX
                        field_name = field_spec.get('field')
                        field_info = self.model_fields[field_name].copy()
                        
                        # Apply field-specific overrides
                        if 'overrides' in field_spec:
                            field_info.update(field_spec['overrides'])
                        
                        # Handle dynamic AJAX configuration
                        if 'ajax' in field_spec:
                            ajax_config = field_spec['ajax']
                            
                            # Generate unique AJAX config key
                            ajax_key = f"{field_name}_ajax_{cat['key']}"
                            
                            # Add the AJAX config to shared configs
                            self.add_ajax_config(
                                ajax_key,
                                ajax_config['endpoint'],
                                method=ajax_config.get('method', 'GET'),
                                events=ajax_config.get('events', ['change']),
                                debounce=ajax_config.get('debounce', 300)
                            )
                            
                            # Update field to reference the AJAX config
                            field_info.update({
                                'field_type': ajax_config.get('field_type', 'ajax_select'),
                                'ajax_config': ajax_key,
                                'search_field': ajax_config.get('search_field'),
                                'display_field': ajax_config.get('display_field'),
                                'value_field': ajax_config.get('value_field', 'id')
                            })
                    
                    field_configs.append(field_info)
                
                self.add_category(cat['key'], cat['title'], field_configs)
        
        return self
    
    def build(self) -> dict:
        """Build and return the complete form schema."""
        return self.schema

class MultiModelFormCreator(JsonFormCreator, ModelMetadataProvider):
    """Creator for forms based on multiple Django models with support for multiple instances."""
    
    def __init__(self, models: Dict[str, models.Model] = None, 
                 config: Dict = None, form_id: str = None, 
                 form_title: str = None):
        """
        Initialize with either models dict (legacy) or config object (new).
        
        Config structure:
        {
            "models": {
                "contact_primary": {
                    "model": ContactPerson,
                    "instance_label": "Primary Contact"
                },
                "contact_secondary": {
                    "model": ContactPerson, 
                    "instance_label": "Secondary Contact"
                },
                "alarmplan": {
                    "model": Alarmplan,
                    "instance_label": "Alarm Plan"
                }
            }
        }
        """
        if config:
            self.models = {}
            self.model_instances = config.get('models', {})
            # Extract unique models for metadata extraction
            for instance_key, instance_config in self.model_instances.items():
                model_class = instance_config['model']
                self.models[model_class.__name__] = model_class
        elif models:
            # Legacy support
            self.models = models
            self.model_instances = {
                model_name.lower(): {
                    'model': model_class,
                    'instance_label': model_class.__name__
                }
                for model_name, model_class in models.items()
            }
        else:
            raise ValueError("Either 'models' or 'config' must be provided")
        
        super().__init__(
            form_id=form_id or "multi_model_form",
            form_title=form_title or "Multi Model Form"
        )
        
        self.all_model_fields = {}
        self._extract_all_model_fields()
    
    def _extract_all_model_fields(self):
        """Extract field metadata from all model instances."""
        for instance_key, instance_config in self.model_instances.items():
            model_class = instance_config['model']
            instance_label = instance_config.get('instance_label', model_class.__name__)
            
            model_metadata = self._get_model_metadata_for_instance(
                model_class, instance_key, instance_label
            )
            self.all_model_fields.update(model_metadata)
    
    def _get_model_metadata_for_instance(self, model_class: models.Model, 
                                       instance_key: str, instance_label: str) -> Dict[str, dict]:
        """Extract metadata for a specific model instance."""
        form_fields = fields_for_model(model_class)
        metadata = {}
        
        for field_name, form_field in form_fields.items():
            try:
                model_field = model_class._meta.get_field(field_name)
                # Use instance key as prefix instead of model name
                prefixed_name = f"{instance_key}_{field_name}"
                
                # Create default label combining instance label with field name
                default_label = f"{instance_label} - {model_field.verbose_name or field_name.replace('_', ' ').title()}"
                
                metadata[prefixed_name] = {
                    "key": prefixed_name,
                    "original_key": field_name,
                    "instance_key": instance_key,
                    "label": default_label,
                    "help_text": model_field.help_text or "",
                    "required": not model_field.blank,
                    "field_type": self._get_field_type(model_field),
                    "choices": self._get_field_choices(model_field),
                    "model": model_class.__name__
                }
            except FieldDoesNotExist:
                continue
                
        return metadata
    
    def configure_from_dict(self, config: dict):
        """Configure the form schema from a dictionary with support for custom questions."""
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
                    if isinstance(field_spec, str):
                        # Simple field reference - try to find in all model fields
                        if field_spec in self.all_model_fields:
                            field_info = self.all_model_fields[field_spec].copy()
                            field_configs.append(field_info)
                    elif isinstance(field_spec, dict):
                        field_info = self._process_field_spec(field_spec)
                        if field_info:
                            field_configs.append(field_info)
                
                self.add_category(cat['key'], cat['title'], field_configs)
        
        return self
    
    def _process_field_spec(self, field_spec: dict) -> Union[Dict, None]:
        """Process a field specification and return field info."""
        # Support for instance-based field specification
        if 'instance' in field_spec and 'field' in field_spec:
            instance_key = field_spec['instance']
            field_name = field_spec['field']
            prefixed_name = f"{instance_key}_{field_name}"
            
            if prefixed_name in self.all_model_fields:
                field_info = self.all_model_fields[prefixed_name].copy()
                
                # Override label with custom question if provided
                if 'question' in field_spec:
                    field_info['label'] = field_spec['question']
                
                # Apply any other field-specific overrides
                if 'overrides' in field_spec:
                    field_info.update(field_spec['overrides'])
                
                # Handle AJAX configuration
                if 'ajax' in field_spec:
                    self._apply_ajax_config(field_info, field_spec['ajax'], prefixed_name)
                
                return field_info
        
        # Legacy support for model-based specification
        elif 'model' in field_spec and 'field' in field_spec:
            model_name = field_spec['model']
            field_name = field_spec['field']
            
            # Find the first instance of this model
            for instance_key, instance_config in self.model_instances.items():
                if instance_config['model'].__name__ == model_name:
                    prefixed_name = f"{instance_key}_{field_name}"
                    if prefixed_name in self.all_model_fields:
                        field_info = self.all_model_fields[prefixed_name].copy()
                        
                        # Apply overrides and AJAX as before
                        if 'overrides' in field_spec:
                            field_info.update(field_spec['overrides'])
                        if 'ajax' in field_spec:
                            self._apply_ajax_config(field_info, field_spec['ajax'], prefixed_name)
                        
                        return field_info
                    break
        
        return None
    
    def _apply_ajax_config(self, field_info: dict, ajax_config: dict, field_key: str):
        """Apply AJAX configuration to a field."""
        ajax_key = f"{field_key}_ajax"
        
        self.add_ajax_config(
            ajax_key,
            ajax_config['endpoint'],
            method=ajax_config.get('method', 'GET'),
            events=ajax_config.get('events', ['change']),
            debounce=ajax_config.get('debounce', 300)
        )
        
        field_info.update({
            'field_type': ajax_config.get('field_type', 'ajax_select'),
            'ajax_config': ajax_key,
            'search_field': ajax_config.get('search_field'),
            'display_field': ajax_config.get('display_field'),
            'value_field': ajax_config.get('value_field', 'id')
        })
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