# Intelligent Resume Analyzer

The Intelligent Resume Analyzer is the Day 10 capstone project for the HiDevs GenAI Internship. It parses resume text, extracts candidate details, compares them against a job requirement profile, and generates a readable hiring recommendation.

## What It Does

- Extracts candidate name, email, skills, experience, and education from resume text
- Scores each candidate out of 100 using skills, experience, and education
- Uses fuzzy matching when `fuzzywuzzy` is available, with a simple fallback if it is not
- Prints a formatted analysis report for each candidate
- Saves the parsed candidate data to `candidates.json`

## Files

- `Intelligent_Resume_Analyzer.py` - main script
- `requirements.txt` - optional dependencies for fuzzy skill matching
- `README.md` - project overview and usage

## Requirements

- Python 3.12 or newer is recommended
- Optional package:
	- `fuzzywuzzy`

If `fuzzywuzzy` is not installed, the script still runs using a built-in fallback matcher.

## Installation

Install the optional dependency if you want fuzzy matching support:

```sh
pip install -r requirements.txt
```

## Run

Run the project from the Day 10 folder:

```sh
python Intelligent_Resume_Analyzer.py
```

If you are using the alternate filename shown in some terminals, make sure the script name matches the file in your folder exactly.

## Output

When you run the script, it will:

1. Parse three sample resumes
2. Print a report for each candidate
3. Save the parsed candidate list to `candidates.json`

## Sample Scoring Logic

- Skills: 50 points
- Experience: 30 points
- Education: 20 points

The final score is capped at 100.

## Example Recommendation

- `80-100`: STRONGLY RECOMMEND
- `60-79`: RECOMMEND
- `40-59`: MAYBE
- `0-39`: NOT RECOMMENDED

## Notes

- The project currently uses sample resume text embedded in the script.
