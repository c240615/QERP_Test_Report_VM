Feature: User Login

    # 成功登入的測試
    Scenario Outline: User logs in successfully with valid credentials
        Given the user is on the login page
        When the user enters Username as "<username>" and Password as "<password>"
        Then the user should be logged in successfully

        Examples:
            | username   | password |
            | 1002327011 | admin    |
            | 1          | admin    |

    # 登入失敗的測試
    Scenario Outline: User logs in with invalid credentials
        Given the user is on the login page
        When the user enters Username as "<username>" and Password as "<password>"
        Then the user should be redirected to the login page

        Examples:
            | username   | password |
            | 1          | Admin    |
            | 1002327011 | admin    |