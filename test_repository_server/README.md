This `test_repository_server` helps with setting up a simple AAS Repository Server for testing the semantic matcher.

How to use: 

In this directory:
```commandline
docker compose up
```

If the `storage` directory is empty, it can be filled via: 

```commandline
python3 put_example_submodels.py
```

Then you should have a running repository server. 
