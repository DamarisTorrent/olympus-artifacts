// Minimal structural validator for data-flow-trace.schema.json (draft 2020-12 subset:
// type, required, additionalProperties, enum, pattern, minLength, minItems, minimum).
const fs = require('fs');
const path = process.argv[2];
const doc = JSON.parse(fs.readFileSync(path, 'utf8'));

const errors = [];
function err(p, m) { errors.push(`${p || '<root>'}: ${m}`); }

const ENUM = {
  pii: ['none', 'pii', 'phi', 'sensitive', 'fti'],
  entryIface: ['web-form', 'api', 'batch-file', 'queue', 'sftp', 'direct-db', 'tiff-upload', 'manual-entry'],
  exitIface: ['api', 'file-export', 'queue', 'report', 'screen', 'batch-feed', 'print', 'email', 'sftp'],
  op: ['validate', 'normalize', 'enrich', 'redact', 'aggregate', 'split', 'encode', 'decode', 'calculate', 'translate', 'route'],
  store: ['relational-table', 'adabas-file', 'tiff-image', 'file-system', 'queue-topic', 'cache', 'session-state', 'xml-document', 'json-document'],
  sev: ['critical', 'high', 'medium', 'low', 'info'],
  cat: ['data-loss', 'pii-leak', 'redundant-store', 'unreconciled-copy', 'orphaned-data', 'type-coercion', 'encoding-mismatch'],
};
const FLOW_ID = /^DF-[A-Z0-9]+-[0-9]{3}$/;

function obj(v, p, required, allowed) {
  if (v === null || typeof v !== 'object' || Array.isArray(v)) { err(p, 'must be an object'); return false; }
  for (const k of required) if (!(k in v)) err(p, `missing required property "${k}"`);
  for (const k of Object.keys(v)) {
    if (!allowed.includes(k)) err(p, `additionalProperties:false violated by "${k}"`);
    if (v[k] === null) err(p, `"${k}" is null (schema admits no null)`);
  }
  return true;
}
function str(v, p, { minLength = 0, enumv, pattern } = {}) {
  if (v === undefined) return;
  if (typeof v !== 'string') { err(p, `must be a string, got ${v === null ? 'null' : typeof v}`); return; }
  if (v.length < minLength) err(p, `minLength ${minLength} violated`);
  if (enumv && !enumv.includes(v)) err(p, `"${v}" not in enum [${enumv}]`);
  if (pattern && !pattern.test(v)) err(p, `"${v}" fails pattern ${pattern}`);
}
function bool(v, p) { if (v !== undefined && typeof v !== 'boolean') err(p, 'must be a boolean'); }

obj(doc, '', ['application', 'flows'],
  ['application', 'flows', 'cross_flow_findings', '$schema', 'generated', 'methodology_notes']);

if (obj(doc.application, 'application', ['name', 'id'], ['name', 'id'])) {
  str(doc.application.name, 'application.name', { minLength: 1 });
  str(doc.application.id, 'application.id', { minLength: 1 });
}
str(doc.$schema, '$schema');
str(doc.generated, 'generated');

if (!Array.isArray(doc.flows)) err('flows', 'must be an array');
else doc.flows.forEach((f, i) => {
  const P = `flows[${i}]`;
  obj(f, P, ['flow_id', 'data_element', 'entry_point', 'transformations', 'persistence_points', 'exit_points'],
    ['flow_id', 'data_element', 'entry_point', 'transformations', 'persistence_points', 'exit_points',
     'crosses_system_boundary', 'crosses_identity_boundary', 'has_implicit_transformations', 'risk_findings']);
  str(f.flow_id, `${P}.flow_id`, { pattern: FLOW_ID });

  const de = f.data_element;
  if (obj(de, `${P}.data_element`, ['name', 'pii_classification'],
      ['name', 'type', 'description', 'business_meaning', 'pii_classification'])) {
    str(de.name, `${P}.data_element.name`, { minLength: 1 });
    str(de.pii_classification, `${P}.data_element.pii_classification`, { enumv: ENUM.pii });
    str(de.type, `${P}.data_element.type`);
    str(de.description, `${P}.data_element.description`);
    str(de.business_meaning, `${P}.data_element.business_meaning`);
  }

  const ep = f.entry_point;
  if (obj(ep, `${P}.entry_point`, ['system', 'interface', 'citation'], ['system', 'interface', 'citation'])) {
    str(ep.system, `${P}.entry_point.system`, { minLength: 1 });
    str(ep.interface, `${P}.entry_point.interface`, { enumv: ENUM.entryIface });
    str(ep.citation, `${P}.entry_point.citation`, { minLength: 1 });
  }

  if (!Array.isArray(f.transformations)) err(`${P}.transformations`, 'must be an array');
  else f.transformations.forEach((t, j) => {
    const Q = `${P}.transformations[${j}]`;
    obj(t, Q, ['step', 'operation', 'location'], ['step', 'operation', 'description', 'location', 'implicit']);
    if (!Number.isInteger(t.step)) err(`${Q}.step`, 'must be an integer');
    else if (t.step < 1) err(`${Q}.step`, 'minimum 1 violated');
    str(t.operation, `${Q}.operation`, { enumv: ENUM.op });
    str(t.description, `${Q}.description`);
    bool(t.implicit, `${Q}.implicit`);
    if (obj(t.location, `${Q}.location`, ['system', 'citation'], ['system', 'component', 'citation'])) {
      str(t.location.system, `${Q}.location.system`, { minLength: 1 });
      str(t.location.citation, `${Q}.location.citation`, { minLength: 1 });
      str(t.location.component, `${Q}.location.component`);
    }
  });

  if (!Array.isArray(f.persistence_points)) err(`${P}.persistence_points`, 'must be an array');
  else f.persistence_points.forEach((pp, j) => {
    const Q = `${P}.persistence_points[${j}]`;
    obj(pp, Q, ['system', 'store_type', 'location', 'source_of_truth', 'citation'],
      ['system', 'store_type', 'location', 'source_of_truth', 'retention', 'citation']);
    str(pp.system, `${Q}.system`, { minLength: 1 });
    str(pp.store_type, `${Q}.store_type`, { enumv: ENUM.store });
    str(pp.location, `${Q}.location`, { minLength: 1 });
    if (typeof pp.source_of_truth !== 'boolean') err(`${Q}.source_of_truth`, 'must be a boolean');
    str(pp.retention, `${Q}.retention`);
    str(pp.citation, `${Q}.citation`, { minLength: 1 });
  });

  if (!Array.isArray(f.exit_points)) err(`${P}.exit_points`, 'must be an array');
  else f.exit_points.forEach((xp, j) => {
    const Q = `${P}.exit_points[${j}]`;
    obj(xp, Q, ['system', 'interface', 'citation'], ['system', 'interface', 'citation', 'external_consumer']);
    str(xp.system, `${Q}.system`, { minLength: 1 });
    str(xp.interface, `${Q}.interface`, { enumv: ENUM.exitIface });
    str(xp.citation, `${Q}.citation`, { minLength: 1 });
    bool(xp.external_consumer, `${Q}.external_consumer`);
  });

  bool(f.crosses_system_boundary, `${P}.crosses_system_boundary`);
  bool(f.crosses_identity_boundary, `${P}.crosses_identity_boundary`);
  bool(f.has_implicit_transformations, `${P}.has_implicit_transformations`);

  if (f.risk_findings !== undefined) {
    if (!Array.isArray(f.risk_findings)) err(`${P}.risk_findings`, 'must be an array');
    else f.risk_findings.forEach((r, j) => {
      const Q = `${P}.risk_findings[${j}]`;
      obj(r, Q, ['finding', 'severity', 'category'], ['finding', 'severity', 'category']);
      str(r.finding, `${Q}.finding`, { minLength: 1 });
      str(r.severity, `${Q}.severity`, { enumv: ENUM.sev });
      str(r.category, `${Q}.category`, { enumv: ENUM.cat });
    });
  }
});

if (doc.cross_flow_findings !== undefined) {
  if (!Array.isArray(doc.cross_flow_findings)) err('cross_flow_findings', 'must be an array');
  else doc.cross_flow_findings.forEach((c, i) => {
    const Q = `cross_flow_findings[${i}]`;
    obj(c, Q, ['finding', 'flows_involved', 'severity'], ['finding', 'flows_involved', 'severity']);
    str(c.finding, `${Q}.finding`, { minLength: 1 });
    str(c.severity, `${Q}.severity`, { enumv: ENUM.sev });
    if (!Array.isArray(c.flows_involved)) err(`${Q}.flows_involved`, 'must be an array');
    else {
      if (c.flows_involved.length < 1) err(`${Q}.flows_involved`, 'minItems 1 violated');
      c.flows_involved.forEach((x, j) => str(x, `${Q}.flows_involved[${j}]`, { pattern: FLOW_ID }));
    }
  });
}

// ---- Skill quality rules (not schema, but gate conditions) ----
const q = [];
const ids = new Set(doc.flows.map(f => f.flow_id));
if (ids.size !== doc.flows.length) q.push('duplicate flow_id');
doc.flows.forEach(f => {
  const P = f.flow_id;
  if (!f.persistence_points?.length) q.push(`${P}: no persistence_points`);
  if (!f.exit_points?.length) q.push(`${P}: no exit_points`);
  if (!f.transformations?.length) q.push(`${P}: no transformations`);
  const sot = (f.persistence_points || []).filter(p => p.source_of_truth).length;
  const hasUnrec = (f.risk_findings || []).some(r => r.category === 'unreconciled-copy');
  if (sot !== 1 && !hasUnrec) q.push(`${P}: ${sot} source_of_truth and no unreconciled-copy finding`);
  (f.persistence_points || []).forEach((p, i) => {
    const hasOrph = (f.risk_findings || []).some(r => r.category === 'orphaned-data');
    if (!p.retention && !hasOrph) q.push(`${P}: persistence[${i}] has no retention and flow has no orphaned-data finding`);
  });
  const anyImplicit = (f.transformations || []).some(t => t.implicit === true);
  if (anyImplicit !== (f.has_implicit_transformations === true)) q.push(`${P}: has_implicit_transformations disagrees with transformations`);
  (f.transformations || []).forEach((t, i) => {
    if (t.implicit === true && !t.description) q.push(`${P}: implicit transformation[${i}] has no description`);
  });
  const SEV = { critical: 5, high: 4, medium: 3, low: 2, info: 1 };
  const ext = (f.exit_points || []).some(x => x.external_consumer === true);
  if (['pii', 'phi', 'fti'].includes(f.data_element?.pii_classification) && ext) {
    const ok = (f.risk_findings || []).some(r => SEV[r.severity] >= 3);
    if (!ok) q.push(`${P}: classified flow exits trust boundary without a >=medium risk finding`);
  }
  if (f.crosses_system_boundary === true && !(f.risk_findings || []).length) q.push(`${P}: crosses_system_boundary with no risk findings`);
});
// duplicate-store detection -> cross_flow_findings must be populated
const locs = {};
doc.flows.forEach(f => (f.persistence_points || []).forEach(p => {
  (locs[p.location] = locs[p.location] || new Set()).add(f.flow_id);
}));
const shared = Object.entries(locs).filter(([, s]) => s.size >= 2);
if (shared.length && !(doc.cross_flow_findings || []).length) q.push('shared persistence locations but cross_flow_findings empty');
// all referenced flow ids exist
(doc.cross_flow_findings || []).forEach((c, i) => c.flows_involved.forEach(x => {
  if (!ids.has(x)) q.push(`cross_flow_findings[${i}] references unknown flow ${x}`);
}));

console.log(`flows=${doc.flows.length} cross_flow_findings=${(doc.cross_flow_findings || []).length}`);
console.log(`transformations=${doc.flows.reduce((n, f) => n + f.transformations.length, 0)} ` +
  `implicit=${doc.flows.reduce((n, f) => n + f.transformations.filter(t => t.implicit).length, 0)} ` +
  `risk_findings=${doc.flows.reduce((n, f) => n + (f.risk_findings || []).length, 0)}`);
console.log(`shared persistence locations (>=2 flows): ${shared.length}`);
console.log(errors.length ? `\nSCHEMA ERRORS (${errors.length}):\n` + errors.join('\n') : '\nSCHEMA: 0 errors');
console.log(q.length ? `\nQUALITY-RULE ISSUES (${q.length}):\n` + q.join('\n') : 'QUALITY RULES: 0 issues');
process.exit(errors.length || q.length ? 1 : 0);
