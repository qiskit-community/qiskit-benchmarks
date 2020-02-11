python generate_contributions_req.py contributions.yaml contributions.txt
pip install -r contributions.txt
python test_entry_points.py contributions.yaml www/data.json
