python3 generate_contributions_req.py contributions.yaml contributions.txt
pip install -r contributions.txt
python3 test_entry_points.py contributions.yaml www/data.json
