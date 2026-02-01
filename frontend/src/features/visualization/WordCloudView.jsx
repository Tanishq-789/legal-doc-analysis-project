import React from 'react';
import { TagCloud } from 'react-tagcloud';
import { Box, Typography, Paper, CircularProgress } from '@mui/material';
import useDocStore from '../../store/useDocStore';

const WordCloudView = () => {
  const { analysisResults } = useDocStore();

  const data = React.useMemo(() => {
    if (!analysisResults?.word_cloud) return [];
    return analysisResults.word_cloud.map(item => ({
      value: item.text,
      count: item.value,
    }));
  }, [analysisResults]);

  if (!analysisResults) return <CircularProgress />;

  return (
    <Paper elevation={3} sx={{ p: 4, borderRadius: 3, textAlign: 'center', minHeight: 450 }}>
      <Typography variant="h5" fontWeight="bold">Information Density Map</Typography>
      <Box sx={{ mt: 4 }}>
        <TagCloud minSize={18} maxSize={45} tags={data} colorOptions={{ luminosity: 'dark', hue: 'blue' }} />
      </Box>
    </Paper>
  );
};
export default WordCloudView;