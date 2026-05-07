## Sprint Generation Task

Today is {today_date} ({day_of_week}). Week {week_number} of the program.

### Student's Last Journal Entry
{journal_body}

### Journal Metadata
- Faculty: {journal_faculty}
- Status: {journal_status}
- Hours Spent: {journal_hours}
- Difficulty Rating: {journal_difficulty}
- Blocker: {journal_blocker}

### Current Syllabus Position
{syllabus_progress}

### This Week's Faculty Hours So Far
{weekly_hours_summary}

### Faculty Needing Attention (Underweight)
{underweight_faculties}

### Spaced Repetition Items Due
{sr_due_items}

### Competency Snapshot (Relevant Topics)
{competency_snapshot}

---

**Generate the next daily assignment.** Choose the faculty that is most underweight this week, unless:
- The student was blocked yesterday — address the blocker first
- An SR item is critically overdue (>7 days) — prioritize that faculty
- The syllabus has a time-sensitive milestone approaching

Output a single assignment in the specified markdown format.
