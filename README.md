# 💣 Minesweeper Game 💣

An implementation of the classic Minesweeper game with a Django backend and React frontend.

![Minesweeper Game](https://img.shields.io/badge/Game-Minesweeper-brightgreen)
![Python](https://img.shields.io/badge/Backend-Django-blue)
![React](https://img.shields.io/badge/Frontend-React-61DAFB)


[Demo](https://screenshot.click/09-18-3zupg-gasx2.mp4)

## 🎮 Game Features

- 🎲 Customizable board size and mine count
- ⏱️ Game timer to track your speed
- 🏆 Win detection
- 💥 Game over when hitting a mine
- 🔄 Auto-reveal of adjacent empty cells

## 📜 Game Rules

1. 🎯 The goal is to reveal all cells that don't contain mines.
2. 🔢 Numbers indicate how many mines are adjacent to that cell.
3. 💥 If you reveal a cell with a mine, the game is over.
4. 🏆 If you reveal all non-mine cells, you win!
5. 0️⃣ Revealing a cell with no adjacent mines automatically reveals adjacent cells.

## 📋 Table of Contents

- [Project Setup](#-project-setup)
  - [Backend Setup](#backend-setup)
  - [Frontend Setup](#frontend-setup)
- [Running the Project](#-running-the-project)
- [Running Tests](#-running-tests)
- [API Documentation](#-api-documentation)
- [Technologies Used](#-technologies-used)

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
# On macOS/Linux
source django_env/bin/activate
```

3. **Run migrations**

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
python3 manage.py runserver
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
python3 manage.py test
```

### Running Specific Backend Test Modules

```bash
# Test models only
python3 manage.py test minesweeper_backend.tests.test_models

# Test views only
python3 manage.py test minesweeper_backend.tests.test_views

# Test utility functions only
python3 manage.py test minesweeper_backend.tests.test_utils
```

### Frontend Tests

```bash
# From the minesweeper_frontend directory
npm test
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

## Behind the scene

The Stack-Based Flood Fill Algorithm is used to reveal cells.
This algorithm "is an algorithm mainly used to determine a bounded area connected to a given node in a multi-dimensional array." ([source](https://www.freecodecamp.org/news/flood-fill-algorithm-explained/))

Here is a visual representation of the algorithm:

Internal board (M = mine, numbers would be calculated):

```
[ ,  ,  ]
[ , M,  ]
[ ,  ,  ]
```

Initial player board (all hidden):

```
[ ,  ,  ]
[ ,  ,  ]
[ ,  ,  ]
```

If the player clicks on the top-left cell (0,0):
- We add (0,0) to the stack: stack = [(0,0)]
- We pop (0,0), mark it as visited, and reveal it as '1' (it has one adjacent mine)
- Since it's not an empty cell (mine_count = 1), we don't add any neighbors to the stack
The stack is now empty, so we're done.

Final player board:

```
[1,  ,  ]
[ ,  ,  ]
[ ,  ,  ]
```

Now, if the player clicks on the bottom-left cell (2,0), which has no adjacent mines:

- We add (2,0) to the stack: stack = [(2,0)]
- We pop (2,0), mark it as visited, and reveal it as '0'
- Since it's an empty cell, we add its unvisited neighbors: stack = [(1,0), (2,1)]
- We pop (2,1), mark it as visited, and reveal it as '1'
- Since it's not an empty cell, we don't add any neighbors: stack = [(1,0)]
- We continue this process until the stack is empty

Final player board:

```
[1,  1, ]
[1 , M, ]
[0, 1, 1]
```



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