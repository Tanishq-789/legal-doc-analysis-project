export const transformToGraph = (clauses, risks = []) => {
  const nodes = clauses.map((text, index) => {
    // Check if this clause is flagged as a risk/fuzzy
    const isRisk = risks.some(r => r.clause_index === index || text.includes(r.term));

    return {
      id: `c-${index}`,
      label: `Clause ${index + 1}`,
      fullText: text,
      val: isRisk ? 15 : 10, // Nodes with risk are larger
      color: isRisk ? '#ef4444' : '#3b82f6', // Red for risk, Blue for normal
    };
  });

  const links = [];
  // Basic semantic linking: Link consecutive clauses or based on shared keywords
  for (let i = 0; i < nodes.length - 1; i++) {
    links.push({
      source: nodes[i].id,
      target: nodes[i + 1].id,
      label: 'procedural_flow'
    });
  }

  return { nodes, links };
};