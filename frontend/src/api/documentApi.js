import apiClient from './client';

/**
 * uploadDocument: Ingests the PDF into the backend's storage.
 * Endpoint: POST /api/v1/documents/upload
 */
export const uploadDocument = async (file) => {
    const formData = new FormData();
    formData.append('file', file);

    const response = await apiClient.post('/documents/upload', formData, {
        headers: {
            'Content-Type': 'multipart/form-data',
        },
    });
    return response.data;
};

/**
 * runDocumentAnalysis: Triggers the Orchestrated Lawformer Pipeline.
 * This starts the pivot to VSM, FSM, or Fuzzy algorithms.
 * Endpoint: POST /api/v1/analysis/{doc_id}/run
 */
export const runDocumentAnalysis = async (docId) => {
    try {
        // encodeURIComponent handles filenames with spaces safely in the URL path
        const encodedId = encodeURIComponent(docId);
        const response = await apiClient.post(`/analysis/${encodedId}/run`);

        // Returns the data containing 'visualization_evidence' (Responsible Words)
        return response.data;
    } catch (error) {
        console.error("Orchestration Pipeline Error:", error.response?.data || error.message);
        throw error;
    }
};