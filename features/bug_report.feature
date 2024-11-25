Feature: test bug report button and version button

    # 使用者成功送出 Bug 回報 及 版本按鈕 的測試
    Scenario Outline: user sent bug report successfully
        Given user is on a page with QERP-BUG and version button
        When user submit reportText as "<reportText>" and file as "<file>"
        Then sent report successfully

        Examples:
            | reportText | file                                     |
            | 1002327011 | "D:\我的文件夾\Downloads\變形工時.pdf"   |
            | 1          | '"D:\我的文件夾\Downloads\變形工時.pdf"' |

