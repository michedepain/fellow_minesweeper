const API_BASE_URL = 'http://localhost:8000/api'; //  Adjust as needed

export const createGame = async (width, height, mines) => {
    const response = await fetch(`${API_BASE_URL}/games/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ width, height, mines }),
    });
    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to create game');
    }
    return response.json();
};

export const getGame = async (gameId) => {
    const response = await fetch(`${API_BASE_URL}/games/${gameId}/`);
     if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to get game');
    }
    return response.json();
};

export const revealCell = async (gameId, row, col) => {
    const response = await fetch(`${API_BASE_URL}/games/${gameId}/reveal/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ row, col }),
    });
     if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to reveal cell');
    }
    return response.json();
};