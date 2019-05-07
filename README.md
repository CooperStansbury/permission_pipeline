# Permission Pipeline
This is proof-of-concept ingestion of permissions into ontological instances. Predictions are generated using a model trained on human annotation of candidate permission statements. Work regarding model training and evaluation can be found here: [permission_statement_extraction](https://github.com/CooperStansbury/permission_statement_extraction). Once predictions are made, they are stored in a `.csv` for class instantiation in the [Informed Consent Ontology](https://github.com/ICO-ontology/ICO).

Currently, instantiation is rudimentary. Future work will be devoted to making predictions more robust and axiomatization of incoming instances of 'permission directives.'

## TODO:
1. Train new CNN to make predictions more robust.
1. Allow threshold specification for positive class prediction to be specified from the CLI.
1. Clean-up axiom definition.
1. Make axiom definition more interesting.
    1. Add document ids
    1. Add annotations for p(x)
    1. Add the person who 'signed' the form?
    1. Add synthetic instances of clinical data?
