export const transformToFlow = (clauses) => {
  const nodes = [];
  const edges = [];

  clauses.forEach((text, index) => {
    // Create a Node for each clause
    nodes.push({
      id: `node-${index}`,
      data: {
        label: (
          <div className="p-2">
            <div style={{ fontSize: '10px', opacity: 0.6, fontWeight: 'bold' }}>STATE {index + 1}</div>
            <div style={{
              display: '-webkit-box',
              WebkitLineClamp: 4, // Limits text to 4 lines
              WebkitBoxOrient: 'vertical',
              overflow: 'hidden',
              lineHeight: '1.4'
            }}>
              {text}
            </div>
          </div>
        )
      },
      style: {
        width: 280, // Force a consistent width
        background: '#1e293b',
        color: '#fff',
        borderRadius: '12px',
        border: '1px solid #334155'
      },
      position: { x: 250, y: index * 180 }, // Increase Y spacing
    });

    // Create a directed Edge to the next clause
    if (index < clauses.length - 1) {
      edges.push({
        id: `edge-${index}`,
        source: `node-${index}`,
        target: `node-${index + 1}`,
        animated: true,
        style: { stroke: '#6366f1' },
        type: 'smoothstep',
      });
    }
  });

  return { nodes, edges };
};