import React from 'react';
import { Container, Tabs, Tab, Box, Paper, Typography, Chip, Stack } from '@mui/material';
import DocumentUpload from './features/upload/DocumentUpload';
import RiskHighlighter from './features/risk-analysis/RiskHighlighter';
import WordCloudView from './features/visualization/WordCloudView';
import LegalGraphView from './features/structural-map/LegalGraphView';
import ProceduralFlowView from './features/visualization/ProceduralFlowView';
import useDocStore from './store/useDocStore';

/**
 * Main Application: LegalDoc AI
 * Features: Automatic domain switching and unified analysis pipeline.
 */
function App() {
  // Access global state and tab navigation from the Zustand store
  const { tabValue, setTabValue, analysisData } = useDocStore();

  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
  };

  /**
   * Domain-Specific Visualization Strategy:
   * Dynamically renders a component based on the classification result.
   */
  const renderVisualInsight = () => {
    if (!analysisData) return null;

    const domain = analysisData.domain_context?.predicted_domain;

    switch (domain) {
      case 'Criminal Law':
        // Explicitly passing data to avoid syntax errors
        return (
          <LegalGraphView
            clauses={analysisData.clauses}
            risks={analysisData.risks}
          />
        );

      case 'Education Law':
        return (
          <ProceduralFlowView
            clauses={analysisData.clauses}
          />
        );

      case 'General Legal':
        return (
          <Box sx={{ p: 4, textAlign: 'center' }}>
            <Typography variant="h6" color="textSecondary" gutterBottom>
              General Document Analysis (Keyword Density)
            </Typography>
            <WordCloudView words={analysisData.word_cloud} />
          </Box>
        );

      default:
        // Default fallback to Word Cloud for Contracts or unknown types
        return <WordCloudView words={analysisData.word_cloud} />;
    }
  };

  /**
   * Helper to determine the label for the 3rd Tab dynamically
   */
  const getDynamicTabLabel = () => {
    if (!analysisData) return "3. Visual Insight";
    const domain = analysisData.domain_context?.predicted_domain;

    if (domain === 'Criminal Law') return "3. Structural Map";
    if (domain === 'Education Law') return "3. Procedural Flow";
    if (domain === 'General Legal') return "3. Keyword Analysis";
    return "3. Keyword Cloud";
  };

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      {/* Header with Classification Badge */}
      <Stack direction="row" justifyContent="space-between" alignItems="center" sx={{ mb: 2 }}>
        <Typography variant="h3" fontWeight="bold" color="primary">
          LegalDoc AI
        </Typography>

        {analysisData?.domain_context && (
          <Chip
            label={`Classified: ${analysisData.domain_context.predicted_domain}`}
            color="secondary"
            variant="filled"
            sx={{ fontWeight: 'bold', fontSize: '1rem', py: 2.5, px: 2, borderRadius: 2 }}
          />
        )}
      </Stack>

      {/* Navigation Bar */}
      <Paper sx={{ width: '100%', mb: 3, borderRadius: 2, elevation: 1 }}>
        <Tabs
          value={tabValue}
          onChange={handleTabChange}
          centered
          indicatorColor="secondary"
          textColor="secondary"
        >
          <Tab label="1. Ingestion" />
          {/* Renamed Tab as per requirements */}
          <Tab label="2. Extracted Content" disabled={!analysisData} />
          <Tab label={getDynamicTabLabel()} disabled={!analysisData} />
        </Tabs>
      </Paper>

      {/* Main Display Area */}
      <Box sx={{ minHeight: '60vh' }}>
        {tabValue === 0 && (
          <Box sx={{ py: 4 }}>
            <DocumentUpload />
          </Box>
        )}

        {tabValue === 1 && (
          <Paper elevation={0} sx={{ p: 3, border: '1px solid #e2e8f0', borderRadius: 2 }}>
            <RiskHighlighter />
          </Paper>
        )}

        {tabValue === 2 && (
          <Box>
             {renderVisualInsight()}
          </Box>
        )}
      </Box>
    </Container>
  );
}

export default App;