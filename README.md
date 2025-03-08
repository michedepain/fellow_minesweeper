# 💣 Minesweeper Game 💣

A modern implementation of the classic Minesweeper game with a Django backend and React frontend.

![Minesweeper Game](https://img.shields.io/badge/Game-Minesweeper-brightgreen)
![Python](https://img.shields.io/badge/Backend-Django-blue)
![React](https://img.shields.io/badge/Frontend-React-61DAFB)

## 🎮 Game Features

- 🎲 Customizable board size and mine count
- ⏱️ Game timer to track your speed
- 🏆 Win detection
- 💥 Game over when hitting a mine
- 🔄 Auto-reveal of adjacent empty cells

## 📋 Table of Contents

- [Project Setup](#-project-setup)
  - [Backend Setup](#backend-setup)
  - [Frontend Setup](#frontend-setup)
- [Running the Project](#-running-the-project)
- [Running Tests](#-running-tests)
- [API Documentation](#-api-documentation)
- [Game Rules](#-game-rules)
- [Technologies Used](#-technologies-used)
- [Contributing](#-contributing)

## 🚀 Project Setup

### Prerequisites

- Python 3.8+
- Node.js 14+
- npm or yarn

### Backend Setup

1. **Clone the repository**

```bash
git clone https://github.com/michedepain/mineswipper.git
cd mineswipper
```

2. **Create and activate a virtual environment**

```bash
python -m venv django_env
# On Windows
django_env\Scripts\activate
# On macOS/Linux
source django_env/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Run migrations**

```bash
python manage.py makemigrations
python manage.py migrate
```

### Frontend Setup

1. **Navigate to the frontend directory**

```bash
cd minesweeper_frontend
```

2. **Install dependencies**

```bash
npm install
# or
yarn install
```

## 🏃‍♂️ Running the Project

### Start the Backend Server

```bash
# From the project root
python manage.py runserver
```

The backend will be available at http://localhost:8000/

### Start the Frontend Development Server

```bash
# From the minesweeper_frontend directory
npm start
# or
yarn start
```

The frontend will be available at http://localhost:3000/

## 🧪 Running Tests

The project includes comprehensive tests for both backend and frontend components. Here's how to run them:

### Backend Tests

```bash
# From the project root
python manage.py test
```

### Running Specific Backend Test Modules

```bash
# Test models only
python manage.py test minesweeper_backend.tests.test_models

# Test views only
python manage.py test minesweeper_backend.tests.test_views

# Test utility functions only
python manage.py test minesweeper_backend.tests.test_utils
```

### Running Specific Backend Test Classes

```bash
# Test only the Game model
python manage.py test minesweeper_backend.tests.test_models.GameModelTest

# Test only the create game view
python manage.py test minesweeper_backend.tests.test_views.CreateGameViewTest
```

### Running Individual Backend Tests

```bash
# Run a specific test method
python manage.py test minesweeper_backend.tests.test_models.GameModelTest.test_game_creation
```

### Frontend Tests

```bash
# From the minesweeper_frontend directory
npm test
```

### Running Frontend Tests in Different Modes

```bash
# Run tests in watch mode (default)
npm test

# Run tests once without watching
npm run test:ci

# Run tests with coverage report
npm run test:coverage

# Run a specific test file
npm test -- Cell.test.jsx

# Run tests matching a specific pattern
npm test -- GameBoard
```

### Backend Test Coverage

To generate a test coverage report for the backend, you can use the `coverage` tool:

```bash
# Install coverage if you haven't already
pip install coverage

# Run tests with coverage
coverage run --source='minesweeper_backend' manage.py test

# Generate a report
coverage report

# For a more detailed HTML report
coverage html
# Then open htmlcov/index.html in your browser
```

## 📡 API Documentation

### Game Endpoints

#### Create a New Game

- **URL**: `/api/games/`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "width": 10,
    "height": 10,
    "mines": 10
  }
  ```
- **Success Response**:
  - **Code**: 201 CREATED
  - **Content**:
    ```json
    {
      "game_id": "uuid-string",
      "width": 10,
      "height": 10,
      "mines": 10,
      "board_state": [["", "", ""], ["", "", ""], ...]
    }
    ```

#### Get Game State

- **URL**: `/api/games/:game_id/`
- **Method**: `GET`
- **Success Response**:
  - **Code**: 200 OK
  - **Content**:
    ```json
    {
      "game_id": "uuid-string",
      "width": 10,
      "height": 10,
      "mines": 10,
      "board_state": [["", "", ""], ["", "0", ""], ...],
      "game_over": false,
      "game_won": false,
      "elapsed_time": 45
    }
    ```

#### Reveal a Cell

- **URL**: `/api/games/:game_id/reveal/`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "row": 0,
    "col": 0
  }
  ```
- **Success Response**:
  - **Code**: 200 OK
  - **Content**:
    ```json
    {
      "message": "Cell revealed",
      "game_id": "uuid-string",
      "board_state": [["0", "", ""], ["", "", ""], ...],
      "game_over": false,
      "game_won": false,
      "elapsed_time": 50
    }
    ```
  - **Game Over Response**:
    ```json
    {
      "message": "Game Over! You hit a mine!",
      "game_id": "uuid-string",
      "board_state": [["M", "", ""], ["", "", ""], ...],
      "game_over": true,
      "game_won": false,
      "elapsed_time": 55
    }
    ```

## 📜 Game Rules

1. 🎯 The goal is to reveal all cells that don't contain mines.
2. 🔢 Numbers indicate how many mines are adjacent to that cell.
3. 💥 If you reveal a cell with a mine, the game is over.
4. 🏆 If you reveal all non-mine cells, you win!
5. 0️⃣ Revealing a cell with no adjacent mines automatically reveals adjacent cells.

## 🛠️ Technologies Used

### Backend
- Django
- Django REST Framework
- SQLite (development) / PostgreSQL (production)

### Frontend
- React
- React Router
- CSS for styling

Made with ❤️ by Michaël C.