import React from 'react';
import { Box, Typography, Tooltip, Paper } from '@mui/material';
import useDocStore from '../../store/useDocStore';

/**
 * RiskHighlighter: Renders document clauses with precision-targeted
 * word highlights based on Lawformer/VSM/FSM "evidence" tokens.
 */
const RiskHighlighter = () => {
  const { analysisData } = useDocStore();

  if (!analysisData) {
    return (
      <Paper sx={{ p: 3, textAlign: 'center', bgcolor: '#f5f5f5' }}>
        <Typography color="textSecondary">Upload and run analysis to view evidence-based highlights.</Typography>
      </Paper>
    );
  }

  const { clauses, visualization_evidence, risks, domain_context } = analysisData;

  /**
   * Helper: Highlights specific "Responsible Words" within a block of text.
   */
  const highlightResponsibleWords = (text, evidence) => {
    if (!evidence || evidence.length === 0) return text;

    // Create a regex from evidence tokens (case-insensitive)
    const pattern = new RegExp(`(${evidence.join('|')})`, 'gi');
    const parts = text.split(pattern);

    return parts.map((part, i) =>
      evidence.some(word => word.toLowerCase() === part.toLowerCase()) ? (
        <Box
          component="mark"
          key={i}
          sx={{
            backgroundColor: '#ffeb3b', // Bright yellow for responsible words
            color: '#000',
            fontWeight: 'bold',
            px: '2px',
            borderRadius: '2px',
            borderBottom: '2px solid #fbc02d',
            transition: 'all 0.2s',
            '&:hover': { backgroundColor: '#fdd835' }
          }}
        >
          {part}
        </Box>
      ) : (
        <span key={i}>{part}</span>
      )
    );
  };

  return (
    <Box sx={{ p: 2 }}>
      <Box sx={{ mb: 3, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Typography variant="h5" sx={{ fontWeight: 600 }}>
          Domain Evidence: {domain_context.predicted_domain}
        </Typography>
        <Typography variant="caption" sx={{ bgcolor: '#e3f2fd', p: 1, borderRadius: 1 }}>
          Algorithm: {domain_context.algorithm_used}
        </Typography>
      </Box>

      <Box sx={{ lineHeight: 1.8, fontSize: '1.1rem', textAlign: 'justify' }}>
        {clauses.map((clause, index) => {
          const risk = risks.find(r => r.clause_index === index);

          return (
            <Tooltip
              key={index}
              title={risk ? `Condition: ${risk.matched_anchor} | Clarity: ${risk.clarity_score}` : ""}
              placement="top"
              arrow
            >
              <Box
                component="span"
                sx={{
                  backgroundColor: risk ? 'rgba(255, 241, 118, 0.15)' : 'transparent',
                  borderLeft: risk ? '3px solid #fbc02d' : 'none',
                  pl: risk ? 1 : 0,
                  mr: 0.5,
                  display: 'inline',
                  cursor: risk ? 'help' : 'text'
                }}
              >
                {highlightResponsibleWords(clause, visualization_evidence)}
                {" "}
              </Box>
            </Tooltip>
          );
        })}
      </Box>
    </Box>
  );
};

export default RiskHighlighter;