import React, { useState } from 'react';
import { Box, Button, Typography, CircularProgress, Alert, Paper, IconButton } from '@mui/material';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import AutoGraphIcon from '@mui/icons-material/AutoGraph';
import ReplayIcon from '@mui/icons-material/Replay';
import { uploadDocument, runDocumentAnalysis } from '../../api/documentApi';
import useDocStore from '../../store/useDocStore';

const DocumentUpload = () => {
    const [file, setFile] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const { setDocId, setAnalysisData, setTabValue, docId } = useDocStore();

    const handleFileChange = (e) => {
        const selectedFile = e.target.files[0];
        if (selectedFile) {
            setFile(selectedFile);
            setError(null); // Clear previous errors on new selection
        }
    };

    /**
     * Resets the component state so a user can upload a new document
     * without refreshing the page.
     */
    const resetUpload = () => {
        setFile(null);
        setDocId(null);
        setError(null);
        setLoading(false);
    };

    const handleAnalyze = async () => {
        if (!file) return;
        setLoading(true);
        setError(null);

        try {
            // STEP 1: Ingest
            const uploadData = await uploadDocument(file);
            const currentDocId = uploadData.filename;
            setDocId(currentDocId);

            // STEP 2: Orchestrate
            const results = await runDocumentAnalysis(currentDocId);

            // --- NEW: EDGE CASE HANDLING ---
            if (results.status === "error") {
                // Display the red text from the backend ('detail')
                setError(results.detail);
                setLoading(false);
                return; // Stop the pipeline here
            }

            if (results.status === "analysis_complete") {
                setAnalysisData(results);
                setTabValue(1);
            }
        } catch (err) {
            console.error("Pipeline Failure:", err);
            setError("Critical Engine Error. Ensure the backend is running.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <Paper elevation={0} sx={{ p: 4, border: '1px solid #e2e8f0', borderRadius: 2 }}>
            <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 3 }}>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <Typography variant="h6" fontWeight="bold">Document Analysis</Typography>
                    {(file || error) && (
                        <IconButton size="small" onClick={resetUpload} title="Clear and Reset">
                            <ReplayIcon fontSize="small" />
                        </IconButton>
                    )}
                </Box>

                {/* File Input - Hidden but triggered by label */}
                <input
                    accept="application/pdf"
                    style={{ display: 'none' }}
                    id="analyze-upload"
                    type="file"
                    onChange={handleFileChange}
                />

                <label htmlFor="analyze-upload">
                    <Button
                        variant="outlined"
                        component="span"
                        startIcon={<CloudUploadIcon />}
                        sx={{ px: 4, textTransform: 'none' }}
                        disabled={loading}
                    >
                        {file ? file.name : "Select Legal PDF"}
                    </Button>
                </label>

                <Button
                    variant="contained"
                    color="primary"
                    size="large"
                    onClick={handleAnalyze}
                    disabled={!file || loading || !!error}
                    startIcon={loading ? <CircularProgress size={20} color="inherit" /> : <AutoGraphIcon />}
                    sx={{ minWidth: 200, py: 1.5, borderRadius: 2, fontWeight: 'bold' }}
                >
                    {loading ? "Extracting..." : "ANALYZE"}
                </Button>

                {/* Error Display (The "Red Text") */}
                {error && (
                    <Alert
                        severity="error"
                        variant="filled"
                        sx={{ width: '100%', mt: 1, borderRadius: 2 }}
                        onClose={resetUpload}
                    >
                        {error}
                    </Alert>
                )}
            </Box>
        </Paper>
    );
};

export default DocumentUpload;