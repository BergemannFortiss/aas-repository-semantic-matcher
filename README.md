# AAS Repository Semantic Matcher

This is a proof-of-concept implementation for a simple semantic matcher for an AAS Repository.

Here's what it does:
- It connects to an existing AAS Repository Server
- It queries and indexes all the `semanticIDs` of the Submodels stored in that Repository Server
- It returns the semantically equivalent `semanticIDs` in a specific format needed for `Submodel Conformance Checking`
