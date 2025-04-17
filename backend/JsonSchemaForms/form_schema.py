class FormSchemaBuilder:
    """Builder class for dynamic form schemas."""
    
    def __init__(self, form_id, form_title):
        self.schema = {
            "form_id": form_id,
            "form_title": form_title,
            "shared_configs": {
                "ajax_configs": {}
            },
            "structure": []
        }
    
    def add_ajax_config(self, key, endpoint, method="GET", events=None, debounce=300):
        """Add an AJAX configuration to the schema."""
        if events is None:
            events = ["change", "blur"]
            
        self.schema["shared_configs"]["ajax_configs"][key] = {
            "endpoint": endpoint,
            "method": method,
            "triggerEvents": events,
            "debounceTime": debounce
        }
        return self
        
    def add_category(self, key, title, fields=None):
        """Add a category with fields to the form structure."""
        category = {
            "key": key,
            "title": title,
            "isCategory": True,
            "fields": fields or []
        }
        self.schema["structure"].append(category)
        return self
        
    def build(self):
        """Return the complete form schema."""
        return self.schema