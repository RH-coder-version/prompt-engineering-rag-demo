/* Shared pure functions used by the browser demo and Node tests. */
(function(root) {
  function retrieve(chunks, query, topK = 3) {
    return chunks.map(chunk => ({
      ...chunk,
      score: chunk.tags.filter(tag => query.includes(tag)).length
    })).filter(chunk => chunk.score > 0)
      .sort((a, b) => b.score - a.score).slice(0, topK);
  }
  function checklistScore(flags) {
    if (flags.length !== 10 || flags.some(v => ![0, 1, false, true].includes(v)))
      throw new Error('Expected ten binary checklist judgments');
    return flags.reduce((sum, value) => sum + Number(value), 0) * 10;
  }
  const api = { retrieve, checklistScore };
  if (typeof module !== 'undefined') module.exports = api;
  root.DemoCore = api;
})(typeof globalThis !== 'undefined' ? globalThis : this);
