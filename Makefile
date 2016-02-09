BASE = .

commits.pickle: ./commits-combined.csv
	$(BASE)/tokenize_and_pickle.py $<

commits-combined.csv: commit-status.csv commits.csv
	$(BASE)/join.py $^

commit-status.csv: commits.csv
	$(BASE)/get_builds.rb
