Feature: Tests for bestsellers functionality

    Scenario: There are 5 bestsellers links
        Given Open Amazon Bestsellers
        Then Verify there are 5 links