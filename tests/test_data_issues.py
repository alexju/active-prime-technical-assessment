from playwright.sync_api import expect


def test_navigate_to_data_issues_grid(issues_page):
    """Test 1: Navigate to the Data Issues page and verify 10 issue cards are displayed."""
    expect(issues_page.locator(".issue-card")).to_have_count(10)


def test_all_original_rows_have_nonempty_sfid(issues_page):
    """Test 2: Each card's original row contains a non-empty sfid value."""
    cards = issues_page.locator(".issue-card")
    expect(cards).to_have_count(10)

    for i in range(cards.count()):
        original_row = cards.nth(i).locator('tr[data-row-type="original"]')
        sfid = original_row.locator("td").last.inner_text().strip()
        assert sfid, f"Issue card #{i + 1} has an empty sfid in its original row"


def test_select_original_value_for_seventh_card(issues_page):
    """Test 3: On the 7th card, select the original value for the issue column
    and verify the final row updates to reflect it."""
    card = issues_page.locator(".issue-card").nth(6)
    original_row = card.locator('tr[data-row-type="original"]')

    original_value = original_row.locator(".cell-issue .cell-radio span").inner_text().strip()
    original_row.locator('input[type="radio"]').check()

    final_value = card.locator('tr[data-row-type="final"] .cell-editable span')
    expect(final_value).to_have_text(original_value, timeout=5000)


def test_edit_final_row_issue_field(issues_page):
    """Test 4: Edit the issue column in the final row of a specific card."""
    card = issues_page.locator('.issue-card[data-record-id="00Qak00000RHtuzEAD"]')
    editable_cell = card.locator('tr[data-row-type="final"] .cell-editable')

    editable_cell.click()
    edit_input = editable_cell.locator("input.inline-edit-input")
    edit_input.fill("123 Test Street")
    edit_input.press("Enter")

    expect(editable_cell.locator("span")).to_have_text("123 Test Street", timeout=5000)


def test_checkbox_selection_counter(issues_page):
    """Test 5: Selection counter shows correct counts and hides when empty."""
    checkboxes = issues_page.locator(".issue-checkbox")
    confirm_bar = issues_page.locator("#confirmBar")

    # Select 1st, 3rd and 5th cards.
    for index in (0, 2, 4):
        checkboxes.nth(index).check()
    expect(confirm_bar).to_be_visible()
    expect(confirm_bar).to_contain_text("3 issue(s) selected")

    # Select all.
    issues_page.locator("#selectAll").check()
    expect(confirm_bar).to_contain_text("10 issue(s) selected")

    # Deselect all.
    issues_page.locator("#selectAll").uncheck()
    expect(confirm_bar).not_to_be_visible()
