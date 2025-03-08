const API_BASE_URL = 'http://localhost:8000/api';

export const createGame = async (width, height, mines) => {
    console.log(`API call: Creating game with width=${width}, height=${height}, mines=${mines}`);
    try {
        const response = await fetch(`${API_BASE_URL}/games/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ width, height, mines }),
        });
        
        console.log('Create game response status:', response.status);
        
        if (!response.ok) {
            let errorMessage = 'Failed to create game';
            try {
                const errorData = await response.json();
                errorMessage = errorData.error || errorMessage;
            } catch (e) {
                console.error('Error parsing error response:', e);
            }
            throw new Error(errorMessage);
        }
        
        const data = await response.json();
        console.log('Game created successfully:', data);
        return data;
    } catch (error) {
        console.error('Error in createGame:', error);
        throw error;
    }
};

export const getGame = async (gameId) => {
    console.log(`API call: Getting game with ID ${gameId}`);
    try {
        const response = await fetch(`${API_BASE_URL}/games/${gameId}/`);
        
        console.log('Get game response status:', response.status);
        
        if (!response.ok) {
            let errorMessage = 'Failed to get game';
            try {
                const errorData = await response.json();
                errorMessage = errorData.error || errorMessage;
            } catch (e) {
                console.error('Error parsing error response:', e);
            }
            throw new Error(errorMessage);
        }
        
        const data = await response.json();
        console.log('Game fetched successfully:', data);
        return data;
    } catch (error) {
        console.error('Error in getGame:', error);
        throw error;
    }
};

export const revealCell = async (gameId, row, col) => {
    console.log(`API call: Revealing cell at (${row}, ${col}) for game ${gameId}`);
    try {
        const response = await fetch(`${API_BASE_URL}/games/${gameId}/reveal/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ row, col }),
        });
        
        console.log('Reveal cell response status:', response.status);
        
        if (!response.ok) {
            let errorMessage = 'Failed to reveal cell';
            try {
                const errorData = await response.json();
                errorMessage = errorData.error || errorMessage;
            } catch (e) {
                console.error('Error parsing error response:', e);
            }
            throw new Error(errorMessage);
        }
        
        const data = await response.json();
        console.log('Cell revealed successfully:', data);
        return data;
    } catch (error) {
        console.error('Error in revealCell:', error);
        throw error;
    }
};