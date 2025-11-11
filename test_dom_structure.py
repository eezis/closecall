#!/usr/bin/env python3
"""
Test script to analyze the DOM structure of the incident form
"""
import os
import sys
import django
from django.template import Template, Context
from django.template.loader import render_to_string

# Setup Django
sys.path.append('/home/eezis/code/closecall')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'closecall.settings')
django.setup()

from incident.forms import CreateIncidentForm

def analyze_form_rendering():
    """Analyze how crispy forms renders the latitude/longitude fields"""

    # Create a form instance
    form = CreateIncidentForm()

    # Print field information
    print("=== FORM FIELD ANALYSIS ===")
    for field_name, field in form.fields.items():
        if field_name in ['latitude', 'longitude']:
            print(f"\nField: {field_name}")
            print(f"  Widget: {field.widget.__class__.__name__}")
            print(f"  Widget attrs: {field.widget.attrs}")
            print(f"  Required: {field.required}")
            print(f"  Label: {field.label}")

    # Test rendering with crispy forms
    print("\n=== CRISPY FORMS RENDERING ===")

    # Create a minimal template to test crispy rendering
    template_content = """
    {% load crispy_forms_tags %}
    <form>
        {{ form|crispy }}
    </form>
    """

    template = Template(template_content)
    context = Context({'form': form})
    rendered_html = template.render(context)

    # Look for latitude/longitude field HTML
    lines = rendered_html.split('\n')
    lat_lines = []
    lng_lines = []
    capture_lat = False
    capture_lng = False

    for i, line in enumerate(lines):
        # Look for latitude field
        if 'name="latitude"' in line:
            lat_lines.append(f"Line {i}: {line.strip()}")
            # Capture surrounding context
            for j in range(max(0, i-3), min(len(lines), i+4)):
                if j != i:
                    lat_lines.append(f"Context {j}: {lines[j].strip()}")

        # Look for longitude field
        if 'name="longitude"' in line:
            lng_lines.append(f"Line {i}: {line.strip()}")
            # Capture surrounding context
            for j in range(max(0, i-3), min(len(lines), i+4)):
                if j != i:
                    lng_lines.append(f"Context {j}: {lines[j].strip()}")

    print("Latitude field HTML:")
    for line in lat_lines[:10]:  # Limit output
        print(f"  {line}")

    print("\nLongitude field HTML:")
    for line in lng_lines[:10]:  # Limit output
        print(f"  {line}")

    # Look for any div/wrapper structures
    print("\n=== DIV STRUCTURE ANALYSIS ===")
    div_count = 0
    for i, line in enumerate(lines):
        if '<div' in line and ('latitude' in line or 'longitude' in line or 'control-group' in line or 'form-group' in line):
            print(f"Line {i}: {line.strip()}")
            div_count += 1
            if div_count > 5:  # Limit output
                break

if __name__ == "__main__":
    analyze_form_rendering()