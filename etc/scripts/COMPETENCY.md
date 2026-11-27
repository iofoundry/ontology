# Competency tests

Competency questions check that IOF does the job: a dataset is loaded on top of the IOF
modules it imports, optionally entailed with HermiT, and questions about it are answered
with SHACL or SPARQL. (Hygiene tests, in `etc/testing/hygiene_shapes`, check that IOF is
well-formed.)

The runner is here (`competency_runner.py`, run as `./competency`); the questions and
their data are in the **private** repository
[`iofoundry/ontology-questions`](https://github.com/iofoundry/ontology-questions)
(IOF members only), because some of the data is member-contributed. That repository's
README is the authoring guide: layout, the `# description:` / `# reasoning:` header,
graphs, expected CSVs and the list of suites.

## The overlay

The questions repository is overlaid at `etc/testing/competency/` (git-ignored here —
never a submodule):

```bash
git clone git@github.com:iofoundry/ontology-questions.git ../ontology-questions   # once
ln -s ../../../ontology-questions etc/testing/competency                         # once
./competency                                  # every suite
./competency provisional/slots                # one category of suites
./competency provisional/slots/fasteners      # one suite (a dataset and its question sets)
./competency provisional/slots/fasteners/bolt-types   # one question set
./competency --no-cache                       # force HermiT
./competency --update-expected                # (re)write the .expected.csv files
./competency --redact                         # as CI: print nothing from the data
python -m unittest discover -s etc/scripts/tests -t etc/scripts   # the runner's own tests
```

Without the overlay the runner prints a notice and exits 0. `--base DIR` points it
elsewhere.

## How a suite runs

- **Imports.** A suite (`<tier>/[<category>/...]<dataset>/`: a directory with data files; directories
  between the tier and a suite are categories) loads only its own files and what they
  `owl:imports`, resolved through `catalog-v001.xml` (plus the suite's overlay catalog);
  nothing is fetched from the web. A `release/` suite may only import modules in
  `AboutIOFProd.rdf`.
- **One load per suite.** The import closure is resolved once for all the suite's question
  sets. HermiT runs once if any question has `# reasoning: true`; questions with
  `# reasoning: false` are asked of the asserted triples alone (parsed directly, so the
  result does not depend on whether HermiT ran). A suite with no reasoning questions never
  starts HermiT.
- **Engines.** SPARQL questions are evaluated by Oxigraph (`pyoxigraph`), SHACL by pySHACL;
  rdflib only parses. rdflib's own SPARQL evaluator took minutes per query on the BTEC
  suites' multi-pattern joins that Oxigraph answers in milliseconds. In expected CSVs,
  numbers compare by value (`25.0` matches `25`), since engines write them differently.
- **Cache.** HermiT results are cached in `build/competency/<suite name>/`, keyed on
  the content of every file in the import closure and the runner's entailment code.
  Pre-entailing IOF and layering the data on top does not help: HermiT has no incremental
  mode (on the fasteners suite, 185 s with IOF's entailments preloaded vs 192 s from
  scratch).
- **Expected inconsistency.** A reasoning question with `# expect: inconsistent` passes
  only if HermiT finds the suite's data inconsistent (its body is not run). When every
  reasoning question in a suite expects it, the inconsistency is a notice, not a
  reasoner failure; any other reasoning question in that suite is reported not run.
- **Results.** Failures are errors in `release/` (they block the build) and warnings in
  `provisional/`. A broken suite or question (unresolved import, unparseable file, missing
  header or expected CSV, a release suite importing a provisional module) is an error in
  both. Each question's description is printed as it runs.

## CI (`.github/workflows/build.yml`)

`competency-suites` checks out the questions and lists the suites; `competency-tests`
runs one parallel job per suite.

**Who can read the questions.** A workflow run uses the workflow file *of the branch it
runs on*, so anyone who can push a branch could edit the workflow to copy the questions
or the deploy key somewhere. Repository secrets are given to every branch, so the
secrets are instead in the **`competency` environment**, which only `master`,
`review/*`, `staging/*` and `releases/*` may use. A workflow edited on any other branch gets no
secrets (GitHub refuses the job), and changing the workflow on an allowed branch needs a
reviewed pull request (branch protection). Consequently:

- The competency jobs run on pushes and manual runs on `master`, `review/*`, `staging/*`
  and `releases/*` only — after a pull request is merged, not on the pull request itself or
  on feature branches, where they are skipped (not failed). Run the questions locally
  before opening the pull request.
- Pull requests from forks and Dependabot never get secrets either.

**Public logs and caches.** This repository is public, so:

- The runner runs with **`--redact`**: question names, descriptions and counts only;
  never result rows, focus nodes, data IRIs or parser messages. Debug failures locally.
- The entailment cache is **encrypted** (`openssl enc -aes-256-cbc -pbkdf2`) before it is
  saved: other branches and forks can restore this repository's caches but have no key.

A manual run (`workflow_dispatch`, on an allowed branch) can pick the questions branch
(`questions-ref`, default `main`).

### Setup (once, by a repository admin)

1. Create a key pair: `ssh-keygen -t ed25519 -N "" -C ontology-ci -f oq_deploy`.
2. In `iofoundry/ontology-questions` → Settings → Deploy keys: add `oq_deploy.pub`,
   **read-only**.
3. In `iofoundry/ontology` → Settings → Environments → New environment `competency`:
   - Deployment branches and tags → **Selected branches and tags**: add `master`,
     `review/*`, `staging/*` and `releases/*`.
   - Environment secrets:
     - `ONTOLOGY_QUESTIONS_DEPLOY_KEY` = the contents of `oq_deploy` (private key);
     - `COMPETENCY_CACHE_KEY` = a random string, e.g. `openssl rand -base64 32`.
   - Do **not** also add these as repository secrets — that would give them to every
     branch again.
4. Protect every allowed branch with a ruleset targeting `master`, `review/**`,
   `staging/**` and `releases/**`:
   - **Restrict creations** — otherwise anyone with write access can create a new
     matching branch (e.g. `review/x`) with an edited workflow and get the secrets;
   - **Require a pull request** with an approving review (ideally a CODEOWNER of
     `.github/`), and block force pushes and deletions;
   - bypass list: only the people who cut release, staging and review branches.

   The environment rule is only as strong as this: anyone who can push straight to, or
   create, an allowed branch can run any workflow there. A branch pattern people push to
   directly does not belong in the environment.
5. Delete the local key files. Rotate the key (repeat 1–3) if it may have leaked.

If more branches should run the questions, add them both to the environment's branch
list and to the jobs' `if:` condition in the workflow.
