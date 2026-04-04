# The Men — Golf Tracker

## Known Issues & Fixes

### ESPN API incomplete hole data (April 2026)
**Problem:** ESPN's scoreboard API sometimes returns fewer than 18 hole-by-hole entries for completed rounds (e.g., 17 instead of 18). The `isRoundComplete()` function required all 18 holes, so it would fail to detect a finished round — meaning round winners wouldn't get awarded their $12.

**Fix:** Added a fallback in `isRoundComplete()`: for rounds 1-3, if any active player has started the next round (has hole data in the subsequent round), the current round is marked complete. This avoids relying solely on potentially incomplete hole counts from ESPN.

**Where:** The `isRoundComplete()` function inside each tournament HTML file.
