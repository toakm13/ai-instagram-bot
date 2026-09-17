"""Production entrypoint that keeps the verified live runner but swaps in the locked premium visual system."""
from __future__ import annotations

import os
import sys

import evidyarthee_live as live
from evidyarthee_templates import render as premium_render


def main() -> int:
    lane = sys.argv[1] if len(sys.argv) > 1 else ""
    if lane not in {"pre-market", "educational", "post-market", "news"}:
        print("Usage: python evidyarthee_production.py [pre-market|educational|post-market|news]")
        return 2

    # run() resolves render from the live module's globals. Replace only that
    # renderer; research, duplicate protection, Metricool publishing and state
    # persistence remain the existing production implementation.
    os.environ["EVIDYARTHEE_LANE"] = lane
    live.render = premium_render
    result = live.run(lane)
    print(result)
    return 0 if result.get("status") in {"queued", "no_material_news", "duplicate", "blocked"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
