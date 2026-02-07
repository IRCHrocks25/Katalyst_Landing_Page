from django.shortcuts import render
from django.http import JsonResponse
import os

def home(request):
    return render(request, 'myApp/home_v2.html')

def parse_node_file(node_id):
    """Parse a journey node template file and return node data"""
    try:
        from django.conf import settings
        import os
        
        # Build path to template file
        template_path = os.path.join(
            settings.BASE_DIR,
            'myApp',
            'templates',
            'myApp',
            'new_partial',
            'journey_nodes',
            f'{node_id}.html'
        )
        
        if not os.path.exists(template_path):
            print(f"Node file not found: {template_path}")
            return None
        
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        node = {"kind": "statement"}  # default
        choices = []
        in_body = False
        body_lines = []
        
        lines = content.split('\n')
        for i, line in enumerate(lines):
            line = line.strip()
            if not line or line.startswith('<!--'):
                continue
            
            if line.startswith('kind:'):
                node['kind'] = line.split(':', 1)[1].strip()
                in_body = False
            elif line.startswith('design:'):
                node['design'] = line.split(':', 1)[1].strip()
                in_body = False
            elif line.startswith('eyebrow:'):
                node['eyebrow'] = line.split(':', 1)[1].strip()
                in_body = False
            elif line.startswith('icon:'):
                node['icon'] = line.split(':', 1)[1].strip()
                in_body = False
            elif line.startswith('title:'):
                node['title'] = line.split(':', 1)[1].strip()
                in_body = False
            elif line.startswith('subtitle:'):
                node['subtitle'] = line.split(':', 1)[1].strip()
                in_body = False
            elif line.startswith('body:'):
                body_lines = [line.split(':', 1)[1].strip()]
                in_body = True
            elif line.startswith('choice:'):
                in_body = False
                choice_parts = line.split(':', 1)[1].strip()
                if '|' in choice_parts:
                    label, target = choice_parts.split('|', 1)
                    choices.append({"label": label.strip(), "to": target.strip()})
            elif in_body and line:
                # Continue collecting body text
                body_lines.append(line)
        
        if body_lines:
            node['body'] = ' '.join(body_lines)
        
        if choices:
            node['choices'] = choices
        
        return node
    except Exception as e:
        print(f"Error parsing node {node_id}: {e}")
        import traceback
        traceback.print_exc()
        return None

def journey_config(request):
    """API endpoint that loads journey nodes from individual template files"""
    
    # List of all journey node IDs
    node_ids = [
        "home_hero",
        "intro_problem",
        "engine_overview",
        "business_engine_hero",
        "business_engine_problem",
        "business_engine_module_a",
        "business_engine_module_b",
        "business_engine_module_c",
        "business_engine_module_d",
        "business_engine_module_e",
        "business_engine_at_glance",
        "business_engine_guarantee",
        "marketing_engine_hero",
        "marketing_engine_problem",
        "marketing_social",
        "marketing_video",
        "marketing_ads",
        "marketing_content",
        "marketing_comparison",
        "visibility_hero",
        "visibility_problem",
        "visibility_layer1",
        "visibility_layer2",
        "visibility_layer3",
        "visibility_methodology",
        "knowledge_scale",
        "dfy_hero",
        "dfy_service1",
        "dfy_service2",
        "dfy_service3",
        "dfy_service4",
        "dfy_process",
        "trust_validation",
        "impact_metrics",
        "testimonials",
        "risk_mitigation",
        "promise",
        "about_hero",
        "leadership",
        "philosophy",
        "track_record",
        "final_cta",
        "contact",
        "contact_form"
    ]
    
    # Load all nodes from template files
    nodes = {}
    for node_id in node_ids:
        node = parse_node_file(node_id)
        if node:
            nodes[node_id] = node
    
    JOURNEY = {
        "start": "home_hero",
        "nodes": nodes
    }
    
    return JsonResponse(JOURNEY)
