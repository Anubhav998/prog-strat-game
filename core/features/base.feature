Feature: The Basic Login Functions
  
  Scenario: Landing Screen
    Given I am on the page with relative url "/"
    Then I should be on the page with relative url "/landing/"

  Scenario: API Home Screen
    Given I am on the page with relative url "/api/"
    Then I should see the text "Api Root"

  Scenario: Login Page
    Given I am on the page with relative url "/login/"
    Then I should be on the page with relative url "/login/"

  Scenario: Swagger Docs Page
    Given I am on the page with relative url "/docs/"
    Then I should be on the page with relative url "/docs/"
    And I should see the text "Turn Based Progressional Game"

  Scenario Outline: Test out logging in via the api-ath and going to the homepage
    Given a super user with username "<user>" and password "<password>"
    And I am on the page with relative url "/api-auth/login"
    When I put "<user>" in the field with name "username"
    And I put "<password>" in the field with name "password"
    And I click the element with name "submit"
    Then I should be on the page with relative url "/accounts/profile/"
    Given I am on the page with relative url "/"
    Then I should be on the page with relative url "/#/"

  Examples:
    | user | password |
    | foo3 | bar3     |

   Scenario Outline: Test out logging out via the api-ath and going to the homepage
    Given a super user with username "<user>" and password "<password>"
    And I am on the page with relative url "/api-auth/login"
    When I put "<user>" in the field with name "username"
    And I put "<password>" in the field with name "password"
    And I click the element with name "submit"
    Then I should be on the page with relative url "/accounts/profile/"
    Given I am on the page with relative url "/logout/"
    Then I should be on the page with relative url "/login/"

  Examples:
    | user | password |
    | foo4 | bar4     |

  Scenario Outline: Test Logging in via the login page invalid
    Given an inactive user with username "<user>" and password "<password>"
    And I am on the page with relative url "/login/"
    When I put "<user>" in the field with name "username"
    And I put "<password>" in the field with name "password"
    And I click the element with name "submit"

  Examples:
    | user | password |
    | foo5 | bar5     |

  Scenario Outline: Test Logging in via the login page
    Given a user with username "<user>" and password "<password>"
    And I am on the page with relative url "/login/"
    When I put "<user>" in the field with name "username"
    And I put "<password>" in the field with name "password"
    And I click the element with name "submit"

  Examples:
    | user | password |
    | foo6 | bar6     |

  Scenario Outline: Test invalid Logging in via the login page
    Given a user with username "<user>" and password "<password>"
    And I am on the page with relative url "/login/"
    When I put "<user>" in the field with name "username"
    And I put "password" in the field with name "password"
    And I click the element with name "submit"

  Examples:
    | user | password |
    | foo7 | bar7     |