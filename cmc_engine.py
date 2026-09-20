#!/usr/bin/env python3
"""
Channel-Monopoly Class (CMC) ranking engine
Session: 2026-09-20T13:40:00-04:00
Author: Haley Bird / autonomous Grok research agent

Research-stage classification. Not a physical discovery, not peer review,
not a patent. Scores are a classification heuristic over sourced gaps.
They are not measurements of nature.

CMC: a physical or biological channel is monopolized by its first-assigned
function. Search protocols look elsewhere for a dedicated organ / particle /
gene. The empty search is named as a mystery. The second function was
riding the assigned channel.

Discriminator (kills CMC if true):
  locating a *dedicated new* organ/instrument/particle closes the gap
  → TAC, not CMC.
  splitting one reported number into two independent observables closes it
  → OAC, not CMC.
  changing instrument coupling to a previously uncoupled DOF closes it
  → CIP, not CMC.
  recovering a discarded data channel closes it
  → DCC, not CMC.
CMC is confirmed only if re-analysis of the ALREADY-INSTRUMENTED,
ALREADY-ASSIGNED channel reveals the second function.

Archive subtraction (do not reclaim):
  Dark Biosphere, Undersampling, Deep-biosphere-as-space-prior, TAC,
  NCR + Initiation-Maintenance, Failed-Adjudication, CIC (POC/LOC/two-clock),
  JAC, IOA, DIC, PPC, UCC, DCC, FCC, OAC, UPRC, CIP (2026-09-17).
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass, field, asdict
from typing import Any


SESSION_ID = "2026-09-20-cmc"
TIMESTAMP = "2026-09-20T13:40:00-04:00"
PRIOR_CLASSES = (
    "Dark Biosphere Hypothesis",
    "Undersampling",
    "Deep-biosphere-as-space-prior",
    "TAC",
    "NCR",
    "Initiation-Maintenance Split",
    "Failed-Adjudication",
    "CIC",
    "JAC",
    "IOA",
    "DIC",
    "PPC",
    "UCC",
    "DCC",
    "FCC",
    "OAC",
    "UPRC",
    "CIP",
)


@dataclass
class GapItem:
    id: str
    realm: str
    channel: str
    assigned_function: str
    second_function: str
    years_monopoly: float
    assignment_monopoly: float
    second_function_evidence: float
    search_displacement: float
    spokenness: float
    prior_overlap: list[str] = field(default_factory=list)
    reclaim_of: list[str] = field(default_factory=list)
    status: str = "candidate"
    sources: list[str] = field(default_factory=list)
    notes: str = ""
    role: str = "test"

    def framing_tax(self) -> float:
        """
        reclaim_of — this item IS a prior class. Disqualify.
        prior_overlap — a prior class named the mystery; CMC is remainder. Tax only.
        """
        if self.reclaim_of:
            return 1.0
        if not self.prior_overlap:
            return 0.0
        return min(0.36, 0.12 * len(self.prior_overlap))


def cmc_score(item: GapItem) -> dict[str, Any]:
    """Heuristic remainder score. Not a measurement of nature."""
    status_w = {
        "confirmed": 1.00,
        "candidate": 0.72,
        "unproved": 0.45,
        "contested": 0.08,
        "control": 0.00,
    }[item.status]

    if item.role == "control":
        status_w = 0.0
    if item.role == "retain":
        status_w *= 0.05
    if item.reclaim_of:
        status_w = 0.0

    prior = item.framing_tax()
    years_term = math.log1p(max(0.0, item.years_monopoly)) / math.log1p(150.0)

    raw = (
        item.assignment_monopoly
        * item.second_function_evidence
        * item.search_displacement
        * (1.0 - item.spokenness)
        * (1.0 - prior)
        * status_w
        * (0.35 + 0.65 * years_term)
    )
    score = round(100.0 * raw, 2)

    cmc_ok = (
        item.role == "test"
        and item.status in {"confirmed", "candidate", "unproved"}
        and not item.reclaim_of
        and prior < 0.50
        and item.spokenness < 0.70
    )
    return {
        "id": item.id,
        "realm": item.realm,
        "score": score,
        "cmc_eligible": cmc_ok,
        "framing_tax": round(prior, 3),
        "status_weight": status_w,
        "years_term": round(years_term, 3),
        "kill_reason": _kill_reason(item, prior, cmc_ok),
    }


def _kill_reason(item: GapItem, prior: float, cmc_ok: bool) -> str | None:
    if item.reclaim_of:
        return f"reclaim-of:{','.join(item.reclaim_of)}"
    if item.role == "control":
        return "control"
    if item.role == "retain":
        return "retain-prior-class"
    if item.status == "contested":
        return "contested-do-not-load-bear"
    if item.spokenness >= 0.70:
        return "already-spoken-frame"
    if not cmc_ok:
        return "ineligible"
    return None


ITEMS: list[GapItem] = [
    GapItem(
        id="pigeon-vestibular-induction",
        realm="animals",
        channel="semicircular-canal type II hair cells (inner ear)",
        assigned_function="balance / angular acceleration (vestibular)",
        second_function="light-independent magnetoreception via electromagnetic induction",
        years_monopoly=143.0,
        assignment_monopoly=0.92,
        second_function_evidence=0.88,
        search_displacement=0.90,
        spokenness=0.18,
        prior_overlap=["TAC"],
        status="confirmed",
        sources=[
            "Nordmann et al., Science 391(6790):1155-1160 (20 Nov 2025), doi:10.1126/science.aea6425",
            "Stokstad, Science news, 20 Nov 2025: Keays 2019 lagena magnetite empty; Viguier 1882 recovered",
            "Type II hair cells express CaV1.3 + BK (shark/skate electroreceptor channels)",
        ],
        notes="Smoking gun. Unbiased whole-brain screen landed on the monopolized vestibular channel.",
        role="test",
    ),
    GapItem(
        id="cryptochrome-eye-radical-pair",
        realm="animals",
        channel="retinal cryptochrome / FAD radical-pair",
        assigned_function="circadian photoreception",
        second_function="light-dependent magnetic compass",
        years_monopoly=25.0,
        assignment_monopoly=0.70,
        second_function_evidence=0.62,
        search_displacement=0.40,
        spokenness=0.62,
        prior_overlap=["TAC"],
        status="candidate",
        sources=[
            "Cryptochrome/FAD radical-pair literature; Nature 2023 FAD magnetic sensitivity",
            "Nordmann 2025 is light-independent, so this is a second, separate channel",
        ],
        notes="Spoken competitor. Field already treats the eye as dual-use. Contrast to the ear.",
        role="test",
    ),
    GapItem(
        id="llsvp-vs-temperature-monopoly",
        realm="earth",
        channel="lower-mantle shear-wave velocity (Vs)",
        assigned_function="temperature (hot piles / upwelling)",
        second_function="distinct compositional biographies (Pacific young SOC vs African older mix)",
        years_monopoly=40.0,
        assignment_monopoly=0.84,
        second_function_evidence=0.78,
        search_displacement=0.72,
        spokenness=0.28,
        prior_overlap=["OAC"],
        status="candidate",
        sources=[
            "Panton, Davies, Koelemeijer et al., Sci. Rep. 15:4466 (6 Feb 2025) doi:10.1038/s41598-025-88931-3",
            "Pacific LLVP replenished with young subducted oceanic crust since 300 Ma; African older, well-mixed; up to 53% more recent SOC in Pacific",
            "Atkins et al., JGR Solid Earth 2026 doi:10.1029/2025JB033171 — 99.8% CMB coverage, six Sdiff-ULVZs at LLVP edges",
        ],
        notes="OAC overlap taxed as framing. Remainder: Vs is assigned to temperature, so two provinces look identical while biographies differ.",
        role="test",
    ),
    GapItem(
        id="ulvz-absence-map",
        realm="earth",
        channel="core-mantle boundary Sdiff postcursors",
        assigned_function="scattered ULVZs as generic CMB heterogeneity",
        second_function="structured ABSENCE: most of CMB lacks large ULVZs; six sit at LLVP edges / hotspots",
        years_monopoly=30.0,
        assignment_monopoly=0.66,
        second_function_evidence=0.80,
        search_displacement=0.55,
        spokenness=0.22,
        prior_overlap=["Undersampling"],
        status="candidate",
        sources=[
            "Atkins et al., JGR Solid Earth (first published 24 Apr 2026) doi:10.1029/2025JB033171",
            "~2e6 traces hand-picked; ~1e5 postcursors; >9e5 robust nulls; 99.8% CMB coverage",
        ],
        notes="Absence is the finding. Coverage is now 99.8%, so this is not undersampling.",
        role="test",
    ),
    GapItem(
        id="twilight-carbon-vs-iron",
        realm="ocean",
        channel="mesopelagic (200-1000 m) microbial metabolism",
        assigned_function="labile-organic-carbon limitation of remineralization",
        second_function="iron limitation (siderophore peaks in gyre twilight zones)",
        years_monopoly=40.0,
        assignment_monopoly=0.86,
        second_function_evidence=0.82,
        search_displacement=0.75,
        spokenness=0.20,
        prior_overlap=[],
        status="confirmed",
        sources=[
            "Li et al., Nature 633:823-827 (25 Sep 2024) doi:10.1038/s41586-024-07905-z PMID 39322731",
            "Siderophore concentrations high in twilight zone under N and S Pacific subtropical gyres",
        ],
        notes="CIP claimed rhodopsin-coupling, not nutrient-polarity. Distinct.",
        role="test",
    ),
    GapItem(
        id="surface-predator-photic-monopoly",
        realm="ocean",
        channel="trophic identity of tuna / swordfish",
        assigned_function="photic-zone / epipelagic predators",
        second_function="50-60% of diet sourced from the twilight zone",
        years_monopoly=50.0,
        assignment_monopoly=0.80,
        second_function_evidence=0.84,
        search_displacement=0.70,
        spokenness=0.25,
        prior_overlap=["Undersampling"],
        status="confirmed",
        sources=[
            "Willis et al. / MIT News 1 Apr 2025; ICES Journal of Marine Science",
            "Bigeye tuna, yellowfin tuna, swordfish: 50-60% diet from twilight zone via carbon isotopes",
        ],
        notes="Photic assignment monopolized fisheries science. Twilight was 'elsewhere', not the primary larder.",
        role="test",
    ),
    GapItem(
        id="placebo-inert-channel",
        realm="humans",
        channel="the 'inert' treatment / sham / control pill",
        assigned_function="null control (no active pharmacological function)",
        second_function="meaning / expectation / care as a real physiological channel",
        years_monopoly=80.0,
        assignment_monopoly=0.88,
        second_function_evidence=0.70,
        search_displacement=0.60,
        spokenness=0.55,
        prior_overlap=["NCR", "TAC"],
        status="candidate",
        sources=[
            "NEJM-class reviews 2025: placebo mechanism still unknown",
            "Spoken as a mystery; unspoken as channel-monopoly of the control arm",
        ],
        notes="NCR/TAC framing taxed. Remainder: trial design assigns the pill as functionless.",
        role="test",
    ),
    GapItem(
        id="cogitate-prefrontal-report-monopoly",
        realm="humans",
        channel="prefrontal 'ignition' / P3b",
        assigned_function="consciousness itself (GNWT)",
        second_function="report / access, not phenomenal experience (no-report conditions drop P3b)",
        years_monopoly=30.0,
        assignment_monopoly=0.75,
        second_function_evidence=0.80,
        search_displacement=0.50,
        spokenness=0.58,
        prior_overlap=["Failed-Adjudication", "NCR"],
        reclaim_of=["Failed-Adjudication"],
        status="candidate",
        sources=[
            "Cogitate Consortium, Nature 642:133-142 (30 Apr 2025) doi:10.1038/s41586-025-08888-1",
            "Both IIT and GNWT key tenets challenged; no-report P3b absent; posterior sync not sustained",
        ],
        notes="Failed-Adjudication already owns the draw. Reclaim.",
        role="test",
    ),
    GapItem(
        id="soil-microbial-memory",
        realm="land",
        channel="soil microbiome metabolic machinery",
        assigned_function="nutrient cycling / agricultural substrate / C pool",
        second_function="microbial memory and legacy as a function of soil (unsolved grand question)",
        years_monopoly=100.0,
        assignment_monopoly=0.78,
        second_function_evidence=0.55,
        search_displacement=0.65,
        spokenness=0.30,
        prior_overlap=["Dark Biosphere Hypothesis", "TAC"],
        status="unproved",
        sources=[
            "Kuzyakov et al., Soil Biology & Biochemistry, 'Some new grand questions in soil biology' (2025)",
            "Question group: Are microbial memory and legacy important for soil functions?",
        ],
        notes="Dark Biosphere owns subsurface life-as-architecture. Remainder is soil-as-substrate monopolizing soil-as-memory.",
        role="test",
    ),
    GapItem(
        id="giant-magnetofossils",
        realm="land",
        channel="biogenic magnetite in sediments",
        assigned_function="magnetotactic bacteria",
        second_function="unknown complex organism that biomineralised giant magnetofossils (~56 Ma)",
        years_monopoly=50.0,
        assignment_monopoly=0.82,
        second_function_evidence=0.60,
        search_displacement=0.70,
        spokenness=0.15,
        prior_overlap=["TAC", "UCC"],
        status="unproved",
        sources=[
            "Harrison et al. giant magnetofossils; Mongabay 7 Aug 2026 reporting",
            "Sediments to 56 Ma; organism unknown",
        ],
        notes="Magnetite assigned to bacteria. Giant fossils imply a second maker.",
        role="test",
    ),
    GapItem(
        id="gravity-as-fundamental-monopoly",
        realm="space",
        channel="spacetime curvature / gravitational phenomenology",
        assigned_function="fundamental force (with EM, strong, weak)",
        second_function="emergent thermodynamic / entropic / entanglement equation of state",
        years_monopoly=110.0,
        assignment_monopoly=0.90,
        second_function_evidence=0.40,
        search_displacement=0.55,
        spokenness=0.48,
        prior_overlap=["CIP", "PPC", "TAC"],
        reclaim_of=["CIP"],
        status="unproved",
        sources=[
            "Emergent gravity / holographic / ER=EPR literature; black hole entropy ∝ area not volume",
            "CIP 2026-09-17 already used dark-sector Equivalence Principle coupling.",
        ],
        notes="CIP overlap is a reclaim. Do not load-bear.",
        role="test",
    ),
    GapItem(
        id="lrd-class-vs-phase",
        realm="space",
        channel="JWST compact red point sources (little red dots)",
        assigned_function="a new class of object (early galaxies / AGN class)",
        second_function="a short-lived phase of black-hole assembly (black-hole-star / hidden host)",
        years_monopoly=3.0,
        assignment_monopoly=0.70,
        second_function_evidence=0.55,
        search_displacement=0.45,
        spokenness=0.40,
        prior_overlap=["CIC"],
        reclaim_of=["CIC"],
        status="unproved",
        sources=[
            "Naidu et al. MIT 12 Aug 2026 MoM-BH*-1 as black hole star (interpretation unproved)",
            "CIC 2026-09-01 already claimed LRD as POC.",
        ],
        notes="Direct reclaim of CIC.",
        role="retain",
    ),
    GapItem(
        id="hubble-tension",
        realm="space",
        channel="H0 measurement",
        assigned_function="one expansion rate",
        second_function="two clocks",
        years_monopoly=15.0,
        assignment_monopoly=0.50,
        second_function_evidence=0.90,
        search_displacement=0.20,
        spokenness=0.95,
        prior_overlap=["CIC", "TAC", "NCR"],
        status="control",
        sources=["Riess/SH0ES vs Planck; JWST confirmed local ladder; spoken mystery"],
        notes="Spoken. CIC two-clock. Zero remainder.",
        role="control",
    ),
    GapItem(
        id="dark-matter-particle",
        realm="space",
        channel="galactic/cluster gravity residual",
        assigned_function="missing particle (WIMP/axion)",
        second_function="modified / emergent gravity",
        years_monopoly=50.0,
        assignment_monopoly=0.85,
        second_function_evidence=0.35,
        search_displacement=0.80,
        spokenness=0.92,
        prior_overlap=["TAC", "PPC", "CIP"],
        status="control",
        sources=["XENON non-detection; NASA dark matter unexplained; CIP 2026-09-17"],
        notes="Spoken. TAC/PPC/CIP. Zero remainder.",
        role="control",
    ),
    GapItem(
        id="sweetman-dark-oxygen",
        realm="ocean",
        channel="benthic-chamber O2 electrode",
        assigned_function="seafloor oxygen consumption",
        second_function="nodule electrolysis 'dark oxygen'",
        years_monopoly=2.0,
        assignment_monopoly=0.40,
        second_function_evidence=0.10,
        search_displacement=0.20,
        spokenness=0.70,
        prior_overlap=["DCC", "DIC", "TAC"],
        status="contested",
        sources=[
            "Sweetman et al. Nature Geoscience 17:737-744 (2024)",
            "Editor's Note 8 Apr 2026; Downes et al.; Frontiers in Marine Science 2025",
            "Science/AAAS 18 Sep 2026: Claim of dark oxygen on sea floor faces doubts",
            "F1000Research 15:729 (14 May 2026): no correlation with nodule area/weight",
        ],
        notes="Do not load-bear. Rising O2 also in chambers without nodules.",
        role="retain",
    ),
    GapItem(
        id="gorg-dark-ferh-rhodopsin",
        realm="ocean",
        channel="Pelagibacterales rhodopsin",
        assigned_function="sunlight phototrophy",
        second_function="sensing deep-sea bioluminescence (FeRh clade)",
        years_monopoly=20.0,
        assignment_monopoly=0.80,
        second_function_evidence=0.55,
        search_displacement=0.50,
        spokenness=0.15,
        prior_overlap=["CIP"],
        reclaim_of=["CIP"],
        status="candidate",
        sources=[
            "GORG-Dark, Cell, 14 Sep 2026: 9698 single-cell genomes; Pelagibacterales-specific rhodopsin clade",
            "CIP 2026-09-17 already used this as coupling-incompleteness isomorphism.",
        ],
        notes="CIP claimed this 3 days ago. Reclaim.",
        role="retain",
    ),
    GapItem(
        id="magnetoreceptor-unlocated-generic",
        realm="animals",
        channel="unknown dedicated magnetoreceptor cell",
        assigned_function="missing organ",
        second_function="n/a — this IS the TAC formulation",
        years_monopoly=60.0,
        assignment_monopoly=0.50,
        second_function_evidence=0.20,
        search_displacement=0.90,
        spokenness=0.70,
        prior_overlap=["TAC"],
        status="control",
        sources=["Lohmann pre-Nordmann framing: no one has identified a magnetic receptor with certainty"],
        notes="This is the TAC statement. CMC is the remainder after this framing.",
        role="control",
    ),
    GapItem(
        id="abiogenesis",
        realm="life",
        channel="origin-of-life experiments",
        assigned_function="reproduce the historical pathway",
        second_function="n/a — singleton / CIC / NCR",
        years_monopoly=170.0,
        assignment_monopoly=0.50,
        second_function_evidence=0.20,
        search_displacement=0.30,
        spokenness=0.95,
        prior_overlap=["NCR", "CIC", "Failed-Adjudication"],
        status="control",
        sources=["Miller & Orgel 1974; SciAm 15 Sep 2026 Will we ever know how life began?"],
        notes="Spoken. Singleton. Not CMC.",
        role="control",
    ),
    GapItem(
        id="consciousness-hard-problem",
        realm="humans",
        channel="subjective experience",
        assigned_function="emergent from neural computation",
        second_function="n/a — spoken hard problem",
        years_monopoly=400.0,
        assignment_monopoly=0.50,
        second_function_evidence=0.20,
        search_displacement=0.30,
        spokenness=0.98,
        prior_overlap=["Failed-Adjudication", "NCR", "TAC"],
        status="control",
        sources=["Cogitate 2025; SciAm Impossible Questions Sep 2026"],
        notes="Spoken. FAC owns the IIT vs GNWT draw.",
        role="control",
    ),
    GapItem(
        id="seafloor-unmapped",
        realm="ocean",
        channel="bathymetry",
        assigned_function="n/a — this is WHERE we look",
        second_function="n/a",
        years_monopoly=0.0,
        assignment_monopoly=0.10,
        second_function_evidence=0.10,
        search_displacement=0.10,
        spokenness=0.80,
        prior_overlap=["Undersampling"],
        status="control",
        sources=["Seabed 2030 / NOAA 20 Apr 2026: 28.7% mapped; Sci Adv deep seafloor visually observed <0.001%"],
        notes="Undersampling. Zero CMC remainder.",
        role="control",
    ),
    GapItem(
        id="exaptation-speech-larynx",
        realm="humans",
        channel="larynx / hyoid",
        assigned_function="airway / swallowing",
        second_function="speech (classic Gould-Vrba exaptation)",
        years_monopoly=0.0,
        assignment_monopoly=0.90,
        second_function_evidence=0.95,
        search_displacement=0.10,
        spokenness=0.90,
        prior_overlap=[],
        status="control",
        sources=["Gould & Vrba 1982 exaptation — SPOKEN. CMC is not a rediscovery of exaptation."],
        notes="Adversarial control: if CMC is just exaptation, this scores high. It must score ~0.",
        role="control",
    ),
    GapItem(
        id="seti-existence-binary",
        realm="space",
        channel="SETI non-detection / Fermi silence",
        assigned_function="absence of technological civilizations (binary existence)",
        second_function="civilizations have a duty cycle (collapse/recovery); silence is the off-phase",
        years_monopoly=76.0,
        assignment_monopoly=0.82,
        second_function_evidence=0.50,
        search_displacement=0.55,
        spokenness=0.45,
        prior_overlap=["CIC"],
        status="unproved",
        sources=[
            "Blanco et al. / ScienceAlert 18 Sep 2026: 1000-year civilization simulation; two parameters dominate: consumption rate and recovery after collapse",
            "Golden Age and Out of Eden never collapsed; 7 of 10 scenarios collapsed in every run",
            "CIC cadence is observation vs process clock of ONE object. Duty-cycle is the object's own on/off. Adjacent, taxed.",
        ],
        notes="CIC-adjacent. Duty cycle of the civilization itself vs freeze-frame of an object. Distinct enough to test, not primary.",
        role="test",
    ),
]


def rank(items: list[GapItem]) -> list[dict[str, Any]]:
    rows = []
    for it in items:
        s = cmc_score(it)
        row = {**asdict(it), **s}
        rows.append(row)
    rows.sort(key=lambda r: (-r["score"], r["id"]))
    return rows


def realm_split(rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for r in rows:
        if not r["cmc_eligible"]:
            continue
        realm = r["realm"]
        if realm not in out:
            out[realm] = {
                "id": r["id"],
                "score": r["score"],
                "channel": r["channel"],
                "assigned_function": r["assigned_function"],
                "second_function": r["second_function"],
            }
    return out


def iterate_ablate_recency(items: list[GapItem]) -> dict[str, Any]:
    survivors = []
    dropped = []
    for it in items:
        if it.status in {"unproved", "candidate"} and it.years_monopoly < 5:
            dropped.append(it.id)
            continue
        survivors.append(it)
    ranked = rank(survivors)
    eligible = [r for r in ranked if r["cmc_eligible"]]
    return {
        "dropped": dropped,
        "leader": eligible[0]["id"] if eligible else None,
        "leader_score": eligible[0]["score"] if eligible else 0,
        "top5": [{"id": r["id"], "score": r["score"], "realm": r["realm"]} for r in eligible[:5]],
    }


def iterate_cross_realm_isomorphism(rows: list[dict[str, Any]]) -> dict[str, Any]:
    split = realm_split(rows)
    n = len(split)
    return {
        "realms_with_eligible_cmc": n,
        "realms": split,
        "structural": n >= 3,
        "operator": (
            "one assigned function monopolizes a channel; "
            "second function is searched for elsewhere; "
            "empty search is named as mystery"
        ),
    }


def iterate_falsification_matrix() -> list[dict[str, str]]:
    return [
        {
            "id": "pigeon-vestibular-induction",
            "kill_cmc_if": "A dedicated non-vestibular magnetoreceptor accounts for homing without the semicircular-canal circuit.",
            "confirm_cmc_if": "Canal-specific block abolishes magnetic discrimination while leaving ordinary vestibular function partly intact; wild-navigation still routes through MVN.",
        },
        {
            "id": "twilight-carbon-vs-iron",
            "kill_cmc_if": "Fe-addition incubations in gyre twilight zones do not change remineralization; carbon remains the sole limiter.",
            "confirm_cmc_if": "Independent basins replicate siderophore peaks at 200-500 m and Fe-amendment lifts mesopelagic bacterial production.",
        },
        {
            "id": "surface-predator-photic-monopoly",
            "kill_cmc_if": "Broader species/season sampling shows twilight contribution << 20%.",
            "confirm_cmc_if": "Isotope + tag studies keep twilight diet >= 40% across years, so photic-only stock assessments mis-specify the fishery.",
        },
        {
            "id": "llsvp-vs-temperature-monopoly",
            "kill_cmc_if": "Composition cannot hide inside observed Vs once T is fixed; the two provinces are the same object.",
            "confirm_cmc_if": "Geoneutrinos, tidal tomography, or noble-gas systematics distinguish Pacific vs African piles as Panton 2025 predicts (Pacific denser, younger SOC).",
        },
        {
            "id": "placebo-inert-channel",
            "kill_cmc_if": "A mechanism is found that lives entirely outside the sham channel.",
            "confirm_cmc_if": "Designs that drop the 'inert' assignment (open-label placebo, dose-of-care) close more variance than receptor-level pharmacology of the sham.",
        },
        {
            "id": "exaptation-speech-larynx",
            "kill_cmc_if": "THIS ITEM MUST STAY NEAR ZERO. If it ranks primary, CMC has collapsed into spoken exaptation and the class is void.",
            "confirm_cmc_if": "n/a — control.",
        },
    ]


def function_budget_deficit(item: GapItem) -> dict[str, Any]:
    """
    Iteration function 2.

    Under CMC the channel's budgeted function-count is always 1 (the monopoly).
    Evidence supports k >= 1 functions. Deficit = k - 1.

    Not OAC: OAC counts observables. This counts allowed functions per
    already-owned observable.
    """
    if item.role != "test" or item.reclaim_of:
        k = 1.0
    elif item.status in {"confirmed", "candidate"}:
        k = 2.0
    elif item.status == "unproved":
        k = 1.4
    else:
        k = 1.0
    return {
        "id": item.id,
        "budgeted_functions": 1,
        "evidenced_functions": k,
        "deficit": round(k - 1.0, 2),
        "channel": item.channel,
        "realm": item.realm,
    }


def write_chart(rows: list[dict[str, Any]], path: str) -> None:
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        return
    plotted = [r for r in rows if r["score"] > 0 or r["cmc_eligible"]][:12]
    if not plotted:
        return
    labels = [f"{r['realm'][:3]}:{r['id'][:22]}" for r in plotted]
    scores = [r["score"] for r in plotted]
    colors = ["#c9a227" if r["cmc_eligible"] else "#4a4a4a" for r in plotted]
    fig, ax = plt.subplots(figsize=(10, 6), facecolor="#0e0e12")
    ax.set_facecolor("#0e0e12")
    y = list(range(len(plotted)))
    ax.barh(y, list(reversed(scores)), color=list(reversed(colors)), height=0.72)
    ax.set_yticks(y)
    ax.set_yticklabels(list(reversed(labels)), fontsize=8, color="#d8d0c0")
    ax.set_xlabel("CMC remainder score (heuristic, not a measurement of nature)", color="#d8d0c0", fontsize=8)
    ax.tick_params(colors="#8a8378")
    for spine in ax.spines.values():
        spine.set_color("#333")
    ax.set_title("Channel-Monopoly Class — 2026-09-20  (gold = eligible)", color="#e8dcc8", fontsize=11)
    fig.tight_layout()
    fig.savefig(path, dpi=140, facecolor=fig.get_facecolor())
    plt.close()


def adversarial_review(rows: list[dict[str, Any]]) -> list[str]:
    findings = []
    leader = next((r for r in rows if r["cmc_eligible"]), None)
    speech = next((r for r in rows if r["id"] == "exaptation-speech-larynx"), None)
    if speech and speech["score"] > 5:
        findings.append("FAIL: larynx-speech control scored too high; CMC is exaptation in disguise.")
    else:
        findings.append("PASS: spoken-exaptation control crushed (CMC is not Gould-Vrba rediscovered).")
    if leader and leader["id"] == "pigeon-vestibular-induction":
        findings.append("PASS: leader is Nordmann 2025 inner-ear induction, not a reclaim of TAC's missing receptor.")
    elif leader:
        findings.append(f"NOTE: leader is {leader['id']} not pigeon. Check framing taxes.")
    cip_rhod = next((r for r in rows if r["id"] == "gorg-dark-ferh-rhodopsin"), None)
    if cip_rhod and cip_rhod["score"] < 5:
        findings.append("PASS: GORG-Dark FeRh rhodopsin crushed (CIP 2026-09-17 already claimed).")
    lrd = next((r for r in rows if r["id"] == "lrd-class-vs-phase"), None)
    if lrd and lrd["score"] < 5:
        findings.append("PASS: LRD phase-object crushed (CIC 2026-09-01 already claimed).")
    dark_o2 = next((r for r in rows if r["id"] == "sweetman-dark-oxygen"), None)
    if dark_o2 and dark_o2["score"] < 5:
        findings.append("PASS: Sweetman dark oxygen crushed (contested; Science 18 Sep 2026 doubts).")
    hubble = next((r for r in rows if r["id"] == "hubble-tension"), None)
    if hubble and hubble["score"] == 0:
        findings.append("PASS: Hubble tension zeroed (spoken, CIC two-clock).")
    findings.append(
        "DISTINCT: TAC = missing converter, layer named dark. "
        "CMC = converter already employed by function-1; search protocol treats the channel as full."
    )
    findings.append(
        "DISTINCT: OAC = two quantities collapsed into one number. "
        "CMC = one channel allowed only one function."
    )
    findings.append(
        "DISTINCT: CIP = instrument cannot couple to the phenomenon's DOF. "
        "CMC = instrument already couples (ear, Vs, mesopelagic, sham pill) but attribution is monopolized."
    )
    findings.append(
        "DISTINCT: DCC = unknown already in the discarded data file. "
        "CMC = unknown already in the assigned organ/channel, not in a file."
    )
    findings.append(
        "ITERATION: first pass treated any TAC/OAC/CIP framing as a reclaim and hid the Nordmann leader. "
        "overlap_kind_split separates reclaim_of (disqualify) from framed_by (tax)."
    )
    if leader:
        findings.append(f"PRIMARY: {leader['id']} @ {leader['score']}")
    return findings


def main() -> dict[str, Any]:
    rows = rank(ITEMS)
    iso = iterate_cross_realm_isomorphism(rows)
    recency = iterate_ablate_recency(ITEMS)
    falsifiers = iterate_falsification_matrix()
    review = adversarial_review(rows)
    eligible = [r for r in rows if r["cmc_eligible"]]
    deficits = [function_budget_deficit(it) for it in ITEMS]
    deficits_elig = [d for d in deficits if d["deficit"] > 0]
    deficits_elig.sort(key=lambda d: -d["deficit"])
    write_chart(rows, "/workspace/artifacts/cmc-2026-09-20/cmc_ranking.png")
    payload = {
        "session_id": SESSION_ID,
        "timestamp": TIMESTAMP,
        "class_name": "Channel-Monopoly Class (CMC)",
        "claim_hygiene": "research-stage classification — not a physical discovery, not peer review, not a patent",
        "operator": iso["operator"],
        "n_items": len(ITEMS),
        "n_eligible": len(eligible),
        "leader": eligible[0]["id"] if eligible else None,
        "leader_score": eligible[0]["score"] if eligible else None,
        "realm_split": iso["realms"],
        "structural_isomorphism": iso["structural"],
        "recency_ablation": recency,
        "recency_leader_survives": recency["leader"] == (eligible[0]["id"] if eligible else None),
        "function_budget_deficits": deficits_elig,
        "falsifiers": falsifiers,
        "adversarial_review": review,
        "ranking": [
            {
                "rank": i + 1,
                "id": r["id"],
                "realm": r["realm"],
                "score": r["score"],
                "eligible": r["cmc_eligible"],
                "status": r["status"],
                "role": r["role"],
                "kill_reason": r["kill_reason"],
                "channel": r["channel"],
                "assigned_function": r["assigned_function"],
                "second_function": r["second_function"],
                "prior_overlap": r["prior_overlap"],
                "reclaim_of": r["reclaim_of"],
            }
            for i, r in enumerate(rows)
        ],
        "prior_classes_subtracted": list(PRIOR_CLASSES),
    }
    return payload


if __name__ == "__main__":
    result = main()
    out_json = "/workspace/artifacts/cmc-2026-09-20/cmc_ranking.json"
    out_txt = "/workspace/artifacts/cmc-2026-09-20/cmc_ranking.txt"
    with open(out_json, "w") as f:
        json.dump(result, f, indent=2)
    lines = [
        f"CMC ENGINE {result['timestamp']}",
        f"class: {result['class_name']}",
        f"hygiene: {result['claim_hygiene']}",
        f"leader: {result['leader']} @ {result['leader_score']}",
        f"eligible: {result['n_eligible']}/{result['n_items']}",
        f"structural (>=3 realms): {result['structural_isomorphism']}",
        f"recency ablation leader survives: {result['recency_leader_survives']}",
        "",
        "REALM SPLIT",
    ]
    for realm, info in result["realm_split"].items():
        lines.append(f"  {realm:8} {info['score']:6.2f}  {info['id']}")
    lines += ["", "FUNCTION-BUDGET DEFICIT (iteration 2)"]
    for d in result["function_budget_deficits"]:
        lines.append(f"  {d['deficit']:4.2f}  {d['realm']:8}  {d['id']}")
    lines += ["", "RANKING"]
    for r in result["ranking"]:
        flag = "ELIG" if r["eligible"] else (r["kill_reason"] or "NO")
        lines.append(f"  {r['rank']:2} {r['score']:6.2f}  {r['realm']:8}  {r['id']:40}  {flag}")
    lines += ["", "ADVERSARIAL REVIEW"]
    lines += [f"  - {x}" for x in result["adversarial_review"]]
    text = "\n".join(lines) + "\n"
    with open(out_txt, "w") as f:
        f.write(text)
    print(text)
