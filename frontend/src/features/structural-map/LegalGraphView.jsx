import React, { useMemo, useRef, useEffect } from 'react';
import ForceGraph2D from 'react-force-graph-2d';
import { Box, Typography, Paper, Stack } from '@mui/material';

// --- Professional Legal Theme ---
const PARCHMENT_BG = '#fdfaf2';
const NODE_PRIMARY = '#1e88e5';
const NODE_RISK = '#d32f2f';
const TEXT_MAIN = '#1a1a1a';

const LegalGraphView = ({ clauses = [], risks = [] }) => {
  const fgRef = useRef();

  // 1. DATA TRANSFORMATION
  const graphData = useMemo(() => {
    if (!clauses.length) return { nodes: [], links: [] };

    const nodes = clauses.map((text, index) => {
      const isRisky = risks.some(r => r.clause_index === index);
      return {
        id: index,
        label: `Clause ${index + 1}`,
        fullText: text,
        color: isRisky ? NODE_RISK : NODE_PRIMARY,
      };
    });

    const links = [];
    for (let i = 0; i < nodes.length - 1; i++) {
      links.push({ source: i, target: i + 1 });
    }

    return { nodes, links };
  }, [clauses, risks]);

  // 2. FORCE SIMULATION CONFIG
  useEffect(() => {
    const fg = fgRef.current;
    if (fg) {
      // Increased distance and charge to accommodate vertical labels
      fg.d3Force('link').distance(180);
      fg.d3Force('charge').strength(-500);
    }
  }, [graphData]);

  // 3. REFINED CUSTOM NODE & LABEL RENDERER
  const renderNodeWithBottomLabel = (node, ctx, globalScale) => {
    const fontSize = 13 / globalScale; // Slightly smaller for better density
    const nodeRadius = 6;
    const verticalGap = 12; // Space between node bottom and text top

    // Truncate text for the graph view
    const displayText = `${node.label}: ${node.fullText.substring(0, 50)}...`;

    // --- DRAW NODE CIRCLE ---
    ctx.beginPath();
    ctx.arc(node.x, node.y, nodeRadius, 0, 2 * Math.PI, false);
    ctx.fillStyle = node.color;
    ctx.fill();
    ctx.strokeStyle = '#ffffff';
    ctx.lineWidth = 1;
    ctx.stroke();

    // --- DRAW CENTERED BOTTOM LABEL ---
    ctx.font = `${fontSize}px "Roboto", "Helvetica", "Arial", sans-serif`;

    // Set horizontal alignment to center so node.x is the midpoint
    ctx.textAlign = 'center';

    // Set baseline to top so text grows downwards from the Y coordinate
    ctx.textBaseline = 'top';

    ctx.fillStyle = TEXT_MAIN;

    // Math: X = node center, Y = node center + radius + gap
    ctx.fillText(displayText, node.x, node.y + nodeRadius + verticalGap);
  };

  if (clauses.length === 0) {
    return (
      <Box sx={{ p: 4, textAlign: 'center' }}>
        <Typography color="textSecondary">No structural data found to map.</Typography>
      </Box>
    );
  }

  return (
    <Paper
      elevation={0}
      sx={{
        width: '100%',
        height: '650px',
        bgcolor: PARCHMENT_BG,
        borderRadius: 2,
        border: '1px solid #e2e8f0',
        overflow: 'hidden',
        position: 'relative'
      }}
    >
      {/* Legend Overlay */}
      <Box sx={{ position: 'absolute', top: 20, left: 20, zIndex: 10, bgcolor: 'rgba(255,255,255,0.7)', p: 2, borderRadius: 2, border: '1px solid #eee', backdropFilter: 'blur(4px)' }}>
        <Typography variant="caption" sx={{ display: 'block', fontWeight: 'bold', mb: 1 }}>
          STRUCTURAL MAP LEGEND
        </Typography>
        <Stack spacing={1}>
          <Box sx={{ display: 'flex', alignItems: 'center' }}>
            <Box sx={{ width: 10, height: 10, bgcolor: NODE_PRIMARY, borderRadius: '50%', mr: 1 }} />
            <Typography variant="caption">Standard Clause</Typography>
          </Box>
          <Box sx={{ display: 'flex', alignItems: 'center' }}>
            <Box sx={{ width: 10, height: 10, bgcolor: NODE_RISK, borderRadius: '50%', mr: 1 }} />
            <Typography variant="caption">Risk/Penalty Anchor</Typography>
          </Box>
        </Stack>
      </Box>

      <ForceGraph2D
        ref={fgRef}
        graphData={graphData}
        nodeCanvasObject={renderNodeWithBottomLabel}
        nodeRelSize={6}
        linkWidth={1.5}
        linkColor={() => 'rgba(0, 0, 0, 0.1)'} // Subtle links
        linkDirectionalArrowLength={4}
        linkDirectionalArrowRelPos={1}
        backgroundColor={PARCHMENT_BG}
        cooldownTicks={100}
      />
    </Paper>
  );
};

export default LegalGraphView;