// Pull the first {...} block out of the reply (v0 often wraps JSON in a code fence), then compare one field.
function parse(output) {
  const m = String(output).match(/\{[\s\S]*\}/);
  try { return m ? JSON.parse(m[0]) : null; } catch (e) { return null; }
}
module.exports.category = (output, ctx) => { const j = parse(output); return !!j && j.category === ctx.vars.category; };
module.exports.urgency = (output, ctx) => { const j = parse(output); return !!j && j.urgency === ctx.vars.urgency; };
module.exports.needsHuman = (output, ctx) => { const j = parse(output); return !!j && String(j.needs_human) === String(ctx.vars.needs_human); };
