# Patent Management System

## Description
Patent Management System: A web application for managing patent registrations, conducting patentability analysis, and interacting with an AI-powered chatbot for patent-related queries.

## Wireframe
![alt text](image.png)

+--------------------------------------------------+
| Header: Home | Register | Login | Chat | Analysis |
+--------------------------------------------------+
|                                                  |
|  +------------------+   +---------------------+  |
|  | Register Box     |   | Login Box           |  |
|  |------------------|   |---------------------|  |
|  | Username         |   | Username            |  |
|  | [TextField]      |   | [TextField]         |  |
|  | Password         |   | Password            |  |
|  | [TextField]      |   | [TextField]         |  |
|  | [Register Button]|   | [Login Button]      |  |
|  +------------------+   +---------------------+  |
|                                                  |
|  +--------------------------------------------+  |
|  | Conditional Rendering (if token exists)    |  |
|  |--------------------------------------------|  |
|  | Chat Component                             |  |
|  | PatentabilityAnalysis Component            |  |
|  | Patent Analysis Chart                      |  |
|  +--------------------------------------------+  |
|                                                  |
+--------------------------------------------------+
| Footer                                           |
+--------------------------------------------------+



## User Stories
1. **As a user, I want to register an account so that I can access the patent management system.**
2. **As a user, I want to log in to my account so that I can manage my patents.**
3. **As a user, I want to create a new patent entry so that I can keep track of my inventions.**
4. **As a user, I want to analyze the patentability of my invention idea so that I can determine its novelty, non-obviousness, and utility.**
5. **As a user, I want to chat with an AI-powered chatbot to get answers to my patent-related queries.**

## React Tree Diagram

## App Component
- **State**:
  - `username`
  - `password`
  - `token`
  - `user`
  - `loading`
- **Functions**:
  - `register`
  - `login`
- **Children**:
  - `Typography` (Patent Management)
  - `Box` (Register)
    - `Typography` (Register)
    - `TextField` (Username)
    - `TextField` (Password)
    - `Button` (Register)
  - `Box` (Login)
    - `Typography` (Login)
    - `TextField` (Username)
    - `TextField` (Password)
    - `Button` (Login)
  - Conditional Rendering (if `token` exists)
    - `Chat`
    - `PatentabilityAnalysis`
    - `Box` (Patent Analysis Chart)
      - `Typography` (Patent Analysis Chart)
      - `Line` (Chart)

## Chat Component
- **Props**:
  - `token`
- **State**:
  - `message`
  - `response`
  - `patents`
- **Functions**:
  - `sendMessage`
- **Children**:
  - `h2` (Chat with GPT)
  - `textarea` (Message Input)
  - `button` (Send)
  - `div` (Response)
    - `h3` (Response)
    - `p` (Response Text)
  - `div` (Related Patents)
    - `h3` (Related Patents)
    - `ul` (Patent List)
      - `li` (Patent Item)
        - `h4` (Patent Title)
        - `p` (Patent Abstract)

## PatentabilityAnalysis Component
- **Props**:
  - `token`
- **State**:
  - `idea`
  - `analysis`
- **Functions**:
  - `submitIdea`
- **Children**:
  - `h2` (Patentability Analysis)
  - `textarea` (Idea Input)
  - `button` (Submit)
  - `div` (Analysis)
    - `h3` (Analysis)
    - `p` (Novelty)
    - `p` (Non-obviousness)
    - `p` (Utility)
    - `h4` (Relevant Precedents)
    - `ul` (Precedent List)
      - `li` (Precedent Item)

## Other Components
- **index.js**
  - Renders `App` component
- **reportWebVitals.js**
  - Measures performance

## Schema Screenshot
!Schema Screenshot

![alt text](image-1.png)

## API Routes
| HTTP Verb | Endpoint                          | Purpose                                      |
|-----------|-----------------------------------|----------------------------------------------|
| POST      | /register                         | Register a new user                          |
| POST      | /login                            | Log in a user and return an access token     |
| POST      | /patents                          | Create a new patent (requires JWT)           |
| GET       | /patents                          | Retrieve all patents for the logged-in user (requires JWT) |
| PATCH     | /patents/<patent_id>              | Update an existing patent (requires JWT)     |
| POST      | /patentability_analysis           | Analyze the patentability of an invention idea (requires JWT) |
| PATCH     | /patentability_analysis/<analysis_id> | Update an existing patentability analysis (requires JWT) |
| POST      | /chat                             | Interact with the AI-powered chatbot (requires JWT) |

## Stretch Goals
1. **Implement user roles and permissions**: Allow different levels of access for users (e.g., admin, regular user).
2. **Add real-time notifications**: Notify users of important events, such as patent status updates.
3. **Integrate with external patent databases**: Automatically fetch and display relevant patent information from external sources.

## Kanban Board
!Kanban Board

## New Technologies
- **Material-UI**: For styling and UI components.
- **React Bootstrap**: For responsive design and additional UI components.
- **Tailwind CSS**: For utility-first CSS styling.
- **Deployment**: Plan to deploy the application using platforms like Heroku or AWS.
- **State Management**: Use React's `useContext` or Redux for state management.
