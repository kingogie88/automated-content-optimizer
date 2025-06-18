from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from typing import Dict, List, Optional

def custom_openapi(app: FastAPI) -> Dict:
    """Generate custom OpenAPI documentation"""
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="GEO AI Optimizer API",
        version="1.0.0",
        description="""
        API for the GEO AI Optimizer tool that optimizes content for AI assistants and search engines.
        
        Features:
        - Content optimization for AI assistants
        - Entity extraction and linking
        - Schema generation
        - Multi-platform content distribution
        """,
        routes=app.routes,
    )

    # Add security schemes
    openapi_schema["components"]["securitySchemes"] = {
        "ApiKeyAuth": {
            "type": "apiKey",
            "in": "header",
            "name": "X-API-Key"
        }
    }

    # Add global security requirement
    openapi_schema["security"] = [{"ApiKeyAuth": []}]

    # Add response examples
    openapi_schema["components"]["examples"] = {
        "EntityExtraction": {
            "value": {
                "entities": [
                    {
                        "text": "Apple Inc.",
                        "label": "ORG",
                        "start": 0,
                        "end": 9
                    }
                ]
            }
        },
        "SchemaGeneration": {
            "value": {
                "@context": "https://schema.org",
                "@type": "FAQPage",
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": "What is GEO?",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": "GEO is a technique for optimizing content."
                        }
                    }
                ]
            }
        }
    }

    # Add tags
    openapi_schema["tags"] = [
        {
            "name": "Content Optimization",
            "description": "Endpoints for content optimization and analysis"
        },
        {
            "name": "Entity Extraction",
            "description": "Endpoints for entity extraction and knowledge graph generation"
        },
        {
            "name": "Schema Generation",
            "description": "Endpoints for generating and validating structured data"
        },
        {
            "name": "Distribution",
            "description": "Endpoints for content distribution to various platforms"
        }
    ]

    app.openapi_schema = openapi_schema
    return app.openapi_schema

def add_api_documentation(app: FastAPI) -> None:
    """Add API documentation to FastAPI app"""
    from fastapi.openapi.docs import get_swagger_ui_html
    from fastapi.openapi.docs import get_redoc_html
    from fastapi.staticfiles import StaticFiles
    
    # Set custom OpenAPI schema
    app.openapi = lambda: custom_openapi(app)
    
    # Add Swagger UI
    @app.get("/docs", include_in_schema=False)
    async def custom_swagger_ui_html():
        return get_swagger_ui_html(
            openapi_url=app.openapi_url,
            title=app.title + " - Swagger UI",
            oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
            swagger_js_url="/static/swagger-ui-bundle.js",
            swagger_css_url="/static/swagger-ui.css",
        )
    
    # Add ReDoc
    @app.get("/redoc", include_in_schema=False)
    async def redoc_html():
        return get_redoc_html(
            openapi_url=app.openapi_url,
            title=app.title + " - ReDoc",
            redoc_js_url="/static/redoc.standalone.js",
        )
    
    # Mount static files
    app.mount("/static", StaticFiles(directory="static"), name="static") 