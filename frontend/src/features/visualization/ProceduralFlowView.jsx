import React, { useMemo } from 'react';
import {
  ReactFlow,
  Background,
  Controls,
  MiniMap,
  useNodesState,
  useEdgesState,
  Handle,
  Position
} from '@xyflow/react';
import '@xyflow/react/dist/style.css';
import { Box, Typography, Paper } from '@mui/material';
import dagre from 'dagre'; // Import the layout engine
import { transformToFlow } from '../../utils/flowTransformer';

// 1. Create the Dagre Graph Instance
const dagreGraph = new dagre.graphlib.Graph();
dagreGraph.setDefaultEdgeLabel(() => ({}));

const nodeWidth = 320;
const nodeHeight = 180; // Estimated height; Dagre will use this for spacing

/**
 * Layout Engine Utility
 * Computes X and Y coordinates to prevent overlaps.
 */
const getLayoutedElements = (nodes, edges, direction = 'TB') => {
  dagreGraph.setGraph({ rankdir: direction, ranksep: 80, nodesep: 50 });

  nodes.forEach((node) => {
    dagreGraph.setNode(node.id, { width: nodeWidth, height: nodeHeight });
  });

  edges.forEach((edge) => {
    dagreGraph.setEdge(edge.source, edge.target);
  });

  dagre.layout(dagreGraph);

  const layoutedNodes = nodes.map((node) => {
    const nodeWithPosition = dagreGraph.node(node.id);
    return {
      ...node,
      position: {
        // Center the node based on Dagre's top-left calculation
        x: nodeWithPosition.x - nodeWidth / 2,
        y: nodeWithPosition.y - nodeHeight / 2,
      },
    };
  });

  return { nodes: layoutedNodes, edges };
};

const LegalNode = ({ data }) => {
  return (
    <Paper
      elevation={3}
      sx={{
        padding: '20px',
        borderRadius: '10px',
        border: '2px solid #6366f1',
        backgroundColor: '#ffffff',
        width: `${nodeWidth}px`,
        textAlign: 'left',
        whiteSpace: 'normal',
      }}
    >
      <Handle type="target" position={Position.Top} style={{ background: '#6366f1', width: '10px', height: '10px' }} />

      <Typography variant="caption" sx={{ fontWeight: 'bold', color: '#6366f1', textTransform: 'uppercase', mb: 1, display: 'block' }}>
        {data.label || "Clause State"}
      </Typography>

      <Typography variant="body2" sx={{ color: '#1e293b', lineHeight: 1.6, wordBreak: 'break-word' }}>
        {data.fullText || data.label}
      </Typography>

      <Handle type="source" position={Position.Bottom} style={{ background: '#6366f1', width: '10px', height: '10px' }} />
    </Paper>
  );
};

const nodeTypes = { legalNode: LegalNode };

const ProceduralFlowView = ({ clauses }) => {
  const { nodes: layoutedNodes, edges: layoutedEdges } = useMemo(() => {
    // 1. Get raw nodes/edges from your transformer
    const { nodes, edges } = transformToFlow(clauses);

    // 2. Map to custom types
    const mappedNodes = nodes.map(node => ({
      ...node,
      type: 'legalNode',
      data: { ...node.data, fullText: node.data.label }
    }));

    // 3. Run through Dagre layout engine
    return getLayoutedElements(mappedNodes, edges);
  }, [clauses]);

  const [nodes, , onNodesChange] = useNodesState(layoutedNodes);
  const [edges, , onEdgesChange] = useEdgesState(layoutedEdges);

  return (
    <Box sx={{ width: '100%', height: '700px', background: '#f8fafc', borderRadius: 2, border: '1px solid #e2e8f0', position: 'relative' }}>
      <ReactFlow
        nodes={nodes}
        edges={edges}
        nodeTypes={nodeTypes}
        onNodesChange={onNodesChange}
        fitView
        colorMode="light"
        // Prevent manual dragging from breaking the layout if desired
        nodesDraggable={true}
      >
        <Background variant="dots" gap={25} size={1} color="#cbd5e1" />
        <Controls />
        <MiniMap />
      </ReactFlow>
    </Box>
  );
};

export default ProceduralFlowView;