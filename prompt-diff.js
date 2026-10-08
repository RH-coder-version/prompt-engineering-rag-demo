// Highlight new or rewritten clauses relative to the previous experimental prompt.
// Text stays in the original textarea; highlighting never changes the API payload.
function promptDiffSegments(current, previous) {
  const parts = current.match(/[^，。；\n]+[，。；\n]?|[，。；\n]/g) || [];
  return parts.map(text => ({text, added: previous !== null && !previous.includes(text.replace(/[，。；\n]+$/g, '').trim())}));
}
function renderPromptDiff() {
  if (!protocol) return;
  const index = Number(document.getElementById('condition').value);
  const input = document.getElementById('live-prompt');
  const mirror = document.getElementById('prompt-mirror');
  const previous = index ? protocol.conditions[index - 1].prompt : null;
  mirror.replaceChildren(...promptDiffSegments(input.value, previous).map(part => {
    const span = document.createElement('span');
    span.textContent = part.text;
    if (part.added) span.className = 'prompt-added';
    return span;
  }));
  document.getElementById('diff-legend').textContent = index ? '红色：相对上一条件新增或改写的语句；黑色：保留内容。' : '第 1 轮为基线。后续条件用红色标出新增或改写的语句。';
  mirror.scrollTop = input.scrollTop;
}
document.getElementById('live-prompt').addEventListener('input', renderPromptDiff);
document.getElementById('live-prompt').addEventListener('scroll', () => {
  document.getElementById('prompt-mirror').scrollTop = document.getElementById('live-prompt').scrollTop;
});
