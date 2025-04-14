# WORDでHTMLに保存するマクロ

```
Sub ExportToHTML()
    Dim doc As Document
    Set doc = ActiveDocument

    Dim savePath As String
    savePath = ThisDocument.Path & "\output.html"

    doc.SaveAs2 FileName:=savePath, FileFormat:=wdFormatHTML

    MsgBox "HTML file saved to: " & savePath
End Sub
```

# マクロをPowerShellから実行する

## COM (Component Object Model) オブジェクトを利用する方法

PowerShellはCOMオブジェクトを操作する機能を持っており、WordのApplicationオブジェクトを介してVBAマクロを実行できます。

```
# Wordアプリケーションのインスタンスを作成（既に起動している場合はそれを取得）
try {
    $Word = [System.Runtime.InteropServices.Marshal]::GetActiveObject("Word.Application")
} catch {
    $Word = New-Object -ComObject Word.Application
    $Word.Visible = $false # 必要に応じてWordのウィンドウを非表示にする
}

# 実行したいWordファイルへのパス
$WordFilePath = "C:\path\to\your\document.docx"

# Wordドキュメントを開く
$Document = $Word.Documents.Open($WordFilePath)

# 実行したいVBAマクロの名前
$MacroName = "YourMacroName"

try {
    # マクロを実行
    $Word.Run($MacroName)
} catch {
    Write-Error "VBAマクロの実行中にエラーが発生しました: $($_.Exception.Message)"
} finally {
    # ドキュメントを閉じる（必要に応じて保存）
    $Document.Close([ref]$false) # 保存しない場合は$false、保存する場合は$true

    # Wordアプリケーションを終了する（必要に応じて）
    # $Word.Quit()
    # [System.Runtime.InteropServices.Marshal]::ReleaseComObject($Word)
}

# COMオブジェクトの解放
[System.Runtime.InteropServices.Marshal]::ReleaseComObject($Document)
[System.Runtime.InteropServices.Marshal]::ReleaseComObject($Word)
Remove-Variable Word, Document
```

### このスクリプトのポイント:

- [System.Runtime.InteropServices.Marshal]::GetActiveObject("Word.Application"): 既に起動しているWordアプリケーションのインスタンスを取得しようとします。
- New-Object -ComObject Word.Application: Wordが起動していない場合に、新しいWordアプリケーションのインスタンスを作成します。
- $Word.Visible = $false: Wordのウィンドウを非表示にしてバックグラウンドで処理できます。必要に応じて $true に変更して表示させることも可能です。
- $Word.Documents.Open($WordFilePath): 指定したWordファイルを開きます。
- $Word.Run($MacroName): 指定した名前のVBAマクロを実行します。マクロ名は大文字・小文字を区別する場合がありますので注意してください。
- $Document.Close([ref]$false): 開いたWordドキュメントを閉じます。[ref]$true にすると保存確認のダイアログが表示される場合があります。
- $Word.Quit(): Wordアプリケーションを終了します。他のWordドキュメントを開いている可能性がある場合は、この行をコメントアウトすることを推奨します。
- [System.Runtime.InteropServices.Marshal]::ReleaseComObject(): 使用したCOMオブジェクトを解放し、リソースリークを防ぎます。
-

## Wordのコマンドラインオプションを利用する方法 (間接的)

Wordには、コマンドラインから特定のドキュメントを開いたり、特定の処理を実行したりするオプションがありますが、直接的に任意のVBAマクロを実行するオプションは標準では提供されていません。

ただし、VBAマクロ内でドキュメントを開いた際に自動的に実行されるように設定しておけば、PowerShellからWordを起動し、そのドキュメントを開くことで間接的にマクロを実行できます。

例えば、AutoOpen マクロをWordドキュメントに記述しておくと、そのドキュメントが開かれた際に自動的に実行されます。

PowerShellからWordを起動してドキュメントを開く例:

```
$WordFilePath = "C:\path\to\your\document_with_autoopen_macro.docx"

try {
    Start-Process -FilePath "C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE" -ArgumentList "`"$WordFilePath`""
} catch {
    Write-Error "Wordの起動に失敗しました: $($_.Exception.Message)"
}
```

### 注意点:

- Wordのインストールパス: 上記の Start-Process の -FilePath は、Wordの実行ファイルのパスです。環境によって異なる場合がありますので、正しいパスを指定してください。
- セキュリティ設定: Wordのセキュリティ設定によっては、マクロの実行がブロックされる場合があります。必要に応じてWordのセキュリティ設定を確認・変更してください。
- エラー処理: スクリプトにはエラー処理を含めることを強く推奨します。
- COMオブジェクトの解放: COMオブジェクトを使用する場合は、必ず適切に解放するようにしてください。解放を怠ると、リソースリークが発生する可能性があります。
- マクロの存在: 指定したマクロ名がWordドキュメント内に存在することを確認してください。

どちらの方法を選ぶべきか:

直接的に特定のVBAマクロを実行したい場合: COMオブジェクトを利用する方法が適しています。
ドキュメントを開く際に自動的に実行されるマクロがある場合: Wordのコマンドラインオプションと AutoOpen マクロなどを組み合わせる方法も考えられますが、柔軟性はCOMオブジェクトを利用する方法に劣ります。
一般的には、COMオブジェクトを利用する方法が、PowerShellからWord内のVBAマクロを実行するためのより直接的で制御しやすい方法と言えるでしょう。

