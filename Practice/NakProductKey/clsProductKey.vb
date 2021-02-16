Imports System.IO
Imports System.Text

Public Class clsProductKey

    Private enc As Encoding
    Private Const strPpack As String = "中村君千葉県柏市松葉町"

    Public Sub New()
        enc = Encoding.GetEncoding("Shift_JIS")
    End Sub

    Public Sub New(ByVal encStr As String)
        enc = Encoding.GetEncoding(encStr)
    End Sub

    ''' <summary>
    ''' Hex文字列のProductKeyとNameから生成したProductKeyが同じかどうかチェックする
    ''' </summary>
    ''' <param name="P_Name"></param>
    ''' <param name="P_ProductKey"></param>
    ''' <returns></returns>
    ''' <remarks></remarks>
    Public Function CheckKey(P_Name As String, P_ProductKey As String) As String
        Dim strFromName As String = MakeKey(P_Name)

        If strFromName.Equals(DelDelimiter(P_ProductKey, " ")) _
            Or strFromName.Equals(DelDelimiter(P_ProductKey, "-")) Then
            Return "1"
        Else
            Return "0"
        End If
    End Function

    Public Function MakeKey(P_Name As String) As String
        'Dim nameBytes() As Byte = System.Text.Encoding.GetEncoding("Shift_JIS").GetBytes(Name) '932

        Dim strPackedName As String = P_Name & strPpack
        Dim nameBytes() As Byte = enc.GetBytes(strPackedName)

        Dim str As String = ""
        Dim i As Integer
        If True Then    '   配列を変える。
            str += String.Format("{0:X2}", nameBytes(1))
            str += String.Format("{0:X2}", nameBytes(0))

            str += String.Format("{0:X2}", nameBytes(3))
            str += String.Format("{0:X2}", nameBytes(2))

            str += String.Format("{0:X2}", nameBytes(5))
            str += String.Format("{0:X2}", nameBytes(4))

            str += String.Format("{0:X2}", nameBytes(7))
            str += String.Format("{0:X2}", nameBytes(6))
        Else
            For i = 0 To nameBytes.Length - 1
                If i < 8 Then
                    str &= String.Format("{0:X2}", nameBytes(i))
                Else
                    Exit For
                End If
            Next
        End If

        Return str
    End Function

    ''' <summary>
    ''' 入力文字列をHex文字列にする。結果は[MakeKey]と同じ
    ''' </summary>
    ''' <param name="P_Name"></param>
    ''' <returns></returns>
    ''' <remarks></remarks>
    Public Function MakeKey2(P_Name As String) As String
        Dim bytFromName As Byte() = enc.GetBytes(P_Name & strPpack)
        ' 出力：83-56-83-74-83-67-4A-49-53-82-D6-95-CF-8A-B7
        Dim strFromName As String = BitConverter.ToString(bytFromName)
        Dim strHex As String = DelDelimiter(strFromName, "-")

        Return strHex
    End Function

    ''' <summary>
    ''' BitConverter.ToString(bytFromName) の出力から、[-]を削除する。
    ''' </summary>
    ''' <param name="p_strHyphen"></param>
    ''' <returns></returns>
    ''' <remarks></remarks>
    Public Function DelDelimiter(P_strHyphen As String, P_strDelimiter As String) As String
        Dim strArray() As String = P_strHyphen.Split(P_strDelimiter)

        Dim strHex As String = ""
        For Each strOneChar As String In strArray
            strHex &= strOneChar
        Next

        Return strHex
    End Function

    Public Function Decode(P_ProductKey As String) As String
        Dim bytes() As Byte = StringToByteArray(P_ProductKey)
        Return enc.GetString(bytes)
    End Function

    Public Function StringToByteArray(P_ProductKey As String) As Byte()
        Dim NumberChars As Integer = P_ProductKey.Length
        Dim bytes As Byte() = New Byte(NumberChars / 2 - 1) {}
        For i As Integer = 0 To NumberChars - 1 Step 2
            bytes(i / 2) = Convert.ToByte(P_ProductKey.Substring(i, 2), 16)
        Next
        Return bytes
    End Function

End Class
