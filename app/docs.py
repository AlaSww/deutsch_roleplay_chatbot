from __future__ import annotations

from flask import Blueprint, jsonify, render_template_string, request


docs = Blueprint("docs", __name__)


def _server_url() -> str:
    return request.host_url.rstrip("/")


def _openapi_spec() -> dict:
    server_url = _server_url()
    return {
        "openapi": "3.0.3",
        "info": {
            "title": "German Scenario Backend API",
            "version": "1.0.0",
            "description": (
                "Flask backend for an AI-powered German roleplay application using PostgreSQL and Groq."
            ),
        },
        "servers": [{"url": server_url}],
        "tags": [
            {"name": "System"},
            {"name": "Auth"},
            {"name": "Users"},
            {"name": "Scenarios"},
            {"name": "Conversations"},
            {"name": "Feedback"},
        ],
        "components": {
            "securitySchemes": {
                "BearerAuth": {
                    "type": "http",
                    "scheme": "bearer",
                    "bearerFormat": "JWT",
                }
            },
            "schemas": {
                "HealthResponse": {
                    "type": "object",
                    "properties": {"status": {"type": "string", "example": "ok"}},
                },
                "ErrorResponse": {
                    "type": "object",
                    "properties": {"error": {"type": "string"}},
                    "required": ["error"],
                },
                "User": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string", "format": "uuid"},
                        "email": {"type": "string", "format": "email"},
                        "plan": {"type": "string", "enum": ["free", "premium"]},
                        "german_level": {"type": "string", "nullable": True},
                        "native_language": {"type": "string", "nullable": True},
                        "user_profile": {"$ref": "#/components/schemas/UserProfile"},
                        "created_at": {"type": "string", "format": "date-time"},
                    },
                },
                "UserProfile": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string", "format": "uuid", "nullable": True},
                        "user_id": {"type": "string", "format": "uuid", "nullable": True},
                        "common_mistakes": {
                            "type": "array",
                            "items": {},
                        },
                        "grammar_focus_areas": {
                            "type": "array",
                            "items": {},
                        },
                        "vocabulary_gaps": {
                            "type": "array",
                            "items": {},
                        },
                        "strengths": {
                            "type": "array",
                            "items": {},
                        },
                        "last_feedback_summary": {"type": "string", "nullable": True},
                        "created_at": {"type": "string", "format": "date-time", "nullable": True},
                        "updated_at": {"type": "string", "format": "date-time", "nullable": True},
                    },
                },
                "CreateUserRequest": {
                    "type": "object",
                    "properties": {
                        "email": {"type": "string", "format": "email"},
                        "password": {"type": "string", "format": "password"},
                        "plan": {"type": "string", "enum": ["free", "premium"]},
                        "german_level": {"type": "string", "example": "A2"},
                        "native_language": {"type": "string", "example": "English"},
                        "common_mistakes": {"type": "array", "items": {}},
                        "grammar_focus_areas": {"type": "array", "items": {}},
                        "vocabulary_gaps": {"type": "array", "items": {}},
                        "strengths": {"type": "array", "items": {}},
                        "last_feedback_summary": {"type": "string"},
                    },
                    "required": ["email", "password"],
                },
                "LoginRequest": {
                    "type": "object",
                    "properties": {
                        "email": {"type": "string", "format": "email"},
                        "password": {"type": "string", "format": "password"},
                    },
                    "required": ["email", "password"],
                },
                "AuthResponse": {
                    "type": "object",
                    "properties": {
                        "access_token": {"type": "string"},
                        "user": {"$ref": "#/components/schemas/User"},
                    },
                    "required": ["access_token", "user"],
                },
                "ScenarioRole": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string", "format": "uuid"},
                        "scenario_id": {"type": "string", "format": "uuid"},
                        "role_name": {"type": "string"},
                        "prompt_context": {"type": "string"},
                        "created_at": {"type": "string", "format": "date-time"},
                    },
                },
                "Scenario": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string", "format": "uuid"},
                        "name": {"type": "string"},
                        "description": {"type": "string", "nullable": True},
                        "prompt_context": {"type": "string"},
                        "is_premium": {"type": "boolean"},
                        "created_at": {"type": "string", "format": "date-time"},
                        "roles": {
                            "type": "array",
                            "items": {"$ref": "#/components/schemas/ScenarioRole"},
                        },
                    },
                },
                "Message": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string", "format": "uuid"},
                        "conversation_id": {"type": "string", "format": "uuid"},
                        "sender": {"type": "string", "enum": ["user", "assistant"]},
                        "message_type": {"type": "string"},
                        "content": {"type": "string"},
                        "transcript": {"type": "string", "nullable": True},
                        "audio_url": {"type": "string", "nullable": True},
                        "created_at": {"type": "string", "format": "date-time"},
                    },
                },
                "ConversationListItem": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string", "format": "uuid"},
                        "user_id": {"type": "string", "format": "uuid"},
                        "scenario_id": {"type": "string", "format": "uuid"},
                        "scenario_role_id": {"type": "string", "format": "uuid"},
                        "status": {"type": "string"},
                        "started_at": {"type": "string", "format": "date-time"},
                        "ended_at": {"type": "string", "format": "date-time", "nullable": True},
                        "scenario_name": {"type": "string"},
                        "user_role_name": {"type": "string"},
                        "ai_role_name": {"type": "string", "nullable": True},
                    },
                },
                "ConversationDetail": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string", "format": "uuid"},
                        "user_id": {"type": "string", "format": "uuid"},
                        "scenario_id": {"type": "string", "format": "uuid"},
                        "scenario_role_id": {"type": "string", "format": "uuid"},
                        "status": {"type": "string"},
                        "started_at": {"type": "string", "format": "date-time"},
                        "ended_at": {"type": "string", "format": "date-time", "nullable": True},
                        "email": {"type": "string", "format": "email"},
                        "user_plan": {"type": "string"},
                        "german_level": {"type": "string", "nullable": True},
                        "native_language": {"type": "string", "nullable": True},
                        "user_profile": {"$ref": "#/components/schemas/UserProfile"},
                        "scenario_name": {"type": "string"},
                        "scenario_description": {"type": "string", "nullable": True},
                        "scenario_prompt_context": {"type": "string"},
                        "is_premium": {"type": "boolean"},
                        "user_role_name": {"type": "string", "nullable": True},
                        "user_role_prompt_context": {"type": "string", "nullable": True},
                        "ai_role_name": {"type": "string", "nullable": True},
                        "ai_role_prompt_context": {"type": "string", "nullable": True},
                        "user_role": {
                            "oneOf": [
                                {"type": "null"},
                                {"$ref": "#/components/schemas/ScenarioRole"},
                            ]
                        },
                        "ai_role": {
                            "oneOf": [
                                {"type": "null"},
                                {"$ref": "#/components/schemas/ScenarioRole"},
                            ]
                        },
                        "conversation_summary": {"type": "string", "nullable": True},
                        "summary_updated_at": {
                            "type": "string",
                            "format": "date-time",
                            "nullable": True,
                        },
                        "messages": {
                            "type": "array",
                            "items": {"$ref": "#/components/schemas/Message"},
                        },
                        "feedback": {
                            "oneOf": [
                                {"type": "null"},
                                {"$ref": "#/components/schemas/FeedbackSession"},
                            ]
                        },
                        "opening_message_error": {"type": "string"},
                    },
                },
                "CreateConversationRequest": {
                    "type": "object",
                    "properties": {
                        "scenario_id": {"type": "string", "format": "uuid"},
                        "scenario_role_id": {
                            "type": "string",
                            "format": "uuid",
                            "description": "The role chosen by the user. The AI will play the other role in the scenario.",
                        },
                        "generate_opening_message": {"type": "boolean"},
                    },
                    "required": ["scenario_id", "scenario_role_id"],
                },
                "CreateMessageRequest": {
                    "type": "object",
                    "properties": {"content": {"type": "string"}},
                    "required": ["content"],
                },
                "ConversationTurnResponse": {
                    "type": "object",
                    "properties": {
                        "user_message": {"$ref": "#/components/schemas/Message"},
                        "assistant_message": {"$ref": "#/components/schemas/Message"},
                    },
                },
                "Mistake": {
                    "type": "object",
                    "properties": {
                        "span": {"type": "string"},
                        "issue": {"type": "string"},
                        "category": {"type": "string"},
                    },
                },
                "MessageFeedback": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string", "format": "uuid"},
                        "feedback_session_id": {"type": "string", "format": "uuid"},
                        "message_id": {"type": "string", "format": "uuid"},
                        "original_text": {"type": "string"},
                        "corrected_text": {"type": "string"},
                        "mistakes": {
                            "type": "array",
                            "items": {"$ref": "#/components/schemas/Mistake"},
                        },
                        "better_alternatives": {
                            "type": "array",
                            "items": {"type": "string"},
                        },
                        "explanations": {
                            "type": "array",
                            "items": {"type": "string"},
                        },
                        "created_at": {"type": "string", "format": "date-time"},
                    },
                },
                "FeedbackSession": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string", "format": "uuid"},
                        "conversation_id": {"type": "string", "format": "uuid"},
                        "overall_feedback": {"type": "string", "nullable": True},
                        "created_at": {"type": "string", "format": "date-time"},
                        "message_feedback": {
                            "type": "array",
                            "items": {"$ref": "#/components/schemas/MessageFeedback"},
                        },
                    },
                },
                "SingleMessageFeedbackResponse": {
                    "type": "object",
                    "properties": {
                        "feedback_session_id": {"type": "string", "format": "uuid"},
                        "feedback_summary": {"type": "string"},
                        "message_feedback": {"$ref": "#/components/schemas/MessageFeedback"},
                    },
                },
                "CompleteConversationResponse": {
                    "type": "object",
                    "properties": {
                        "feedback_session": {"$ref": "#/components/schemas/FeedbackSession"},
                        "message_feedback": {
                            "type": "array",
                            "items": {"$ref": "#/components/schemas/MessageFeedback"},
                        },
                    },
                },
            }
        },
        "paths": {
            "/": {
                "get": {
                    "tags": ["System"],
                    "summary": "Service root",
                    "responses": {
                        "200": {
                            "description": "Basic service metadata",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "service": {"type": "string"},
                                            "status": {"type": "string"},
                                            "docs": {"type": "string"},
                                        },
                                    }
                                }
                            },
                        }
                    },
                }
            },
            "/api/health": {
                "get": {
                    "tags": ["System"],
                    "summary": "Health check",
                    "responses": {
                        "200": {
                            "description": "API is healthy",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/HealthResponse"}
                                }
                            },
                        }
                    },
                }
            },
            "/api/auth/register": {
                "post": {
                    "tags": ["Auth"],
                    "summary": "Register a new user and return a JWT",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/CreateUserRequest"}
                            }
                        },
                    },
                    "responses": {
                        "201": {
                            "description": "User registered",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/AuthResponse"}
                                }
                            },
                        },
                        "400": {"description": "Invalid request"},
                        "409": {"description": "Email already exists"},
                    },
                }
            },
            "/api/auth/login": {
                "post": {
                    "tags": ["Auth"],
                    "summary": "Log in and return a JWT",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/LoginRequest"}
                            }
                        },
                    },
                    "responses": {
                        "200": {
                            "description": "Login successful",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/AuthResponse"}
                                }
                            },
                        },
                        "400": {"description": "Invalid request"},
                        "401": {"description": "Invalid credentials"},
                    },
                }
            },
            "/api/auth/me": {
                "get": {
                    "tags": ["Auth"],
                    "summary": "Get the current authenticated user",
                    "security": [{"BearerAuth": []}],
                    "responses": {
                        "200": {
                            "description": "Current user",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/User"}
                                }
                            },
                        },
                        "401": {"description": "Missing or invalid token"},
                    },
                }
            },
            "/api/users": {
                "get": {
                    "tags": ["Users"],
                    "summary": "Get the authenticated user",
                    "security": [{"BearerAuth": []}],
                    "responses": {
                        "200": {
                            "description": "Current user wrapped in an array for backward compatibility",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "array",
                                        "items": {"$ref": "#/components/schemas/User"},
                                    }
                                }
                            },
                        },
                        "401": {"description": "Missing or invalid token"},
                    },
                },
            },
            "/api/scenarios": {
                "get": {
                    "tags": ["Scenarios"],
                    "summary": "List scenarios with their roles",
                    "responses": {
                        "200": {
                            "description": "List of scenarios",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "array",
                                        "items": {"$ref": "#/components/schemas/Scenario"},
                                    }
                                }
                            },
                        }
                    },
                }
            },
            "/api/scenarios/{scenario_id}": {
                "get": {
                    "tags": ["Scenarios"],
                    "summary": "Get one scenario",
                    "parameters": [
                        {
                            "name": "scenario_id",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "string", "format": "uuid"},
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Scenario detail",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/Scenario"}
                                }
                            },
                        },
                        "400": {"description": "Invalid UUID"},
                        "404": {"description": "Scenario not found"},
                    },
                }
            },
            "/api/conversations": {
                "get": {
                    "tags": ["Conversations"],
                    "summary": "List conversations",
                    "security": [{"BearerAuth": []}],
                    "responses": {
                        "200": {
                            "description": "List of conversations",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "array",
                                        "items": {
                                            "$ref": "#/components/schemas/ConversationListItem"
                                        },
                                    }
                                }
                            },
                        },
                        "401": {"description": "Missing or invalid token"},
                    },
                },
                "post": {
                    "tags": ["Conversations"],
                    "summary": "Create a conversation and optionally generate the opening AI message",
                    "security": [{"BearerAuth": []}],
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/CreateConversationRequest"
                                }
                            }
                        },
                    },
                    "responses": {
                        "201": {
                            "description": "Conversation created",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/ConversationDetail"
                                    }
                                }
                            },
                        },
                        "400": {"description": "Invalid request"},
                        "401": {"description": "Missing or invalid token"},
                        "404": {"description": "Scenario or role not found"},
                    },
                },
            },
            "/api/conversations/{conversation_id}": {
                "get": {
                    "tags": ["Conversations"],
                    "summary": "Get one conversation with messages and feedback",
                    "security": [{"BearerAuth": []}],
                    "parameters": [
                        {
                            "name": "conversation_id",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "string", "format": "uuid"},
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Conversation detail",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/ConversationDetail"
                                    }
                                }
                            },
                        },
                        "400": {"description": "Invalid UUID"},
                        "401": {"description": "Missing or invalid token"},
                        "403": {"description": "Not allowed"},
                        "404": {"description": "Conversation not found"},
                    },
                }
            },
            "/api/conversations/{conversation_id}/messages": {
                "post": {
                    "tags": ["Conversations"],
                    "summary": "Send a user message and generate the AI reply",
                    "security": [{"BearerAuth": []}],
                    "parameters": [
                        {
                            "name": "conversation_id",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "string", "format": "uuid"},
                        }
                    ],
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/CreateMessageRequest"
                                }
                            }
                        },
                    },
                    "responses": {
                        "201": {
                            "description": "Turn created",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/ConversationTurnResponse"
                                    }
                                }
                            },
                        },
                        "400": {"description": "Invalid request"},
                        "401": {"description": "Missing or invalid token"},
                        "403": {"description": "Not allowed"},
                        "404": {"description": "Conversation not found"},
                        "502": {"description": "Groq call failed"},
                    },
                }
            },
            "/api/conversations/{conversation_id}/messages/{message_id}/feedback": {
                "post": {
                    "tags": ["Feedback"],
                    "summary": "Generate feedback for one user message during the conversation",
                    "security": [{"BearerAuth": []}],
                    "parameters": [
                        {
                            "name": "conversation_id",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "string", "format": "uuid"},
                        },
                        {
                            "name": "message_id",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "string", "format": "uuid"},
                        },
                    ],
                    "responses": {
                        "200": {
                            "description": "Single-message feedback generated",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/SingleMessageFeedbackResponse"
                                    }
                                }
                            },
                        },
                        "400": {"description": "Invalid request"},
                        "401": {"description": "Missing or invalid token"},
                        "403": {"description": "Not allowed"},
                        "404": {"description": "Conversation or message not found"},
                        "502": {"description": "Groq call failed"},
                    },
                }
            },
            "/api/conversations/{conversation_id}/feedback": {
                "get": {
                    "tags": ["Feedback"],
                    "summary": "Get the stored feedback for a conversation",
                    "security": [{"BearerAuth": []}],
                    "parameters": [
                        {
                            "name": "conversation_id",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "string", "format": "uuid"},
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Feedback session",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/FeedbackSession"
                                    }
                                }
                            },
                        },
                        "400": {"description": "Invalid UUID"},
                        "401": {"description": "Missing or invalid token"},
                        "403": {"description": "Not allowed"},
                        "404": {"description": "No feedback yet"},
                    },
                }
            },
            "/api/conversations/{conversation_id}/complete": {
                "post": {
                    "tags": ["Feedback"],
                    "summary": "Complete the conversation and generate final feedback",
                    "security": [{"BearerAuth": []}],
                    "parameters": [
                        {
                            "name": "conversation_id",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "string", "format": "uuid"},
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Conversation completed with feedback",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/CompleteConversationResponse"
                                    }
                                }
                            },
                        },
                        "400": {"description": "Invalid request"},
                        "401": {"description": "Missing or invalid token"},
                        "403": {"description": "Not allowed"},
                        "404": {"description": "Conversation not found"},
                        "502": {"description": "Groq call failed"},
                    },
                }
            },
        },
    }


@docs.get("/openapi.json")
def openapi_json():
    return jsonify(_openapi_spec())


@docs.get("/docs")
def swagger_ui():
    return render_template_string(
        """
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>German Scenario API Docs</title>
    <link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css" />
    <style>
      body { margin: 0; background: #f6f7fb; }
      .topbar { display: none; }
    </style>
  </head>
  <body>
    <div id="swagger-ui"></div>
    <script src="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
    <script>
      window.ui = SwaggerUIBundle({
        url: "{{ spec_url }}",
        dom_id: "#swagger-ui",
        deepLinking: true,
        presets: [SwaggerUIBundle.presets.apis],
        layout: "BaseLayout"
      });
    </script>
  </body>
</html>
        """,
        spec_url="/openapi.json",
    )
