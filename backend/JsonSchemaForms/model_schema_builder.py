from django.db.models import Model, Field
from django.forms.models import fields_for_model
from django.core.exceptions import FieldDoesNotExist
from JsonSchemaForms.form_schema import FormSchemaBuilder

class ModelFormSchemaBuilder(FormSchemaBuilder):
    """Builder class for form schemas based on Django models."""

    def __init__(self, model_class, form_id=None, form_title=None, *args, **kwargs):
        """Initialize with a Django model class."""
        self.model_class = model_class
        model_name = model_class.__name__

        # Use model name as defaults if not provided
        super().__init__(
            form_id=form_id or f"{model_name.lower()}_form",
            form_title=form_title or f"{model_name} Form"
        )

        # Store field information from the model
        self.model_fields = {}
        self._extract_model_fields()

    def _extract_model_fields(self):
        """Extract field metadata from the model."""
        form_fields = fields_for_model(self.model_class)

        for field_name, form_field in form_fields.items():
            try:
                model_field = self.model_class._meta.get_field(field_name)

                # Extract field metadata
                self.model_fields[field_name] = {
                    "key": field_name,
                    "label": model_field.verbose_name or field_name.replace('_', ' ').title(),
                    "help_text": model_field.help_text or "",
                    "required": not model_field.blank,
                    "field_type": self._get_field_type(model_field),
                    "choices": self._get_field_choices(model_field),
                }
            except FieldDoesNotExist:
                continue

    def _get_field_type(self, field):
        """Convert Django field type to form field type."""
        field_class = field.__class__.__name__
        field_type_map = {
            models.CharField: 'text',
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

    def _get_field_choices(self, field):
        """Extract choices from field if available."""
        if hasattr(field, 'choices') and field.choices:
            return [{"value": key, "label": label} for key, label in field.choices]
        return None

    def configure_from_dict(self, config):
        """Configure the form schema from a dictionary."""
        # Apply any ajax configs
        if 'ajax_configs' in config:
            for key, cfg in config['ajax_configs'].items():
                self.add_ajax_config(
                    key,
                    cfg['endpoint'],
                    method=cfg.get('method', 'GET'),
                    events=cfg.get('events'),
                    debounce=cfg.get('debounce', 300)
                )

        # Handle field-to-category mapping if provided
        if 'field_categories' in config:
            # First, organize categories
            categories = {}
            for field_name, category_key in config['field_categories'].items():
                if category_key not in categories:
                    # Find category details from categories list or use defaults
                    cat_details = next((c for c in config.get('categories', [])
                                      if c.get('key') == category_key),
                                     {'title': category_key.replace('_', ' ').title()})

                    categories[category_key] = {
                        'key': category_key,
                        'title': cat_details.get('title'),
                        'fields': []
                    }

                # Add field to this category
                if field_name in self.model_fields:
                    categories[category_key]['fields'].append(field_name)

            # Now process each category
            for cat_key, cat_data in categories.items():
                field_configs = []

                for field_name in cat_data['fields']:
                    field_info = self.model_fields[field_name].copy()

                    # Apply overrides if any
                    if 'field_overrides' in config and field_name in config['field_overrides']:
                        field_info.update(config['field_overrides'][field_name])

                    field_configs.append(field_info)

                self.add_category(cat_key, cat_data['title'], field_configs)

        # Original categories handling
        elif 'categories' in config:
            for cat in config['categories']:
                field_configs = []

                for field_name in cat.get('fields', []):
                    if field_name in self.model_fields:
                        field_info = self.model_fields[field_name].copy()

                        if 'field_overrides' in config and field_name in config['field_overrides']:
                            field_info.update(config['field_overrides'][field_name])

                        field_configs.append(field_info)

                self.add_category(cat['key'], cat['title'], field_configs)

        return self