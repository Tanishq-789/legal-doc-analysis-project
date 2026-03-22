import React from 'react';
import { TagCloud } from 'react-tagcloud';
import { Box, Typography, Paper } from '@mui/material';

const WordCloudView = ({ words = [] }) => {
  // Map our backend schema {text, value} to the component's {value, count}
  const cloudData = words.map(w => ({
    value: w.text,
    count: w.value
  }));

  if (words.length === 0) {
    return <Typography color="textSecondary">Waiting for Knapsack optimization...</Typography>;
  }

  return (
    <Paper elevation={0} sx={{ p: 3, textAlign: 'center', bgcolor: '#fafafa' }}>
      <Typography variant="h6" gutterBottom>Keyword Information Density (Knapsack)</Typography>
      <Box sx={{ p: 2 }}>
        <TagCloud
          minSize={12}
          maxSize={45}
          tags={cloudData}
          onClick={tag => alert(`Term: ${tag.value}`)}
        />
      </Box>
    </Paper>
  );
};

export default WordCloudView;