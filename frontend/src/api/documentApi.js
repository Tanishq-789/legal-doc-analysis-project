import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api/v1';

export const uploadDocument = async (file) => {
    const formData = new FormData();
    // 'file' must match the key expected by the FastAPI 'UploadFile' parameter
    formData.append('file', file);

    const response = await axios.post(`${API_BASE_URL}/documents/upload`, formData, {
        headers: {
            'Content-Type': 'multipart/form-data',
        },
    });
    return response.data;
};