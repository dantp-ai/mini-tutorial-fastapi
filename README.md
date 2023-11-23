# FastAPI Mini Tutorial

Welcome to this mini tutorial on using FastAPI to create an API for managing multiple-choice questions and quizzes. FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.6+.

## Getting Started

Before you begin, make sure you have Python 3.6 or higher installed on your system. You can check your Python version by running:

```bash
python --version
```

Install all the dependencies including FastAPI and pandas using the pip:

```bash
pip install -r requirements.txt
```

## Overview

This FastAPI project allows users to access and manage multiple-choice questions (MCQs). It includes features like basic authentication, Pydantic models for data validation, error handling, and more.

### Basic Authentication

The API uses Basic Authentication for user authentication. There are three predefined users with their usernames and passwords stored in the `users_db` dictionary.

To access authenticated routes, you need to include an `Authorization` header with the value in the format `Basic username:password`. For example:

```bash
curl -X GET "http://localhost:8000/questions" -H "Authorization: Basic YXVyZWxpYTpBdWd1c3RpbmE="
```

### Pydantic Models

The code uses Pydantic models for data validation and serialization. There are two main Pydantic models:

1. `Question`: Represents a multiple-choice question with various fields such as `question`, `subject`, `use`, `correct`, and more.

2. `ResponseQuestionCreate`: Represents the response when creating a new question. It includes the `question` and additional metadata like `id` and `created_at`.

### Error Handling

FastAPI makes error handling straightforward. If something goes wrong, it raises appropriate HTTP exceptions with status codes and detailed error messages. For example, if you provide incorrect credentials or an invalid request, you'll receive an error response.

## Endpoints

Here are the main endpoints of the API:

1. **GET /questions**: Retrieve a random set of multiple-choice questions.

   - Parameters:
     - `test_type` (query, required): Choose a test type.
     - `categories` (query, required): Choose one or more categories.
     - `num_items` (query, required): How many questions to get (options: 5, 10, 20).

   Example:

   ```bash
   curl -X GET "http://localhost:8000/questions?test_type=sample&categories=math&num_items=10" -H "Authorization: Basic YXVyZWxpYTpBdWd1c3RpbmE="
   ```

2. **POST /question**: Create a new question (requires admin authentication).

   - Body:
     - `question` (JSON, required): A JSON object representing a new question.

   Example:

   ```bash
   curl -X POST "http://localhost:8000/question" -H "Authorization: Basic YWRtaW46YWRtaW4=" -H "Content-Type: application/json" -d '{
       "question": {
           "question": "What is the capital of France?",
           "subject": ["Geography"],
           "use": ["Test"],
           "responseA": "London",
           "responseB": "Berlin",
           "responseC": "Paris",
           "responseD": "Madrid",
           "correct": ["C"],
           "remark": "This is an easy one."
       }
   }'
   ```

## Running the Application

To run the FastAPI application, you can execute the following command in the same directory as your code:

```bash
uvicorn main:app --reload
```

This will start the application, and you can access it at `http://localhost:8000` in your web browser or using tools like `curl` or Postman.

## Documentation of API in FastAPI

FastAPI provides automatic generation of API documentation using tools like Swagger UI and ReDoc. Here's how it works:

- The code includes docstrings and type hints in the endpoint functions, query parameters, and request bodies. For example, the `get_questions` endpoint includes docstrings explaining the purpose and usage of the endpoint, and it uses type hints for parameters.

- FastAPI's built-in interactive documentation is automatically generated based on these docstrings and type hints. You can access it by visiting the `/docs` endpoint when your application is running. For example, if your app is running locally, you can access it at `http://localhost:8000/docs`.

- The generated documentation provides detailed information about each endpoint, including the available query parameters, request body structure, and expected responses. It also allows users to test the endpoints directly from the documentation.

- Additionally, FastAPI supports the OpenAPI standard, making it easy to export your API documentation in various formats for sharing with others.

By following these practices and using FastAPI's built-in features, you can create well-documented and robust APIs with minimal effort.


## Conclusion

This mini tutorial provides an introduction to using FastAPI for building a simple API to manage multiple-choice questions.