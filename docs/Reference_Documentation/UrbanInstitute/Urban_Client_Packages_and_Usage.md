# Urban Client Packages and Usage

## 1. Official access methods

Urban's documentation explicitly supports:
- direct URL access to the API
- an official **R** package
- an official **Stata** package

The docs also state that Python and JavaScript examples work by directly calling endpoint URLs.

For TNTECHeck, that means your web application can rely on ordinary HTTP requests. You are not blocked by the absence of a dedicated JavaScript SDK.

---

## 2. R package

Repository:
- https://github.com/UrbanInstitute/education-data-package-r

The R package exposes:

```r
get_education_data(level, source, topic, subtopic, filters, add_labels)
```

Documented arguments include:
- `level` (required)
- `source` (required)
- `topic` (required)
- `subtopic` (optional list of grouping parameters)
- `filters` (optional list of query filters)
- `add_labels`
- `csv`
- `verbose`

### Why this matters
The R package README is valuable even if you are not using R, because it acts like a compact machine-readable index of:
- endpoint names
- available years
- subtopics
- main filters

In other words, the R repo is part documentation and part endpoint catalog.

### Example from Urban
```r
library(educationdata)

df <- get_education_data(
  level = "schools",
  source = "ccd",
  topic = "enrollment",
  subtopic = list("race", "sex"),
  filters = list(
    year = 2008,
    grade = 9:12,
    ncessch = "340606000122"
  ),
  add_labels = TRUE
)
```

### Relevance to TNTECHeck
Even though TNTECHeck will likely not use R in production, the package docs are useful to:
- verify endpoint names
- verify supported years
- understand how Urban conceptualizes `level`, `source`, `topic`, and `subtopic`

---

## 3. Stata package

Repository:
- https://github.com/UrbanInstitute/education-data-package-stata

Urban's Stata package README includes both installation and practical examples.

### Install
```stata
ssc install libjson
ssc install educationdata, replace
```

### Example commands
```stata
educationdata using "college ipeds directory", meta
educationdata using "college ipeds directory", sub(year=2011 fips=12)
```

### Why this matters
The Stata package README is helpful for college-specific phrasing and use cases. It also includes a quickstart example explicitly referencing pulling data for **a specific college and major by race and gender for all years**.

For a grants-oriented dashboard, that is a strong signal that Urban expects users to do exactly the kind of institution-plus-program slicing TNTECHeck will need.

---

## 4. Direct Python usage

Urban's docs state that Python access uses direct endpoint URLs. A modern TNTECHeck backend would typically use `requests` or `httpx`, not just `urllib`, but the principle is the same.

### Minimal example
```python
import requests

url = "https://educationdata.urban.org/api/v1/college-university/ipeds/directory/2022/"
params = {"unitid": "221847"}  # example filter pattern; actual filter names depend on endpoint
resp = requests.get(url, params=params, timeout=30)
resp.raise_for_status()
data = resp.json()
```

### Pagination note
If the response spans multiple pages, your backend should follow the API's pagination links rather than assuming a single-page payload.

---

## 5. Direct JavaScript usage

Urban's docs note JavaScript examples using direct URL access. For TNTECHeck, a normal `fetch()` call is sufficient.

### Minimal example
```js
const url = new URL("https://educationdata.urban.org/api/v1/college-university/ipeds/directory/2022/");
url.searchParams.set("unitid", "221847");

const resp = await fetch(url.toString());
if (!resp.ok) throw new Error(`Urban API error: ${resp.status}`);
const data = await resp.json();
```

### Recommended pattern for TNTECHeck
Do not call Urban directly from every browser component.
Instead:
1. create a server-side Urban adapter
2. normalize endpoint metadata and filters
3. cache results
4. expose a stable internal API to the frontend

That avoids leaking source-specific complexity into the UI.

---

## 6. Suggested adapter contract for TNTECHeck

```ts
interface UrbanQuery {
  level: "college-university";
  source: string;
  topic: string;
  year?: number;
  subtopic?: string[];
  filters?: Record<string, string | number | Array<string | number>>;
  summary?: {
    var: string;
    stat: "sum" | "count" | "avg" | "min" | "max" | "variance" | "stddev" | "median";
    by?: string[];
  };
}
```

```ts
interface UrbanResult {
  requestUrl: string;
  sourceMeta: {
    level: string;
    source: string;
    topic: string;
    year?: number;
    subtopic?: string[];
  };
  rows: unknown[];
  raw: unknown;
}
```

---

## 7. What to borrow from Urban's client packages

Borrow these ideas:

- **level / source / topic / subtopic** as first-class concepts
- centralized endpoint registry
- label enrichment where available
- built-in pagination handling
- a simple public API for analysts

Do **not** copy the packages blindly into project architecture.  
TNTECHeck needs a web-app adapter layer, not an R- or Stata-style command interface.

---

## 8. Recommendation

For TNTECHeck, use:
- Urban's **official docs** for syntax and policy
- Urban's **R repo** as the best compact endpoint index
- Urban's **Stata repo** for practical college-oriented usage patterns
- your own backend adapter for actual production integration
