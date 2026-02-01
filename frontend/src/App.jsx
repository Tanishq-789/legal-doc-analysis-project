import { useState } from 'react';
import {
  Container,
  Tabs,
  Tab,
  Box,
  Paper,
  Typography,
  Button,
  CircularProgress,
  Chip,
  Stack
} from '@mui/material';
import DocumentUpload from './features/upload/DocumentUpload';
import RiskView from './features/risk-analysis/RiskView';
import WordCloudView from './features/visualization/WordCloudView';
import useDocStore from './store/useDocStore';
import apiClient from './api/client';

/**
 * Main Application Component for LegalDoc AI.
 * Handles the dashboard layout, tab navigation, and the coordination of
 * the multi-stage NLP pipeline.
 */
function App() {
  const [tabValue, setTabValue] = useState(0);
  const [loading, setLoading] = useState(false);
  const { docId, setAnalysisResults, analysisResults } = useDocStore();

  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
  };

  /**
   * Triggers the backend AI analysis pipeline.
   * Path: /api/v1/analysis/{doc_id}/run
   * This executes VSM Classification, Lawformer Ambiguity Detection,
   * and Graph-based Knapsack Optimization.
   */
  const handleRunAnalysis = async () => {
    if (!docId) return;

    setLoading(true);
    try {
      // API call to run the full pipeline
      const res = await apiClient.post(`/analysis/${docId}/run`);

      // 1. Update global state with pipeline results
      setAnalysisResults(res.data);

      // 2. Automatically transition to the Risk Analysis view
      setTabValue(1);

      console.log("Analysis Complete. VSM Domain:", res.data.domain_context?.predicted_domain);
    } catch (err) {
      console.error("Pipeline failure:", err);
      alert("Analysis failed. Check backend logs for Transformer or Graph errors.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      {/* Header Section with VSM Classification Result */}
      <Stack direction="row" justifyContent="space-between" alignItems="center" sx={{ mb: 2 }}>
        <Typography variant="h3" fontWeight="bold" gutterBottom>
          LegalDoc AI
        </Typography>

        {/* Dynamic Badge displaying the detected legal domain */}
        {analysisResults?.domain_context && (
          <Chip
            label={`Domain: ${analysisResults.domain_context.predicted_domain}`}
            color="primary"
            variant="outlined"
            sx={{ fontWeight: 'bold', fontSize: '1rem', py: 2 }}
          />
        )}
      </Stack>

      {/* Navigation Tabs */}
      <Paper sx={{ width: '100%', mb: 3 }}>
        <Tabs value={tabValue} onChange={handleTabChange} centered>
          <Tab label="1. Ingestion" />
          <Tab label="2. Risk Analysis" disabled={!analysisResults} />
          <Tab label="3. Keyword Cloud" disabled={!analysisResults} />
        </Tabs>
      </Paper>

      {/* Tab Content Areas */}
      <Box sx={{ p: 2 }}>
        {tabValue === 0 && (
          <Box sx={{ textAlign: 'center' }}>
            <DocumentUpload />

            {/* Action button visible only after file upload is confirmed */}
            {docId && !analysisResults && (
              <Button
                variant="contained"
                color="secondary"
                size="large"
                sx={{ mt: 3, px: 8, py: 1.5, borderRadius: 2, fontWeight: 'bold' }}
                onClick={handleRunAnalysis}
                disabled={loading}
              >
                {loading ? <CircularProgress size={26} color="inherit" /> : "Run AI Risk Assessment"}
              </Button>
            )}
          </Box>
        )}

        {/* Module 2: Semantic Highlight View (Lawformer) */}
        {tabValue === 1 && <RiskView />}

        {/* Module 3: Information Density Map (Graph + Knapsack) */}
        {tabValue === 2 && <WordCloudView />}
      </Box>
    </Container>
  );
}

export default App;