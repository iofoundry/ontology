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
./competency provisional/fasteners            # one suite (a dataset and its question sets)
./competency provisional/fasteners/bolt-types # one question set
./competency --no-cache                       # force HermiT
./competency --update-expected                # (re)write the .expected.csv files
./competency --redact                         # as CI: print nothing from the data
python -m unittest discover -s etc/scripts/tests -t etc/scripts   # the runner's own tests
```

Without the overlay the runner prints a notice and exits 0. `--base DIR` points it
elsewhere.

## How a suite runs

- **Imports.** A suite (`<tier>/<dataset>/`) loads only its own files and what they
  `owl:imports`, resolved through `catalog-v001.xml` (plus the suite's overlay catalog);
  nothing is fetched from the web. A `release/` suite may only import modules in
  `AboutIOFProd.rdf`.
- **One load per suite.** The import closure is resolved once for all the suite's question
  sets. HermiT runs once if any question has `# reasoning: true`; questions with
  `# reasoning: false` are asked of the asserted triples alone (parsed directly, so the
  result does not depend on whether HermiT ran). A suite with no reasoning questions never
  starts HermiT.
- **Cache.** HermiT results are cached in `build/competency/<tier>/<dataset>/`, keyed on
  the content of every file in the import closure and the runner's entailment code.
  Pre-entailing IOF and layering the data on top does not help: HermiT has no incremental
  mode (on the fasteners suite, 185 s with IOF's entailments preloaded vs 192 s from
  scratch).
- **Results.** Failures are errors in `release/` (they block the build) and warnings in
  `provisional/`. A broken suite or question (unresolved import, unparseable file, missing
  header or expected CSV, a release suite importing a provisional module) is an error in
  both. Each question's description is printed as it runs.

## CI (`.github/workflows/build.yml`)

`competency-suites` checks out the questions and lists the suites; `competency-tests`
runs one parallel job per suite. This repository is public — so are its Actions logs and
caches — so:

- The runner runs with **`--redact`**: question names, descriptions and counts only;
  never result rows, focus nodes, data IRIs or parser messages. Debug failures locally.
- The entailment cache is **encrypted** (`openssl enc -aes-256-cbc -pbkdf2`) before it is
  saved: a pull request from a fork can restore this repository's caches but has no key.
- Without the deploy key (forks, Dependabot) no suites are listed and the competency jobs
  are skipped, not failed.
- A manual run (`workflow_dispatch`) can pick the questions branch (`questions-ref`,
  default `main`).

### Setup (once, by a repository admin)

1. Create a key pair: `ssh-keygen -t ed25519 -N "" -C ontology-ci -f oq_deploy`.
2. In `iofoundry/ontology-questions` → Settings → Deploy keys: add `oq_deploy.pub`,
   **read-only**.
3. In `iofoundry/ontology` → Settings → Secrets and variables → Actions:
   - `ONTOLOGY_QUESTIONS_DEPLOY_KEY` = the contents of `oq_deploy` (private key);
   - `COMPETENCY_CACHE_KEY` = a random string, e.g. `openssl rand -base64 32`.
4. Delete the local key files.

Anyone who can push a branch to this repository can run a workflow that reads these
secrets; that is the same set of people (IOF members) who can read the questions.
