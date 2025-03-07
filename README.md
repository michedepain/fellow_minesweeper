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

## 👥 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

Made with ❤️ by Michaël C.