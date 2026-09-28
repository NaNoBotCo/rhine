# The Rhine Deck · สำรับไรน์

J.B. Rhine's ESP tests from Duke University, to play against a server that deals and checks every card:
clairvoyance, precognition and dice, pooled tallies for people and robots, and a daily forecast drawn from
drand. English and Thai.

Site: https://nanobotco.github.io/rhine/ · API: https://rhine-lab.nanobotco.workers.dev/

    python3 tools/build.py && python3 tools/card.py    # docs/
    python3 tools/serve.py 8951                        # http://localhost:8951/rhine/
    cd worker && npx wrangler deploy                   # the API (D1: rhine-lab)
