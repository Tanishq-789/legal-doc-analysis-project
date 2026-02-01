import { Box, Typography, Tooltip, Chip } from '@mui/material';
import useDocStore from '../../store/useDocStore';

const RiskHighlighter = () => {
  const { analysisData } = useDocStore();

  if (!analysisData) return <Typography>Run analysis to see risks.</Typography>;

  return (
    <Box sx={{ p: 2, lineHeight: 2 }}>
      <Typography variant="h5" gutterBottom>Ambiguity & Risk Analysis</Typography>
      {analysisData.clauses.map((clause, index) => {
        const risk = analysisData.risks.find(r => r.clause_index === index);

        return (
          <Tooltip
            key={index}
            title={risk ? `Ambiguity: ${risk.matched_concept} (Clarity: ${risk.clarity_score})` : ""}
            arrow
          >
            <span style={{
              backgroundColor: risk ? '#fff176' : 'transparent',
              padding: '2px 4px',
              borderRadius: '4px',
              cursor: risk ? 'help' : 'text'
            }}>
              {clause}{" "}
            </span>
          </Tooltip>
        );
      })}
    </Box>
  );
};

export default RiskHighlighter;