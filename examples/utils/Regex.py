
from safethread.utils import Regex

# Create a Regex object with a pattern
pattern = r'\d+'  # Matches one or more digits
regex = Regex(pattern)

# Test the pattern on a string
test_string = "The price is 100.57 dollars"
match = regex.search(test_string)

if match:
    print(f"Match found: {match.group()}")
else:
    print("No match found")

# Find all matches in a string
all_matches = regex.find_all(test_string)
print(f"All matches: {all_matches}")

# Replace matches in a string
replaced_string = regex.sub('XXX', test_string)
print(f"Replaced string: {replaced_string}")
