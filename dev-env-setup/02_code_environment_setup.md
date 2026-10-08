# Code Environment Setup

## 1. Setup VSCode

1. Install VSCode by following this guide: https://code.visualstudio.com/docs/setup/linux
2. Install the following extensions:
    - https://marketplace.visualstudio.com/items?itemName=ms-vscode.cpptools
    - https://marketplace.visualstudio.com/items?itemName=ms-vscode.cmake-tools
3. Press CTRL+SHIFT+P and choose "Preferences: Open User Settings (JSON)" and paste the following code settings into it:
    ```
    {
        // Editor
        "editor.formatOnSave": true,
        "editor.tabSize": 4,
        "editor.detectIndentation": false,
        "editor.insertSpaces": true,
        "editor.renderFinalNewline": "on",
        "editor.foldingStrategy": "indentation",
        "editor.acceptSuggestionOnEnter": "off",
        // C++
        "C_Cpp.default.intelliSenseMode": "gcc-x64",
        "C_Cpp.intelliSenseCacheSize": 0,
        "C_Cpp.workspaceParsingPriority": "high",
        // C++ Formatting
        "C_Cpp.clang_format_fallbackStyle": "none",
        "C_Cpp.clang_format_path": "/usr/bin/clang-format",
        // C++ Linting
        "C_Cpp.codeAnalysis.runAutomatically": true,
        "C_Cpp.codeAnalysis.clangTidy.enabled": true,
        "C_Cpp.codeAnalysis.clangTidy.path": "/usr/bin/clang-tidy",
    }
    ```
