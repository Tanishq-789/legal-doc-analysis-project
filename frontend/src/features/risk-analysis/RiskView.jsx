// frontend/src/features/risk-analysis/RiskView.jsx
import { Box, Typography, Tooltip, Paper, Chip } from '@mui/material';
import useDocStore from '../../store/useDocStore';

export default function RiskView() {
  const { analysisResults } = useDocStore();

  if (!analysisResults) return null;

  return (
    <Box>
      <Box sx={{ mb: 3, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Typography variant="h5">Intelligent Risk Assessment</Typography>
        <Chip label={`Clauses Analyzed: ${analysisResults.clauses.length}`} color="primary" variant="outlined" />
      </Box>

      <Paper elevation={3} sx={{ p: 4, bgcolor: '#fafafa', borderRadius: 3, lineHeight: 1.8 }}>
        {analysisResults.clauses.map((clause, idx) => {
          // Check if this specific clause has a detected risk
          const risk = analysisResults.risks.find(r => r.clause_index === idx);

          return (
            <Tooltip
              key={idx}
              title={risk ? `AMBIGUITY DETECTED: "${risk.matched_concept}" (Clarity Score: ${risk.clarity_score})` : ""}
              arrow
              placement="top"
            >
              <span style={{
                backgroundColor: risk ? 'rgba(255, 235, 59, 0.5)' : 'transparent',
                borderBottom: risk ? '2px solid #fbc02d' : 'none',
                padding: '2px 0',
                cursor: risk ? 'help' : 'text',
                transition: 'background-color 0.3s'
              }}>
                {clause}{" "}
              </span>
            </Tooltip>
          );
        })}
      </Paper>
    </Box>
  );
}