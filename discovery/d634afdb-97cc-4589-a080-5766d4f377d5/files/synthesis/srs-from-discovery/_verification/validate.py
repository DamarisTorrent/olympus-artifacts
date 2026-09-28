import json, os, sys, collections

D = "/workspace/discovery-d634afdb-97cc-4589-a080-5766d4f377d5-01a0e90cffd0/artifacts/discovery-srs-from-discovery"
FILES = ["srs.json","srs-requirements-functional.json","srs-requirements-nonfunctional.json",
         "srs-data-model.json","srs-accessibility-compliance.json","srs-anomaly-resolution-log.json"]
docs = {}
errs, warns = [], []

# 1. parse
for f in FILES:
    p = os.path.join(D,f)
    if not os.path.exists(p):
        errs.append("MISSING FILE: %s" % f); continue
    try:
        docs[f] = json.load(open(p))
        print("parsed OK  %-42s %8d bytes" % (f, os.path.getsize(p)))
    except Exception as e:
        errs.append("JSON PARSE FAIL %s: %s" % (f,e))
if errs:
    print("\n".join(errs)); sys.exit(1)

APP = "d634afdb-97cc-4589-a080-5766d4f377d5"
srs = docs["srs.json"]
fn  = docs["srs-requirements-functional.json"]
nf  = docs["srs-requirements-nonfunctional.json"]
dm  = docs["srs-data-model.json"]
ac  = docs["srs-accessibility-compliance.json"]
al  = docs["srs-anomaly-resolution-log.json"]

# 2. required top-level keys per bound schemas
def req(doc,name,keys):
    for k in keys:
        if k not in doc: errs.append("%s: missing required key '%s'" % (name,k))
req(srs,"srs.json",["application_id","modules","actors","traceability_matrix","anomaly_resolution_log_summary"])
req(fn,"functional",["requirements"]); req(nf,"nonfunctional",["requirements"])
req(dm,"data-model",["application_id","entities"])
req(ac,"accessibility",["application_id","prescribed_standard","conformance_target","findings"])
req(al,"anomaly-log",["application_id","total","anomalies"])

# 3. app id verbatim everywhere
for f,d in docs.items():
    if "application_id" in d and d["application_id"] != APP:
        errs.append("%s: application_id not verbatim: %r" % (f,d["application_id"]))

# 4. null-in-optional check (schemas forbid null unless declared)
def scan_nulls(o,path,f):
    if isinstance(o,dict):
        for k,v in o.items():
            if v is None: warns.append("%s: null value at %s.%s" % (f,path,k))
            else: scan_nulls(v,path+"."+k,f)
    elif isinstance(o,list):
        for i,v in enumerate(o):
            if v is None: warns.append("%s: null element at %s[%d]" % (f,path,i))
            else: scan_nulls(v,"%s[%d]"%(path,i),f)
for f,d in docs.items(): scan_nulls(d,"$",f)

# 5. per-requirement required fields + modal verb
MODALS = ("MUST","SHALL","SHOULD","MAY")
allreqs = {}
for label,doc in (("functional",fn),("nonfunctional",nf)):
    rs = doc["requirements"]
    if len(rs) < 1: errs.append("%s: requirements must have minItems 1" % label)
    for r in rs:
        for k in ("id","description","traces_to","acceptance_criteria"):
            if k not in r: errs.append("%s %s: missing required '%s'" % (label,r.get("id","?"),k))
        rid = r.get("id")
        if rid in allreqs: errs.append("duplicate requirement id %s" % rid)
        allreqs[rid] = (label,r)
        if not any(m in r.get("description","") for m in MODALS):
            errs.append("%s %s: description has no modal verb" % (label,rid))
        ac_ = r.get("acceptance_criteria")
        if isinstance(ac_,list) and len(ac_) < 1: errs.append("%s: empty acceptance_criteria" % rid)
        tt = r.get("traces_to")
        if isinstance(tt,dict) and len(tt) < 1: errs.append("%s: empty traces_to object" % rid)
print("\nrequirements parsed: %d functional-file + %d nonfunctional-file = %d"
      % (len(fn["requirements"]), len(nf["requirements"]), len(allreqs)))

# 6. reconcile functional totals
ft = fn["totals"]
byt = collections.Counter(r.get("type") for r in fn["requirements"])
byp = collections.Counter(r.get("priority") for r in fn["requirements"])
bym = collections.Counter(r.get("module_hint") for r in fn["requirements"])
bya = collections.Counter(r["anomaly_resolution"] for r in fn["requirements"] if "anomaly_resolution" in r)
def chk(label,claim,actual):
    if claim != actual: errs.append("COUNT MISMATCH %s: claims %r actual %r" % (label,claim,actual))
chk("fn.totals.total", ft["total"], len(fn["requirements"]))
chk("fn.by_type", {k:v for k,v in ft["by_type"].items() if v}, {k:v for k,v in byt.items() if v})
chk("fn.by_priority", {k:v for k,v in ft["by_priority"].items() if v}, dict(byp))
chk("fn.by_module", ft["by_module"], dict(bym))
chk("fn.by_anomaly_resolution", ft["by_anomaly_resolution"], dict(bya))
chk("fn.with_anomaly_resolution", ft["with_anomaly_resolution"], sum(bya.values()))
chk("fn.without_anomaly_resolution", ft["without_anomaly_resolution"], len(fn["requirements"])-sum(bya.values()))

# 7. reconcile nonfunctional totals
nt = nf["totals"]
nbyp = collections.Counter(r.get("priority") for r in nf["requirements"])
nbym = collections.Counter(r.get("module_hint") for r in nf["requirements"])
nbya = collections.Counter(r["anomaly_resolution"] for r in nf["requirements"] if "anomaly_resolution" in r)
chk("nf.totals.total", nt["total"], len(nf["requirements"]))
chk("nf.by_priority", {k:v for k,v in nt["by_priority"].items() if v}, dict(nbyp))
chk("nf.by_module", nt["by_module"], dict(nbym))
chk("nf.by_anomaly_resolution", nt["by_anomaly_resolution"], dict(nbya))

# 8. reconcile srs.json summary
s = srs["summary"]
chk("summary.total_requirements", s["total_requirements"], len(allreqs))
chk("summary.total_functional", s["total_functional"], byt.get("functional",0))
chk("summary.total_constraints", s["total_constraints"], byt.get("constraint",0))
chk("summary.total_non_functional", s["total_non_functional"], len(nf["requirements"]))
chk("summary.total_must", s["total_must"], byp.get("must",0)+nbyp.get("must",0))
chk("summary.total_should", s["total_should"], byp.get("should",0)+nbyp.get("should",0))
chk("summary.total_modules", s["total_modules"], len(srs["modules"]))
chk("summary.total_actors", s["total_actors"], len(srs["actors"]))
chk("summary.total_state_machines", s["total_state_machines"], len(srs["state_machines"]))
chk("summary.total_data_entities", s["total_data_entities"], len(dm["entities"]))
combined_mod = collections.Counter(bym); combined_mod.update(nbym)
chk("summary.requirements_per_module", s["requirements_per_module"], dict(combined_mod))
chk("summary.requirements_per_module sum", sum(s["requirements_per_module"].values()), len(allreqs))

# 9. state machine states/transitions totals + reachability
tot_states = tot_trans = tot_dead = 0
for sm in srs["state_machines"]:
    for k in ("entity","states"):
        if k not in sm: errs.append("state machine missing '%s'" % k)
    names = [st["name"] for st in sm["states"]]
    if len(sm["states"]) < 1: errs.append("%s: states minItems 1" % sm.get("entity"))
    tot_states += len(names)
    trs = sm.get("transitions",[])
    tot_trans += len(trs)
    tot_dead += len(sm.get("dead_states_removed",[]))
    for t in trs:
        for end in ("from","to"):
            if t[end] not in names:
                errs.append("%s: transition %s=%r not a declared state" % (sm["name"],end,t[end]))
    init = sm.get("initial_state")
    if init and init not in names: errs.append("%s: initial_state %r not declared" % (sm["name"],init))
    for ts in sm.get("terminal_states",[]):
        if ts not in names: errs.append("%s: terminal_state %r not declared" % (sm["name"],ts))
    # reachability from initial
    reach={init}; changed=True
    while changed:
        changed=False
        for t in trs:
            if t["from"] in reach and t["to"] not in reach:
                reach.add(t["to"]); changed=True
    unreach = set(names)-reach
    if unreach: warns.append("%s: states unreachable from initial_state: %s" % (sm["name"],sorted(unreach)))
    # non-terminal states must have an exit
    term=set(sm.get("terminal_states",[]))
    for n in names:
        if n not in term and not any(t["from"]==n for t in trs):
            warns.append("%s: non-terminal state %r has no exit transition" % (sm["name"],n))
chk("summary.total_states", s["total_states"], tot_states)
chk("summary.total_transitions", s["total_transitions"], tot_trans)
chk("summary.total_dead_states_removed", s["total_dead_states_removed"], tot_dead)

# 10. anomaly log reconciliation
an = al["anomalies"]
chk("al.total", al["total"], len(an))
aba = collections.Counter(a["action"] for a in an)
chk("al.by_action", al["by_action"], dict(aba))
abt = collections.Counter(a.get("type") for a in an)
chk("al.by_type", al["by_type"], dict(abt))
abs_ = collections.Counter(a.get("discovery_source",{}).get("artifact") for a in an)
chk("al.by_source", al["by_source"], dict(abs_))
chk("index.anomaly.by_source", srs["anomaly_resolution_log_summary"]["by_source"], dict(abs_))
for lbl,mp in (("al.by_action",al["by_action"]),("al.by_type",al["by_type"]),("al.by_source",al["by_source"])):
    chk(lbl+" sums to total", sum(mp.values()), len(an))
sme_flagged = sorted(a["anomaly_id"] for a in an if a.get("sme_confirmation_required"))
chk("al.sme_confirmation_required list", sorted(al["sme_confirmation_required"]), sme_flagged)
chk("summary.total_sme_confirmations_required", s["total_sme_confirmations_required"], len(sme_flagged))
deferred = sorted(a["anomaly_id"] for a in an if a["action"]=="DEFER")
chk("al.verification.deferred", sorted(al["verification"]["deferred_anomalies"]), deferred)
chk("summary.total_anomalies_deferred", s["total_anomalies_deferred"], len(deferred))
chk("summary.total_anomalies_resolved", s["total_anomalies_resolved"], len(an)-len(deferred))
chk("summary.total_anomalies", s["total_anomalies"], len(an))
for a in an:
    for k in ("anomaly_id","action"):
        if k not in a: errs.append("anomaly missing '%s'" % k)
    if a["action"]=="DEFER" and not a.get("justification"):
        errs.append("%s: DEFER without justification" % a["anomaly_id"])
    if a["action"]=="DEFER" and not a.get("sme_question"):
        errs.append("%s: DEFER without a named human decision" % a["anomaly_id"])
# index summary mirrors log
ix = srs["anomaly_resolution_log_summary"]
chk("index.anomaly.total", ix["total"], len(an))
chk("index.anomaly.by_action", ix["by_action"], dict(aba))
chk("index.anomaly.by_type", ix["by_type"], dict(abt))
chk("index.anomaly.deferred", ix["deferred"], len(deferred))
chk("index.anomaly.sme count", len(ix["sme_confirmation_required"]), len(sme_flagged))

# 11. every proposed_anomaly referenced exists; every anomaly's affected_requirements exist
anom_ids = {a["anomaly_id"] for a in an}
for rid,(lab,r) in allreqs.items():
    pa = r.get("proposed_anomaly")
    if pa and pa not in anom_ids: errs.append("%s cites unknown anomaly %s" % (rid,pa))
    for rr in r.get("related_requirements",[]):
        if rr not in allreqs: errs.append("%s related_requirements cites unknown %s" % (rid,rr))
for a in an:
    for rr in a.get("affected_requirements",[]):
        if rr not in allreqs: errs.append("%s affected_requirements cites unknown %s" % (a["anomaly_id"],rr))

# 12. traceability: BR/IL mappings point at real requirements; coverage numbers true
tm = srs["traceability_matrix"]["discovery_to_srs"]
brmap = tm["business_rules"]["mapping"]
chk("BR mapping size", tm["business_rules"]["total"], len(brmap))
covered_br = [k for k,v in brmap.items() if v]
chk("BR with_requirements", tm["business_rules"]["with_requirements"], len(covered_br))
ilmap = tm["implicit_logic_entries"]["mapping"]
chk("IL mapping size", tm["implicit_logic_entries"]["total"], len(ilmap))
cov_il = [k for k,v in ilmap.items() if v]
chk("IL with_requirements", tm["implicit_logic_entries"]["with_requirements"], len(cov_il))
chk("IL deferred", tm["implicit_logic_entries"]["deferred"], len(ilmap)-len(cov_il))
for label,mp in (("BR",brmap),("IL",ilmap),("QR",tm["code_smells"]["mapping"]),
                 ("BV",tm["data_domain_violations"]["mapping"]),("MG",tm["measurement_gaps"]["mapping"]),
                 ("IF",tm["interfaces"]["mapping"])):
    for k,v in mp.items():
        for rr in v:
            if rr not in allreqs and not rr.startswith("MOD-"):
                errs.append("%s mapping %s -> unknown requirement %s" % (label,k,rr))
cov = srs["traceability_matrix"]["coverage"]
chk("coverage.business_rules_covered", cov["business_rules_covered"], len(covered_br))
chk("coverage.implicit_logic_covered", cov["implicit_logic_covered"], len(cov_il))
chk("srs_to_discovery.total_requirements", srs["traceability_matrix"]["srs_to_discovery"]["total_requirements"], len(allreqs))
# every BR-001..024 + MISSING present
expect_br = set("BR-%03d"%i for i in range(1,25)) | {"BR-MISSING-001"}
if set(brmap) != expect_br: errs.append("BR mapping key set wrong; missing %s extra %s"
    % (sorted(expect_br-set(brmap)), sorted(set(brmap)-expect_br)))
expect_il = set("IL-%03d"%i for i in range(1,28))
if set(ilmap) != expect_il: errs.append("IL mapping key set wrong; missing %s extra %s"
    % (sorted(expect_il-set(ilmap)), sorted(set(ilmap)-expect_il)))

# 13. detail_files all exist and all written files are declared
declared = set(srs.get("detail_files",{}).values())
ondisk = set(f for f in FILES if f != "srs.json")
if declared != ondisk:
    errs.append("detail_files mismatch: undeclared-on-disk %s / declared-missing %s"
                % (sorted(ondisk-declared), sorted(declared-ondisk)))
chk("anomaly detail pointer", ix.get("detail"), "srs-anomaly-resolution-log.json")

# 14. modules: requirement_count matches module_hint tallies; referenced entities/machines exist
ent_names = {e["entity"] for e in dm["entities"]}
sm_names  = {m.get("name") for m in srs["state_machines"]}
actor_names = {a["name"] for a in srs["actors"]}
for m in srs["modules"]:
    for k in ("id","name"):
        if k not in m: errs.append("module missing '%s'" % k)
    chk("module %s requirement_count" % m["id"], m["requirement_count"], combined_mod.get(m["id"],0))
    for e in m.get("data_entities",[]):
        if e not in ent_names: errs.append("module %s cites unknown entity %s" % (m["id"],e))
    for x in m.get("state_machines",[]):
        if x not in sm_names: errs.append("module %s cites unknown state machine %s" % (m["id"],x))
    for a in m.get("actor_names",[]):
        if a not in actor_names: errs.append("module %s cites unknown actor %s" % (m["id"],a))
mod_ids = {m["id"] for m in srs["modules"]}
for rid,(lab,r) in allreqs.items():
    mh = r.get("module_hint")
    if mh and mh not in mod_ids: errs.append("%s module_hint %s not a declared module" % (rid,mh))
for a in srs["actors"]:
    if "name" not in a: errs.append("actor missing name")
    for mm in a.get("modules",[]):
        if mm not in mod_ids: errs.append("actor %s cites unknown module %s" % (a.get("name"),mm))

# 15. data model + accessibility internal checks
for e in dm["entities"]:
    if "entity" not in e: errs.append("data entity missing 'entity'")
    for rel in e.get("relationships",[]):
        t = rel.get("target_entity")
        if t and t not in ent_names: errs.append("entity %s relationship -> unknown %s" % (e["entity"],t))
    for c in e.get("constraints",[]):
        for g in c.get("governed_by",[]):
            if g not in allreqs: errs.append("entity %s constraint governed_by unknown %s" % (e["entity"],g))
    for at in e.get("attributes",[]):
        for g in at.get("governed_by",[]):
            if g not in allreqs: errs.append("entity %s attr %s governed_by unknown %s" % (e["entity"],at.get("name"),g))
dms = dm["summary"]
chk("dm.total_entities_prescribed", dms["total_entities_prescribed"], len(dm["entities"]))
n_attrs = sum(len(e.get("attributes",[])) for e in dm["entities"])
chk("dm.total_attributes_prescribed", dms["total_attributes_prescribed"], n_attrs)
chk("dm attribute provenance split sums to total",
    dms["attributes_derived_from_a_legacy_source_line"] + dms["attributes_prescribed_without_a_legacy_counterpart"],
    n_attrs)
chk("dm.total_constraints", dms["total_constraints"], sum(len(e.get("constraints",[])) for e in dm["entities"]))
chk("dm.legacy_not_carried_forward", dms["legacy_entities_not_carried_forward"], len(dm["legacy_entities_not_carried_forward"]))
for f_ in ac["findings"]:
    for k in ("id","wcag","level"):
        if k not in f_: errs.append("a11y finding missing '%s'" % k)
    for g in f_.get("governed_by",[]):
        if g not in allreqs: errs.append("a11y %s governed_by unknown %s" % (f_["id"],g))
acs = ac["summary"]
chk("ac.open_findings_count", acs["open_findings_count"], len(ac["findings"]))
chk("ac.verified_non_issues_count", acs["verified_non_issues_count"], len(ac["verified_non_issues"]))
chk("ac.unassessed_gaps_count", acs["unassessed_gaps_count"], len(ac["unassessed_gaps"]))
chk("summary.total_accessibility_findings_open", s["total_accessibility_findings_open"], len(ac["findings"]))
chk("summary.total_open_questions", s["total_open_questions"], len(srs["open_questions"]))
if "method" not in ac["baseline_posture"]: errs.append("accessibility baseline_posture missing 'method'")

# 16. the six intentional requirement-vs-anomaly action divergences are declared, not accidental
DECLARED_DIVERGENCES = {"REQ-005","REQ-022","NFR-004","NFR-005","NFR-007","NFR-009"}
anom_action = {a["anomaly_id"]: a["action"] for a in an}
actual_div = set()
for rid,(lab,r) in allreqs.items():
    pa, ra = r.get("proposed_anomaly"), r.get("anomaly_resolution")
    if pa and ra and anom_action.get(pa) != ra: actual_div.add(rid)
if actual_div != DECLARED_DIVERGENCES:
    errs.append("requirement-vs-anomaly action divergence set changed: undeclared %s / declared-but-absent %s"
                % (sorted(actual_div-DECLARED_DIVERGENCES), sorted(DECLARED_DIVERGENCES-actual_div)))
else:
    print("the 6 requirement-vs-anomaly action divergences match the declared set")
if "granularity_warning" not in srs["anomaly_resolution_log_summary"]:
    errs.append("srs.json anomaly summary missing granularity_warning")
if "requirement_action_vs_anomaly_action" not in al["verification"]:
    errs.append("anomaly log verification missing requirement_action_vs_anomaly_action")

# 17. IL sme flag count agrees with its own enumeration
sc = al["verification"]["source_coverage"]
chk("IL sme flagged count vs enumeration",
    sc["implicit_logic_flagged_requires_sme_review"], len(sc["implicit_logic_sme_flagged_ids"]))

print("\n" + "="*72)
if warns:
    print("WARNINGS (%d):" % len(warns))
    for w in warns: print("  ~", w)
if errs:
    print("\nERRORS (%d):" % len(errs))
    for e in errs: print("  X", e)
    sys.exit(1)
print("ALL CHECKS PASSED — 6 files, %d requirements, %d anomalies, %d state machines, %d entities"
      % (len(allreqs), len(an), len(srs["state_machines"]), len(dm["entities"])))
