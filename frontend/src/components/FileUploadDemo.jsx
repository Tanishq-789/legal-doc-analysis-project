// frontend/src/components/FileUploadDemo.jsx
import { useState } from 'react';
import { Box, Button, Typography, Alert, CircularProgress, Paper } from '@mui/material';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';

const FileUploadDemo = () => {
    const [selectedFile, setSelectedFile] = useState(null);
    const [uploadStatus, setUploadStatus] = useState(null); // 'loading', 'success', 'error'
    const [apiResponse, setApiResponse] = useState(null);

    const handleFileSelect = (event) => {
        // Get the first file selected
        const file = event.target.files[0];
        if (file) {
            // Basic validation to ensure it's a PDF
            if (file.type !== 'application/pdf') {
                alert("For this project, please select PDF files only.");
                return;
            }
            setSelectedFile(file);
            // Reset previous states
            setUploadStatus(null);
            setApiResponse(null);
        }
    };

    const handleUploadClick = async () => {
        if (!selectedFile) {
            alert("Please select a file first!");
            return;
        }

        setUploadStatus('loading');

        // 1. Prepare FormData data to send file
        const formData = new FormData();
        formData.append('file', selectedFile);

        try {
            // 2. Call the FastAPI backend
            // Note: Ensure port 8000 matches your backend running port
            const response = await fetch('http://localhost:8000/upload', {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();

            // 3. Handle success
            setApiResponse(data);
            setUploadStatus('success');
            console.log("Backend response:", data);

        } catch (error) {
            // 4. Handle error
            console.error("Upload failed:", error);
            setUploadStatus('error');
        }
    };

    return (
        <Paper elevation={3} sx={{ p: 4, maxWidth: 500, mx: 'auto', mt: 5, textAlign: 'center' }}>
            <Typography variant="h5" gutterBottom>
                Day 1: Walking Skeleton Demo
            </Typography>
            <Typography variant="body2" color="text.secondary" mb={3}>
                Select a legal PDF to test backend connectivity.
            </Typography>

            {/* Hidden actual HTML file input */}
            <input
                accept="application/pdf"
                style={{ display: 'none' }}
                id="raised-button-file"
                type="file"
                onChange={handleFileSelect}
            />

            {/* MUI Button acting as the label for the hidden input */}
            <label htmlFor="raised-button-file">
                <Button variant="outlined" component="span" sx={{ mb: 2 }}>
                    Choose PDF File
                </Button>
            </label>

            {/* Display selected filename */}
            {selectedFile && (
                <Typography variant="body1" sx={{ my: 2, fontWeight: 'bold' }}>
                    Selected: {selectedFile.name}
                </Typography>
            )}

            {/* Upload Button */}
            <Box sx={{ position: 'relative', mt: 3 }}>
                <Button
                    variant="contained"
                    color="primary"
                    startIcon={<CloudUploadIcon />}
                    onClick={handleUploadClick}
                    disabled={!selectedFile || uploadStatus === 'loading'}
                >
                    Upload to Backend
                </Button>
                {/* Loading spinner overlay */}
                {uploadStatus === 'loading' && (
                    <CircularProgress
                        size={24}
                        sx={{
                            position: 'absolute',
                            top: '50%',
                            left: '50%',
                            marginTop: '-12px',
                            marginLeft: '-12px',
                        }}
                    />
                )}
            </Box>

            {/* Success/Error Alerts */}
            {uploadStatus === 'success' && apiResponse && (
                <Alert severity="success" sx={{ mt: 3, textAlign: 'left' }}>
                    <strong>Success!</strong> Backend received: <br/>
                    -- Filename: {apiResponse.filename}<br />
                    -- Message: {apiResponse.message}
                </Alert>
            )}

            {uploadStatus === 'error' && (
                <Alert severity="error" sx={{ mt: 3 }}>
                    Upload failed. Check frontend console and backend terminal logs.
                </Alert>
            )}
        </Paper>
    );
};

export default FileUploadDemo;