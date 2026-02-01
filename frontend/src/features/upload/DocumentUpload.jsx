import React, { useState } from 'react';
import { Box, Button, Typography, CircularProgress, Alert } from '@mui/material';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import { uploadDocument } from '../../api/documentApi';
import useDocStore from '../../store/useDocStore';

const DocumentUpload = () => {
    const [file, setFile] = useState(null);
    const [status, setStatus] = useState('idle'); // idle, loading, success, error
    const { setDocId } = useDocStore();

    const handleFileChange = (e) => {
        const selectedFile = e.target.files[0];
        if (selectedFile) {
            setFile(selectedFile);
            setStatus('idle'); // Resets the "Success" alert for the new file
        }
    };

    const handleUpload = async () => {
        if (!file) return;

        setStatus('loading');
        try {
            const data = await uploadDocument(file);
            // Based on your Swagger output, the response contains 'filename'
            setDocId(data.filename);
            setStatus('success');
        } catch (error) {
            console.error("Upload failed:", error);
            setStatus('error');
        }
    };

    return (
        <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 2 }}>
            <input
                accept="application/pdf"
                style={{ display: 'none' }}
                id="contained-button-file"
                type="file"
                onChange={handleFileChange}
            />
            <label htmlFor="contained-button-file">
                <Button variant="outlined" component="span" startIcon={<CloudUploadIcon />}>
                    {file ? file.name : "Select Legal PDF"}
                </Button>
            </label>

            <Button
                variant="contained"
                onClick={handleUpload}
                disabled={!file || status === 'loading'}
                sx={{ minWidth: 200 }}
            >
                {status === 'loading' ? <CircularProgress size={24} color="inherit" /> : "Upload for Analysis"}
            </Button>

            {status === 'success' && (
                <Alert severity="success">Document ingested. Proceed to AI Analysis.</Alert>
            )}
            {status === 'error' && (
                <Alert severity="error">Upload failed. Ensure the backend server is running.</Alert>
            )}
        </Box>
    );
};

export default DocumentUpload;